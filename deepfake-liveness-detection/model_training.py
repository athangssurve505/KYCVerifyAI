"""
LSTM-based Temporal Deepfake Detection Model
Uses RNN/LSTM to analyze temporal patterns in facial landmarks
"""
import tensorflow as tf
import keras
from keras import layers, models, callbacks, ops
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import numpy as np
import logging
from pathlib import Path
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TemporalLivenessDetector:
    """LSTM-based model for deepfake detection"""
    
    def __init__(self, 
                 input_shape=(90, 468, 12),  # (frames, landmarks, features)
                 lstm_units=[128, 64],
                 dropout_rate=0.3,
                 learning_rate=0.001):
        """
        Initialize model architecture
        
        Args:
            input_shape: Shape of input features (timesteps, landmarks, features)
            lstm_units: List of LSTM layer units
            dropout_rate: Dropout rate for regularization
            learning_rate: Learning rate for optimizer
        """
        self.input_shape = input_shape
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.model = None
        self.history = None
        
        logger.info(f"Model initialized with input shape: {input_shape}")
    
    def build_model(self):
        """Build the LSTM model architecture"""
        
        # Input layer
        inputs = layers.Input(shape=self.input_shape, name='landmark_sequence')
        
        # Reshape: Flatten landmarks and features
        # From (frames, 468, 12) to (frames, 468*12)
        x = layers.Reshape((self.input_shape[0], -1))(inputs)
        
        # First LSTM layer with return sequences
        x = layers.LSTM(
            self.lstm_units[0], 
            return_sequences=True,
            name='lstm_1'
        )(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(self.dropout_rate)(x)
        
        # Second LSTM layer
        x = layers.LSTM(
            self.lstm_units[1],
            return_sequences=False,  # Only return last output
            name='lstm_2'
        )(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(self.dropout_rate)(x)
        
        # Dense layers for classification
        x = layers.Dense(64, activation='relu', name='dense_1')(x)
        x = layers.Dropout(self.dropout_rate / 2)(x)
        
        x = layers.Dense(32, activation='relu', name='dense_2')(x)
        x = layers.Dropout(self.dropout_rate / 2)(x)
        
        # Output layer (binary classification: real=1, fake=0)
        outputs = layers.Dense(1, activation='sigmoid', name='output')(x)
        
        # Create model
        self.model = models.Model(inputs=inputs, outputs=outputs, name='TemporalLivenessDetector')
        
        # Compile model
        self.model.compile(
            optimizer=Adam(learning_rate=self.learning_rate),
            loss='binary_crossentropy',
            metrics=[
                'accuracy',
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall'),
                keras.metrics.AUC(name='auc')
            ]
        )
        
        logger.info("Model built successfully!")
        return self.model
    
    def build_advanced_model(self):
        """
        Build an advanced model with bidirectional LSTM and attention
        Better for hackathon demo - higher accuracy
        """
        inputs = layers.Input(shape=self.input_shape, name='landmark_sequence')
        
        # Reshape landmarks
        x = layers.Reshape((self.input_shape[0], -1))(inputs)
        
        # Bidirectional LSTM layers (process sequence forward and backward)
        x = layers.Bidirectional(
            layers.LSTM(self.lstm_units[0], return_sequences=True),
            name='bi_lstm_1'
        )(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(self.dropout_rate)(x)
        
        x = layers.Bidirectional(
            layers.LSTM(self.lstm_units[1], return_sequences=True),
            name='bi_lstm_2'
        )(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(self.dropout_rate)(x)
        
        # Attention mechanism (focus on important temporal moments)
        attention = layers.Dense(1, activation='tanh')(x)
        attention = layers.Flatten()(attention)
        attention = layers.Activation('softmax')(attention)
        attention = layers.RepeatVector(self.lstm_units[1] * 2)(attention)  # *2 for bidirectional
        attention = layers.Permute([2, 1])(attention)
        
        # Apply attention
        x = layers.Multiply()([x, attention])
        x = layers.GlobalAveragePooling1D()(x)
        
        # Dense layers
        x = layers.Dense(64, activation='relu')(x)
        x = layers.Dropout(self.dropout_rate)(x)
        
        x = layers.Dense(32, activation='relu')(x)
        x = layers.Dropout(self.dropout_rate / 2)(x)
        
        # Output
        outputs = layers.Dense(1, activation='sigmoid', name='output')(x)
        
        # Create and compile
        self.model = models.Model(inputs=inputs, outputs=outputs, name='AdvancedLivenessDetector')
        
        self.model.compile(
            optimizer=Adam(learning_rate=self.learning_rate),
            loss='binary_crossentropy',
            metrics=['accuracy', 
                    keras.metrics.Precision(name='precision'),
                    keras.metrics.Recall(name='recall'),
                    keras.metrics.AUC(name='auc')]
        )
        
        logger.info("Advanced model with Bi-LSTM and Attention built!")
        return self.model
    
    def get_model_summary(self):
        """Print model architecture"""
        if self.model is None:
            logger.warning("Model not built yet!")
            return
        
        self.model.summary()
        
        # Count parameters
        total_params = self.model.count_params()
        logger.info(f"Total parameters: {total_params:,}")
    
    def train(self, 
              X_train, y_train,
              X_val, y_val,
              epochs=50,
              batch_size=32,
              model_save_path='./data/models/best_model.h5'):
        """
        Train the model
        
        Args:
            X_train: Training features (N, frames, landmarks, features)
            y_train: Training labels (N,)
            X_val: Validation features
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
            model_save_path: Path to save best model
            
        Returns:
            Training history
        """
        if self.model is None:
            logger.error("Model not built! Call build_model() first.")
            return None
        
        # Create callbacks
        callbacks_list = [
            # Save best model
            ModelCheckpoint(
                model_save_path,
                monitor='val_auc',
                mode='max',
                save_best_only=True,
                verbose=1
            ),
            
            # Early stopping
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Reduce learning rate on plateau
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            
            # TensorBoard logging
            callbacks.TensorBoard(
                log_dir=f'./logs/{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                histogram_freq=1
            )
        ]
        
        logger.info(f"Starting training for {epochs} epochs...")
        logger.info(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}")
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks_list,
            verbose=1
        )
        
        logger.info("Training complete!")
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set"""
        if self.model is None:
            logger.error("Model not built!")
            return None
        
        logger.info("Evaluating on test set...")
        results = self.model.evaluate(X_test, y_test, verbose=1)
        
        metrics = dict(zip(self.model.metrics_names, results))
        
        logger.info("\n=== Test Results ===")
        for metric, value in metrics.items():
            logger.info(f"{metric}: {value:.4f}")
        
        return metrics
    
    def predict(self, X):
        """Make predictions"""
        if self.model is None:
            logger.error("Model not built!")
            return None
        
        predictions = self.model.predict(X)
        return predictions
    
    def save_model(self, path):
        """Save model to file"""
        if self.model is None:
            logger.error("Model not built!")
            return
        
        self.model.save(path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path):
        """Load model from file"""
        self.model = keras.models.load_model(path)
        logger.info(f"Model loaded from {path}")


def create_baseline_cnn_lstm():
    """
    Alternative: CNN-LSTM architecture for spatial-temporal features
    Can be used as comparison baseline
    """
    inputs = layers.Input(shape=(90, 468, 12))
    
    # TimeDistributed CNN for spatial features
    x = layers.TimeDistributed(
        layers.Conv1D(64, kernel_size=3, activation='relu')
    )(inputs)
    x = layers.TimeDistributed(layers.MaxPooling1D(2))(x)
    x = layers.TimeDistributed(layers.Flatten())(x)
    
    # LSTM for temporal features
    x = layers.LSTM(128, return_sequences=True)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.LSTM(64)(x)
    x = layers.Dropout(0.3)(x)
    
    # Classification
    x = layers.Dense(32, activation='relu')(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    
    model = models.Model(inputs=inputs, outputs=outputs)
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 
                keras.metrics.Precision(),
                keras.metrics.Recall()]
    )
    
    return model


if __name__ == "__main__":
    """Test model architecture"""
    
    print("=" * 60)
    print("TEMPORAL LIVENESS DETECTOR - MODEL ARCHITECTURE")
    print("=" * 60)
    
    # Create model instance
    detector = TemporalLivenessDetector(
        input_shape=(90, 468, 12),
        lstm_units=[128, 64],
        dropout_rate=0.3
    )
    
    # Build basic model
    print("\n1. Basic LSTM Model:")
    detector.build_model()
    detector.get_model_summary()
    
    # Build advanced model
    print("\n2. Advanced Bi-LSTM + Attention Model:")
    detector_advanced = TemporalLivenessDetector()
    detector_advanced.build_advanced_model()
    detector_advanced.get_model_summary()
    
    print("\n✅ Models ready for training!")