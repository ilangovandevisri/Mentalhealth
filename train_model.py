"""
Machine Learning Model Training for Risk Detection
Includes Random Forest, Deep Learning, and ensemble approaches
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import json
import os
from typing import Tuple, Dict, Any

class RiskDetectionTrainer:
    """Trainer for mental health risk detection models"""
    
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = [
            "sleep_quality", "anxiety_level", "social_isolation",
            "stress_level", "physical_health", "substance_use",
            "self_harm_thoughts", "concentration", "appetite_change",
            "energy_level", "hopelessness", "irritability"
        ]
        self.model_path = "./ml/models/trained_models"
        os.makedirs(self.model_path, exist_ok=True)
    
    def generate_synthetic_data(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data"""
        X = np.random.randint(0, 11, size=(n_samples, len(self.feature_names)))
        
        # Create labels based on feature combinations
        y = []
        for sample in X:
            score = np.mean(sample)
            if score < 3:
                label = 0  # low
            elif score < 5:
                label = 1  # medium
            elif score < 7:
                label = 2  # high
            else:
                label = 3  # critical
            y.append(label)
        
        return X.astype(float), np.array(y)
    
    def train(self, X: np.ndarray = None, y: np.ndarray = None):
        """Train the models"""
        if X is None or y is None:
            print("Generating synthetic training data...")
            X, y = self.generate_synthetic_data(n_samples=2000)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        print("Training Random Forest model...")
        self.rf_model.fit(X_train_scaled, y_train)
        rf_score = self.rf_model.score(X_test_scaled, y_test)
        print(f"Random Forest Accuracy: {rf_score:.4f}")
        
        # Train Gradient Boosting
        print("Training Gradient Boosting model...")
        self.gb_model.fit(X_train_scaled, y_train)
        gb_score = self.gb_model.score(X_test_scaled, y_test)
        print(f"Gradient Boosting Accuracy: {gb_score:.4f}")
        
        # Print detailed metrics
        print("\nRandom Forest Classification Report:")
        print(classification_report(y_test, self.rf_model.predict(X_test_scaled)))
        
        # Save models
        self.save_models()
        
        return {
            "rf_accuracy": float(rf_score),
            "gb_accuracy": float(gb_score),
            "feature_importance": self._get_feature_importance()
        }
    
    def _get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from Random Forest"""
        importance_dict = {}
        for name, importance in zip(self.feature_names, self.rf_model.feature_importances_):
            importance_dict[name] = float(importance)
        return importance_dict
    
    def save_models(self):
        """Save trained models to disk"""
        joblib.dump(self.rf_model, os.path.join(self.model_path, "risk_predictor_rf.pkl"))
        joblib.dump(self.gb_model, os.path.join(self.model_path, "risk_predictor_gb.pkl"))
        joblib.dump(self.scaler, os.path.join(self.model_path, "scaler.pkl"))
        
        # Save feature importance
        with open(os.path.join(self.model_path, "feature_importance.json"), "w") as f:
            json.dump(self._get_feature_importance(), f, indent=2)
        
        print(f"✓ Models saved to {self.model_path}")

if __name__ == "__main__":
    trainer = RiskDetectionTrainer()
    metrics = trainer.train()
    print("\nTraining completed!")
    print(json.dumps(metrics, indent=2))
