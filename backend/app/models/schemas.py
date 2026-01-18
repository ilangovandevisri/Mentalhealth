"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    age: int
    gender: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    age: int
    gender: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Assessment Schemas
class QuestionnaireResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    questions: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True

class AssessmentResponse(BaseModel):
    id: str
    responses: Dict[str, Any]
    status: str
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class AssessmentCreate(BaseModel):
    questionnaire_id: str
    responses: Dict[str, Any]

# Risk Score Schemas
class RiskScoreResponse(BaseModel):
    id: str
    risk_level: str
    risk_score: float
    contributing_factors: List[str]
    recommendations: List[str]
    ml_model_used: str
    confidence_score: float
    calculated_at: datetime
    
    class Config:
        from_attributes = True

# Resource Schemas
class MentalHealthResourceResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    
    class Config:
        from_attributes = True
