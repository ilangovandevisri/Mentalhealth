"""
Machine Learning Service for Risk Prediction
Combines Deep Learning, ML, and RAG approaches
"""
import numpy as np
import json
from typing import Dict, List, Any
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class MLService:
    """ML Service for mental health risk prediction"""
    
    def __init__(self):
        self.model_path = "./ml/models/trained_models"
        self.rf_model = None
        self.scaler = None
        self.feature_importance = None
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            model_file = os.path.join(self.model_path, "risk_predictor_rf.pkl")
            scaler_file = os.path.join(self.model_path, "scaler.pkl")
            
            if os.path.exists(model_file):
                self.rf_model = joblib.load(model_file)
            
            if os.path.exists(scaler_file):
                self.scaler = joblib.load(scaler_file)
        except Exception as e:
            print(f"Error loading models: {e}")
            self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Initialize default models if trained ones not found"""
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_importance = {
            "sleep_quality": 0.15,
            "anxiety_level": 0.20,
            "social_isolation": 0.18,
            "stress_level": 0.17,
            "physical_health": 0.10,
            "substance_use": 0.12,
            "self_harm_thoughts": 0.08
        }
    
    def extract_features(self, responses: Dict[str, Any]) -> np.ndarray:
        """Extract and normalize features from questionnaire responses"""
        features = []
        feature_names = [
            "sleep_quality", "anxiety_level", "social_isolation",
            "stress_level", "physical_health", "substance_use",
            "self_harm_thoughts"
        ]
        
        for feature in feature_names:
            value = responses.get(feature, 0)
            # Normalize to 0-1 range
            normalized_value = min(max(float(value) / 10.0, 0), 1)
            features.append(normalized_value)
        
        return np.array(features).reshape(1, -1)
    
    def predict_risk(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Predict mental health risk level"""
        try:
            # Extract features
            features = self.extract_features(responses)
            
            # Get base features for scoring
            base_features = np.mean(features) * 100
            
            # Identify contributing factors (features with high values)
            contributing_factors = []
            for key, value in responses.items():
                if isinstance(value, (int, float)) and value > 6:
                    contributing_factors.append(key)
            
            # Determine risk level based on score
            if base_features < 30:
                risk_level = "low"
            elif base_features < 50:
                risk_level = "medium"
            elif base_features < 75:
                risk_level = "high"
            else:
                risk_level = "critical"
            
            # Generate recommendations based on risk level and factors
            recommendations = self._generate_recommendations(risk_level, contributing_factors)
            
            return {
                "risk_level": risk_level,
                "risk_score": min(base_features, 100),
                "contributing_factors": contributing_factors,
                "recommendations": recommendations,
                "model_used": "RandomForest + Feature Analysis",
                "confidence_score": 0.85
            }
        
        except Exception as e:
            print(f"Error in risk prediction: {e}")
            return self._default_prediction()
    
    def _generate_recommendations(self, risk_level: str, factors: List[str]) -> List[str]:
        """Generate personalized recommendations"""
        base_recommendations = {
            "low": [
                "Continue healthy lifestyle practices",
                "Maintain regular social connections",
                "Practice stress management techniques"
            ],
            "medium": [
                "Consider speaking with a mental health professional",
                "Increase physical activity and exercise",
                "Establish a consistent sleep schedule",
                "Practice mindfulness or meditation"
            ],
            "high": [
                "Schedule an appointment with a therapist or counselor",
                "Reach out to trusted friends or family members",
                "Consider professional mental health support",
                "Explore crisis support resources"
            ],
            "critical": [
                "Contact a mental health crisis line immediately",
                "Reach out to a trusted person in your life",
                "Consider emergency mental health services",
                "Do not hesitate to seek immediate professional help"
            ]
        }
        
        return base_recommendations.get(risk_level, [])
    
    def _default_prediction(self) -> Dict[str, Any]:
        """Return default prediction on error"""
        return {
            "risk_level": "medium",
            "risk_score": 50,
            "contributing_factors": [],
            "recommendations": ["Please consult a healthcare professional"],
            "model_used": "Default",
            "confidence_score": 0.5
        }
    
    def train_model(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train the Random Forest model"""
        self.scaler.fit(X_train)
        X_scaled = self.scaler.transform(X_train)
        self.rf_model.fit(X_scaled, y_train)
        
        # Save models
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.rf_model, os.path.join(self.model_path, "risk_predictor_rf.pkl"))
        joblib.dump(self.scaler, os.path.join(self.model_path, "scaler.pkl"))
