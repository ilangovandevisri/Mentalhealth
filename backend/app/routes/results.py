"""
Results routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import RiskScore, Assessment, User
from app.models.schemas import RiskScoreResponse
from app.services.auth_service import AuthService
from app.services.rag_service import RAGService

router = APIRouter()
auth_service = AuthService()
rag_service = RAGService()

@router.get("/assessment/{assessment_id}", response_model=RiskScoreResponse)
async def get_risk_score(
    assessment_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk assessment results"""
    risk_score = db.query(RiskScore).filter(
        (RiskScore.assessment_id == assessment_id) &
        (RiskScore.user_id == current_user.id)
    ).first()
    
    if not risk_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found"
        )
    
    return risk_score

@router.get("/user/latest")
async def get_latest_assessment(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's latest risk assessment"""
    risk_score = db.query(RiskScore).filter(
        RiskScore.user_id == current_user.id
    ).order_by(RiskScore.calculated_at.desc()).first()
    
    if not risk_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessments found"
        )
    
    return risk_score

@router.get("/user/history")
async def get_assessment_history(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get user's assessment history"""
    assessments = db.query(Assessment).filter(
        Assessment.user_id == current_user.id
    ).order_by(Assessment.completed_at.desc()).limit(limit).all()
    
    return {
        "count": len(assessments),
        "assessments": assessments
    }

@router.get("/resources/{risk_level}")
async def get_personalized_resources(
    risk_level: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized mental health resources based on risk level"""
    resources = rag_service.get_relevant_resources(risk_level, limit=5)
    
    return {
        "risk_level": risk_level,
        "resources": resources
    }
