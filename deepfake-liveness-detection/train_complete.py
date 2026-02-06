"""
Complete Training Pipeline
End-to-end script for training the deepfake detection model
"""
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import logging
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_training import TemporalLivenessDetector
from data_preprocessing import DataLoader


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrainingPipeline:
    """Complete training pipeline"""
    
    def __init__(self, 
                 processed_data_path: str = "./data/processed",
                 model_save_dir: str = "./data/models",
                 results_dir: str = "./results"):
        
        self.processed_data_path = Path(processed_data_path)
        self.model_save_dir = Path(model_save_dir)
        self.results_dir = Path(results_dir)
        
        # Create directories
        self.model_save_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_loader = DataLoader(processed_data_path)
        self.model = None
        self.history = None
        
    def load_data(self):
        """Load preprocessed data"""
        logger.info("Loading preprocessed data...")
        
        # Load all splits
        self.X_train, self.y_train = self.data_loader.load_split('train')
        self.X_val, self.y_val = self.data_loader.load_split('val')
        self.X_test, self.y_test = self.data_loader.load_split('test')
        
        logger.info("Data loaded successfully!")
        logger.info(f"Training set: {self.X_train.shape}")
        logger.info(f"Validation set: {self.X_val.shape}")
        logger.info(f"Test set: {self.X_test.shape}")
        
        # Check class distribution
        logger.info(f"\nClass distribution:")
        logger.info(f"Train - Real: {np.sum(self.y_train)}, Fake: {len(self.y_train) - np.sum(self.y_train)}")
        logger.info(f"Val - Real: {np.sum(self.y_val)}, Fake: {len(self.y_val) - np.sum(self.y_val)}")
        logger.info(f"Test - Real: {np.sum(self.y_test)}, Fake: {len(self.y_test) - np.sum(self.y_test)}")
    
    def create_model(self, model_type='advanced'):
        """
        Create model
        
        Args:
            model_type: 'basic' or 'advanced' (with attention)
        """
        logger.info(f"Creating {model_type} model...")
        
        input_shape = self.X_train.shape[1:]  # (frames, landmarks, features)
        
        self.model = TemporalLivenessDetector(
            input_shape=input_shape,
            lstm_units=[128, 64],
            dropout_rate=0.3,
            learning_rate=0.001
        )
        
        if model_type == 'advanced':
            self.model.build_advanced_model()
        else:
            self.model.build_model()
        
        self.model.get_model_summary()
    
    def train_model(self, epochs=40, batch_size=32):
        """Train the model"""
        logger.info("Starting training...")
        
        model_save_path = self.model_save_dir / "best_model.h5"
        
        self.history = self.model.train(
            self.X_train, self.y_train,
            self.X_val, self.y_val,
            epochs=epochs,
            batch_size=batch_size,
            model_save_path=str(model_save_path)
        )
        
        logger.info("Training complete!")
    
    def evaluate_model(self):
        """Evaluate model on test set"""
        logger.info("Evaluating model on test set...")
        
        import numpy as np
        from sklearn.metrics import confusion_matrix, classification_report
        
        # Get predictions
        y_pred_proba = self.model.predict(self.X_test)
        y_pred = (y_pred_proba >= 0.5).astype(int).flatten()
        # Keras evaluation
        test_metrics = self.model.evaluate(self.X_test, self.y_test)
        
        # Detect how many classes are present
        unique_labels = np.unique(self.y_test)
        
        # Confusion matrix (force 2x2 shape)
        cm = confusion_matrix(self.y_test, y_pred, labels=[0, 1])
        
        # Classification report (handle single-class case)
        if len(unique_labels) < 2:
            logger.warning(
                "Only one class present in test set. "
                "Classification report will be limited."
            )
            
            report = {
                "note": "Only one class present in test set. "
                        "Precision/Recall/F1 are not meaningful.",
                "present_class": int(unique_labels[0]),
                "accuracy": float(test_metrics[1])
            }
        else:
            report = classification_report(
                self.y_test,
                y_pred,
                labels=[0, 1],
                target_names=["Fake", "Real"],
                output_dict=True,
                zero_division=0
            )
        
        # Save results
        results = {
            "test_metrics": {
                name: float(value)
                for name, value in zip(self.model.metrics_names, test_metrics)
            },
            "confusion_matrix": cm.tolist(),
            "classification_report": report
        }
        
        results_file = self.results_dir / "evaluation_results.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=4)
        
        logger.info(f"Results saved to {results_file}")
        
        return results

    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            logger.warning("No training history available!")
            return
        
        history_dict = self.history.history
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Training History', fontsize=16)
        
        # Accuracy
        axes[0, 0].plot(history_dict['accuracy'], label='Train')
        axes[0, 0].plot(history_dict['val_accuracy'], label='Validation')
        axes[0, 0].set_title('Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(history_dict['loss'], label='Train')
        axes[0, 1].plot(history_dict['val_loss'], label='Validation')
        axes[0, 1].set_title('Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        axes[1, 0].plot(history_dict['precision'], label='Train')
        axes[1, 0].plot(history_dict['val_precision'], label='Validation')
        axes[1, 0].set_title('Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Recall
        axes[1, 1].plot(history_dict['recall'], label='Train')
        axes[1, 1].plot(history_dict['val_recall'], label='Validation')
        axes[1, 1].set_title('Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        save_path = self.results_dir / 'training_history.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Training history plot saved to {save_path}")
        
        plt.show()
    
    def plot_confusion_matrix(self, cm):
        """Plot confusion matrix"""
        plt.figure(figsize=(8, 6))
        
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=['Fake', 'Real'],
            yticklabels=['Fake', 'Real']
        )
        
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        save_path = self.results_dir / 'confusion_matrix.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Confusion matrix saved to {save_path}")
        
        plt.show()
    
    def plot_roc_curve(self):
        """Plot ROC curve"""
        y_pred_proba = self.model.predict(self.X_test)
        
        fpr, tpr, thresholds = roc_curve(self.y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(True)
        
        save_path = self.results_dir / 'roc_curve.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"ROC curve saved to {save_path}")
        
        plt.show()
    
    def run_complete_pipeline(self, 
                             model_type='advanced',
                             epochs=40, 
                             batch_size=32):
        """
        Run complete training and evaluation pipeline
        
        Args:
            model_type: 'basic' or 'advanced'
            epochs: Number of training epochs
            batch_size: Batch size
        """
        print("=" * 70)
        print("DEEPFAKE DETECTION - COMPLETE TRAINING PIPELINE")
        print("=" * 70)
        
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Create model
        self.create_model(model_type=model_type)
        
        # Step 3: Train model
        self.train_model(epochs=epochs, batch_size=batch_size)
        
        # Step 4: Evaluate model
        results = self.evaluate_model()
        
        # Step 5: Visualizations
        print("\nGenerating visualizations...")
        self.plot_training_history()
        self.plot_confusion_matrix(np.array(results['confusion_matrix']))
        self.plot_roc_curve()
        
        # Print final results
        print("\n" + "=" * 70)
        print("FINAL RESULTS")
        print("=" * 70)
        
        report = results['classification_report']
        print(f"\nAccuracy: {report['accuracy']:.4f}")
        print(f"\nFake Detection:")
        print(f"  Precision: {report['Fake']['precision']:.4f}")
        print(f"  Recall: {report['Fake']['recall']:.4f}")
        print(f"  F1-Score: {report['Fake']['f1-score']:.4f}")
        print(f"\nReal Detection:")
        print(f"  Precision: {report['Real']['precision']:.4f}")
        print(f"  Recall: {report['Real']['recall']:.4f}")
        print(f"  F1-Score: {report['Real']['f1-score']:.4f}")
        
        print("\n✅ Training pipeline complete!")
        print(f"Model saved to: {self.model_save_dir / 'best_model.h5'}")
        print(f"Results saved to: {self.results_dir}")


if __name__ == "__main__":
    """
    Main training script
    
    Usage:
        python train_complete.py
    """
    
    # Configuration
    PROCESSED_DATA_PATH = "./data/processed"
    MODEL_SAVE_DIR = "./data/models"
    RESULTS_DIR = "./results"
    
    # Training hyperparameters
    MODEL_TYPE = 'advanced'  # 'basic' or 'advanced'
    EPOCHS = 20
    BATCH_SIZE = 32
    
    # Create pipeline
    pipeline = TrainingPipeline(
        processed_data_path=PROCESSED_DATA_PATH,
        model_save_dir=MODEL_SAVE_DIR,
        results_dir=RESULTS_DIR
    )
    
    # Run complete pipeline
    pipeline.run_complete_pipeline(
        model_type=MODEL_TYPE,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE
    )