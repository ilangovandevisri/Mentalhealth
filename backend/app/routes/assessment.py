"""
Assessment routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.models import Assessment, Questionnaire, User, RiskScore
from app.models.schemas import AssessmentCreate, AssessmentResponse, QuestionnaireResponse
from app.services.auth_service import AuthService
from app.services.assessment_service import AssessmentService
from app.services.ml_service import MLService

router = APIRouter()
auth_service = AuthService()
assessment_service = AssessmentService()
ml_service = MLService()

@router.get("/questionnaires", response_model=list[QuestionnaireResponse])
async def get_questionnaires(db: Session = Depends(get_db)):
    """Get all available questionnaires"""
    questionnaires = db.query(Questionnaire).all()
    return questionnaires

@router.get("/questionnaires/{questionnaire_id}", response_model=QuestionnaireResponse)
async def get_questionnaire(questionnaire_id: str, db: Session = Depends(get_db)):
    """Get specific questionnaire"""
    questionnaire = db.query(Questionnaire).filter(
        Questionnaire.id == questionnaire_id
    ).first()
    
    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )
    
    return questionnaire

@router.post("/start", response_model=AssessmentResponse)
async def start_assessment(
    questionnaire_id: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new assessment"""
    questionnaire = db.query(Questionnaire).filter(
        Questionnaire.id == questionnaire_id
    ).first()
    
    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )
    
    assessment = Assessment(
        user_id=current_user.id,
        questionnaire_id=questionnaire_id,
        responses={},
        status="in_progress"
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return assessment

@router.post("/submit")
async def submit_assessment(
    assessment: AssessmentCreate,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Submit completed assessment and calculate risk"""
    db_assessment = db.query(Assessment).filter(
        (Assessment.id == assessment.questionnaire_id) & 
        (Assessment.user_id == current_user.id)
    ).first()
    
    if not db_assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Update assessment
    db_assessment.responses = assessment.responses
    db_assessment.status = "completed"
    db_assessment.completed_at = datetime.utcnow()
    
    # Calculate risk using ML model
    risk_prediction = ml_service.predict_risk(assessment.responses)
    
    # Store risk score
    risk_score = RiskScore(
        assessment_id=db_assessment.id,
        user_id=current_user.id,
        risk_level=risk_prediction["risk_level"],
        risk_score=risk_prediction["risk_score"],
        contributing_factors=risk_prediction["contributing_factors"],
        recommendations=risk_prediction["recommendations"],
        ml_model_used=risk_prediction["model_used"],
        confidence_score=risk_prediction["confidence_score"]
    )
    
    db.add(risk_score)
    db.commit()
    db.refresh(db_assessment)
    
    return {
        "assessment_id": db_assessment.id,
        "status": "completed",
        "risk_level": risk_prediction["risk_level"],
        "risk_score": risk_prediction["risk_score"]
    }
