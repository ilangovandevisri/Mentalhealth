"""
Database models for Mental Health Risk Detection System
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    assessments = relationship("Assessment", back_populates="user")
    risk_scores = relationship("RiskScore", back_populates="user")

class Questionnaire(Base):
    __tablename__ = "questionnaires"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    description = Column(Text)
    version = Column(String)
    questions = Column(JSON)  # Stores questions as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = relationship("Assessment", back_populates="questionnaire")

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    questionnaire_id = Column(String, ForeignKey("questionnaires.id"))
    responses = Column(JSON)  # Stores user responses
    status = Column(String, default="completed")  # completed, in_progress, cancelled
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="assessments")
    questionnaire = relationship("Questionnaire", back_populates="assessments")
    risk_score = relationship("RiskScore", uselist=False, back_populates="assessment")

class RiskScore(Base):
    __tablename__ = "risk_scores"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assessment_id = Column(String, ForeignKey("assessments.id"), unique=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    risk_level = Column(String)  # low, medium, high, critical
    risk_score = Column(Float)  # 0-100
    contributing_factors = Column(JSON)  # AI-identified factors
    recommendations = Column(JSON)  # Personalized recommendations
    ml_model_used = Column(String)  # Which ML model generated this
    confidence_score = Column(Float)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    assessment = relationship("Assessment", back_populates="risk_score")
    user = relationship("User", back_populates="risk_scores")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String)
    resource = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String)

class MentalHealthResource(Base):
    __tablename__ = "mental_health_resources"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    content = Column(Text)
    category = Column(String)  # crisis, therapy, lifestyle, coping
    embedding = Column(JSON)  # Stored embeddings for RAG
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
