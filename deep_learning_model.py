"""
Deep Learning models for risk detection using TensorFlow/Keras
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from typing import Tuple

class DeepLearningRiskDetector:
    """Deep Neural Network for risk detection"""
    
    def __init__(self, input_dim: int = 12):
        self.input_dim = input_dim
        self.model = self._build_model()
    
    def _build_model(self) -> keras.Model:
        """Build deep neural network"""
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=(self.input_dim,)),
            
            # Normalization layer
            layers.BatchNormalization(),
            
            # Hidden layers with dropout
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.3),
            
            layers.Dense(16, activation='relu'),
            layers.Dropout(0.2),
            
            # Output layer (4 classes: low, medium, high, critical)
            layers.Dense(4, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        return model
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray = None,
        y_val: np.ndarray = None,
        epochs: int = 50,
        batch_size: int = 32
    ) -> dict:
        """Train the deep learning model"""
        
        # Create validation split if not provided
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        # Early stopping callback
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss' if validation_data else 'loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping],
            verbose=1
        )
        
        return history.history
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions"""
        predictions = self.model.predict(X)
        class_predictions = np.argmax(predictions, axis=1)
        confidence_scores = np.max(predictions, axis=1)
        return class_predictions, confidence_scores
    
    def save(self, path: str = "./ml/models/trained_models/dl_risk_detector.h5"):
        """Save model"""
        self.model.save(path)
        print(f"Model saved to {path}")
    
    def load(self, path: str = "./ml/models/trained_models/dl_risk_detector.h5"):
        """Load model"""
        self.model = keras.models.load_model(path)
        print(f"Model loaded from {path}")

class AttentionBasedRiskDetector:
    """Attention-based model for risk detection"""
    
    def __init__(self, input_dim: int = 12, seq_length: int = 1):
        self.input_dim = input_dim
        self.seq_length = seq_length
        self.model = self._build_model()
    
    def _build_model(self) -> keras.Model:
        """Build attention-based model"""
        inputs = layers.Input(shape=(self.seq_length, self.input_dim))
        
        # Multi-head attention
        attention_output = layers.MultiHeadAttention(
            num_heads=4,
            key_dim=self.input_dim // 4
        )(inputs, inputs)
        
        attention_output = layers.LayerNormalization(epsilon=1e-6)(attention_output + inputs)
        
        # Feed-forward
        ffn_output = layers.Dense(64, activation='relu')(attention_output)
        ffn_output = layers.Dense(self.input_dim)(ffn_output)
        
        output = layers.LayerNormalization(epsilon=1e-6)(ffn_output + attention_output)
        
        # Classification head
        output = layers.GlobalAveragePooling1D()(output)
        output = layers.Dense(32, activation='relu')(output)
        output = layers.Dropout(0.2)(output)
        output = layers.Dense(4, activation='softmax')(output)
        
        model = keras.Model(inputs=inputs, outputs=output)
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        epochs: int = 50,
        batch_size: int = 32
    ):
        """Train the attention-based model"""
        # Reshape for sequence
        X_train_seq = X_train.reshape(X_train.shape[0], self.seq_length, self.input_dim)
        
        history = self.model.fit(
            X_train_seq, y_train,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        
        return history.history
