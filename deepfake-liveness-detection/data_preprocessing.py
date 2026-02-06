"""
Data Preprocessing Pipeline
Processes the Kaggle deepfake dataset and extracts features
"""
import os
import numpy as np
from pathlib import Path
from tqdm import tqdm
import logging
from typing import List, Tuple
import json
import pickle

from utils import VideoProcessor, DatasetManager, create_directory_structure
from feature_extraction import process_video_to_features

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Main preprocessing pipeline for deepfake dataset"""
    
    def __init__(self, 
                 raw_data_path: str,
                 processed_data_path: str,
                 target_frames: int = 90,
                 num_workers: int = 4):
        """
        Initialize preprocessor
        
        Args:
            raw_data_path: Path to raw video dataset
            processed_data_path: Path to save processed features
            target_frames: Number of frames per video
            num_workers: Number of parallel workers
        """
        self.raw_data_path = Path(raw_data_path)
        self.processed_data_path = Path(processed_data_path)
        self.target_frames = target_frames
        self.num_workers = num_workers
        
        # Create directory structure
        self.processed_data_path.mkdir(parents=True, exist_ok=True)
        (self.processed_data_path / 'train').mkdir(exist_ok=True)
        (self.processed_data_path / 'val').mkdir(exist_ok=True)
        (self.processed_data_path / 'test').mkdir(exist_ok=True)
        
        logger.info(f"Preprocessor initialized - Target frames: {target_frames}")
    
    def process_single_video(self, video_path: str, label: int, 
                            save_path: str) -> bool:
        """
        Process a single video file
        
        Args:
            video_path: Path to video
            label: 0 for fake, 1 for real
            save_path: Where to save processed features
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract features
            features = process_video_to_features(
                video_path, 
                target_frames=self.target_frames,
                extract_temporal=True
            )
            
            if features is None:
                logger.warning(f"Failed to process {video_path}")
                return False
            
            # Save processed data
            np.savez_compressed(
                save_path,
                features=features,
                label=label,
                video_path=video_path
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing {video_path}: {str(e)}")
            return False
    
    def process_dataset(self, train_ratio: float = 0.7, val_ratio: float = 0.15):
        """
        Process entire dataset and split into train/val/test
        
        Args:
            train_ratio: Ratio of training data
            val_ratio: Ratio of validation data
        """
        logger.info("Starting dataset preprocessing...")
        
        # Get dataset manager
        dataset_manager = DatasetManager(self.raw_data_path)
        video_paths, labels = dataset_manager.get_video_paths()
        
        if len(video_paths) == 0:
            logger.error("No videos found in dataset!")
            return
        
        logger.info(f"Found {len(video_paths)} videos")
        logger.info(f"Real videos: {sum(labels)}, Fake videos: {len(labels) - sum(labels)}")
        
        # Split dataset
        splits = dataset_manager.split_dataset(video_paths, labels, train_ratio, val_ratio)
        
        # Process each split
        stats = {'train': 0, 'val': 0, 'test': 0}
        
        for split_name, (paths, split_labels) in splits.items():
            logger.info(f"\nProcessing {split_name} split ({len(paths)} videos)...")
            
            save_dir = self.processed_data_path / split_name
            successful = 0
            
            for idx, (video_path, label) in enumerate(tqdm(
                zip(paths, split_labels), 
                total=len(paths),
                desc=f"Processing {split_name}"
            )):
                # Create save path
                video_name = Path(video_path).stem
                save_path = save_dir / f"{video_name}.npz"
                
                # Skip if already processed
                if save_path.exists():
                    successful += 1
                    continue
                
                # Process video
                if self.process_single_video(video_path, label, str(save_path)):
                    successful += 1
            
            stats[split_name] = successful
            logger.info(f"{split_name}: Successfully processed {successful}/{len(paths)} videos")
        
        # Save dataset statistics
        self._save_statistics(stats, splits)
        
        logger.info("\n=== Preprocessing Complete ===")
        for split, count in stats.items():
            logger.info(f"{split.capitalize()}: {count} samples")
    
    def _save_statistics(self, stats: dict, splits: dict):
        """Save dataset statistics"""
        stats_file = self.processed_data_path / 'dataset_stats.json'
        
        statistics = {
            'total_videos_processed': sum(stats.values()),
            'splits': stats,
            'target_frames': self.target_frames,
            'feature_shape': f"({self.target_frames}, 468, 12)",
            'class_distribution': {}
        }
        
        # Calculate class distribution for each split
        for split_name, (_, labels) in splits.items():
            statistics['class_distribution'][split_name] = {
                'real': sum(labels),
                'fake': len(labels) - sum(labels)
            }
        
        with open(stats_file, 'w') as f:
            json.dump(statistics, f, indent=4)
        
        logger.info(f"Statistics saved to {stats_file}")


class DataLoader:
    """Load preprocessed data for training"""
    
    def __init__(self, processed_data_path: str):
        self.processed_data_path = Path(processed_data_path)
    
    def load_split(self, split: str = 'train') -> Tuple[np.ndarray, np.ndarray]:
        """
        Load a data split
        
        Args:
            split: 'train', 'val', or 'test'
            
        Returns:
            (features, labels) as numpy arrays
        """
        split_dir = self.processed_data_path / split
        
        if not split_dir.exists():
            raise ValueError(f"Split directory not found: {split_dir}")
        
        features_list = []
        labels_list = []
        
        # Load all .npz files
        npz_files = list(split_dir.glob("*.npz"))
        logger.info(f"Loading {len(npz_files)} samples from {split} split...")
        
        for npz_file in tqdm(npz_files, desc=f"Loading {split}"):
            try:
                data = np.load(npz_file)
                features_list.append(data['features'])
                labels_list.append(data['label'])
            except Exception as e:
                logger.warning(f"Failed to load {npz_file}: {str(e)}")
        
        features = np.array(features_list)
        labels = np.array(labels_list)
        
        logger.info(f"Loaded {split} - Features: {features.shape}, Labels: {labels.shape}")
        
        return features, labels
    
    def create_data_generator(self, split: str, batch_size: int = 32):
        """
        Create a data generator for memory-efficient training
        
        Args:
            split: 'train', 'val', or 'test'
            batch_size: Batch size
            
        Yields:
            (batch_features, batch_labels)
        """
        split_dir = self.processed_data_path / split
        npz_files = list(split_dir.glob("*.npz"))
        
        indices = np.arange(len(npz_files))
        np.random.shuffle(indices)
        
        for i in range(0, len(indices), batch_size):
            batch_indices = indices[i:i + batch_size]
            batch_files = [npz_files[idx] for idx in batch_indices]
            
            features_batch = []
            labels_batch = []
            
            for npz_file in batch_files:
                try:
                    data = np.load(npz_file)
                    features_batch.append(data['features'])
                    labels_batch.append(data['label'])
                except:
                    continue
            
            if len(features_batch) > 0:
                yield np.array(features_batch), np.array(labels_batch)


def download_kaggle_dataset(dataset_name: str = "unidpro/deepfake-videos-dataset", 
                            download_path: str = "./data/raw"):
    """
    Download dataset from Kaggle
    
    Args:
        dataset_name: Kaggle dataset identifier
        download_path: Where to download
    """
    try:
        import kaggle
        
        logger.info(f"Downloading dataset: {dataset_name}")
        kaggle.api.dataset_download_files(
            dataset_name, 
            path=download_path, 
            unzip=True
        )
        logger.info(f"Dataset downloaded to {download_path}")
        
    except Exception as e:
        logger.error(f"Failed to download dataset: {str(e)}")
        logger.info("Please download manually from: https://www.kaggle.com/datasets/unidpro/deepfake-videos-dataset")


if __name__ == "__main__":
    """
    Example usage:
    
    1. Download dataset (requires Kaggle API setup)
    2. Preprocess videos to extract features
    3. Save processed data for training
    """
    
    # Configuration
    RAW_DATA_PATH = "./data/raw"
    PROCESSED_DATA_PATH = "./data/processed"
    TARGET_FRAMES = 90  # 3 seconds at 30 fps
    
    print("=" * 60)
    print("DEEPFAKE DETECTION - DATA PREPROCESSING")
    print("=" * 60)
    
    # Option 1: Download dataset (uncomment if needed)
    # download_kaggle_dataset(download_path=RAW_DATA_PATH)
    
    # Option 2: Process existing dataset
    preprocessor = DataPreprocessor(
        raw_data_path=RAW_DATA_PATH,
        processed_data_path=PROCESSED_DATA_PATH,
        target_frames=TARGET_FRAMES
    )
    
    # Uncomment to run preprocessing
    preprocessor.process_dataset(train_ratio=0.7, val_ratio=0.15)
    
    print("\nPreprocessing module ready!")
    print(f"Raw data path: {RAW_DATA_PATH}")
    print(f"Processed data path: {PROCESSED_DATA_PATH}")
    print(f"Target frames per video: {TARGET_FRAMES}")  