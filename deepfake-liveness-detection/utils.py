"""
Utility functions for Temporal Liveness Detection
"""
import cv2
import numpy as np
import os
from pathlib import Path
import json
from typing import List, Tuple, Dict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoProcessor:
    """Handle video reading and frame extraction"""
    
    @staticmethod
    def extract_frames(video_path: str, max_frames: int = 720) -> List[np.ndarray]:
        """
        Extract frames from video
        
        Args:
            video_path: Path to video file
            max_frames: Maximum number of frames to extract
            
        Returns:
            List of frames as numpy arrays
        """
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        if not cap.isOpened():
            logger.error(f"Failed to open video: {video_path}")
            return frames
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        logger.info(f"Video info - Total frames: {total_frames}, FPS: {fps}")
        
        # Calculate frame indices to extract (evenly spaced)
        if total_frames > max_frames:
            frame_indices = np.linspace(0, total_frames - 1, max_frames, dtype=int)
        else:
            frame_indices = range(total_frames)
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count in frame_indices:
                frames.append(frame)
            
            frame_count += 1
            
            if len(frames) >= max_frames:
                break
        
        cap.release()
        logger.info(f"Extracted {len(frames)} frames from {video_path}")
        
        return frames
    
    @staticmethod
    def get_video_info(video_path: str) -> Dict:
        """Get video metadata"""
        cap = cv2.VideoCapture(video_path)
        
        info = {
            'fps': int(cap.get(cv2.CAP_PROP_FPS)),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration': 0
        }
        
        if info['fps'] > 0:
            info['duration'] = info['frame_count'] / info['fps']
        
        cap.release()
        return info


class DatasetManager:
    """Manage dataset paths and organization"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.real_path = self.base_path / "real"
        self.fake_path = self.base_path / "fake"
        
    def get_video_paths(self, split: str = 'train') -> Tuple[List[str], List[int]]:
        """
        Get all video paths and labels
        
        Args:
            split: 'train', 'val', or 'test'
            
        Returns:
            Tuple of (video_paths, labels)
        """
        video_paths = []
        labels = []
        
        # Real videos (label = 1)
        if self.real_path.exists():
            real_videos = list(self.real_path.glob("*.mp4"))
            video_paths.extend([str(p) for p in real_videos])
            labels.extend([1] * len(real_videos))
            logger.info(f"Found {len(real_videos)} real videos")
        
        # Fake videos (label = 0)
        if self.fake_path.exists():
            fake_videos = list(self.fake_path.glob("*.mp4"))
            video_paths.extend([str(p) for p in fake_videos])
            labels.extend([0] * len(fake_videos))
            logger.info(f"Found {len(fake_videos)} fake videos")
        
        return video_paths, labels
    
    def split_dataset(self, video_paths: List[str], labels: List[int], 
                     train_ratio: float = 0.7, val_ratio: float = 0.15):
        """Split dataset into train/val/test"""
        from sklearn.model_selection import train_test_split
        
        # First split: train+val vs test
        X_temp, X_test, y_temp, y_test = train_test_split(
            video_paths, labels, test_size=(1 - train_ratio - val_ratio), 
            random_state=42, stratify=labels
        )
        
        # Second split: train vs val
        val_size = val_ratio / (train_ratio + val_ratio)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size, 
            random_state=42, stratify=y_temp
        )
        
        logger.info(f"Dataset split - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        return {
            'train': (X_train, y_train),
            'val': (X_val, y_val),
            'test': (X_test, y_test)
        }


def normalize_landmarks(landmarks: np.ndarray) -> np.ndarray:
    """
    Normalize facial landmarks to be translation and scale invariant
    
    Args:
        landmarks: Array of shape (num_frames, 468, 3)
        
    Returns:
        Normalized landmarks
    """
    normalized = landmarks.copy()
    
    for i in range(len(landmarks)):
        # Center landmarks (translation invariance)
        centroid = np.mean(landmarks[i], axis=0)
        normalized[i] = landmarks[i] - centroid
        
        # Scale normalization
        max_dist = np.max(np.linalg.norm(normalized[i], axis=1))
        if max_dist > 0:
            normalized[i] = normalized[i] / max_dist
    
    return normalized


def compute_temporal_derivatives(landmarks: np.ndarray) -> np.ndarray:
    """
    Compute velocity, acceleration, and jerk (micro-jitter detection)
    
    Args:
        landmarks: Array of shape (num_frames, 468, 3)
        
    Returns:
        Array of shape (num_frames, 468, 9) with [x, y, z, vx, vy, vz, ax, ay, az]
    """
    num_frames, num_points, dims = landmarks.shape
    features = np.zeros((num_frames, num_points, dims * 3))
    
    # Original positions
    features[:, :, :3] = landmarks
    
    # Velocity (first derivative)
    velocity = np.zeros_like(landmarks)
    velocity[1:] = landmarks[1:] - landmarks[:-1]
    features[:, :, 3:6] = velocity
    
    # Acceleration (second derivative)
    acceleration = np.zeros_like(landmarks)
    acceleration[1:] = velocity[1:] - velocity[:-1]
    features[:, :, 6:9] = acceleration
    
    return features


def save_processed_data(data: np.ndarray, label: int, save_path: str):
    """Save processed landmarks and label"""
    np.savez_compressed(
        save_path,
        landmarks=data,
        label=label
    )


def load_processed_data(file_path: str) -> Tuple[np.ndarray, int]:
    """Load processed landmarks and label"""
    data = np.load(file_path)
    return data['landmarks'], data['label']


def create_directory_structure(base_path: str):
    """Create necessary directories for the project"""
    directories = [
        'data/raw',
        'data/processed/train',
        'data/processed/val',
        'data/processed/test',
        'data/models',
        'logs',
        'results'
    ]
    
    base = Path(base_path)
    for dir_path in directories:
        (base / dir_path).mkdir(parents=True, exist_ok=True)
    
    logger.info("Directory structure created successfully")


if __name__ == "__main__":
    # Test utilities
    print("Utility functions loaded successfully!")
    create_directory_structure("./deepfake-detection")