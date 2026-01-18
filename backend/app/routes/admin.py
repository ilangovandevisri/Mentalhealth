"""
Admin routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Questionnaire, AuditLog
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

async def check_admin(current_user: User = Depends(auth_service.get_current_user)):
    """Check if user is admin"""
    # In a real app, you'd check a role field
    if current_user.id not in ["admin_user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    return current_user

@router.post("/questionnaire/create")
async def create_questionnaire(
    name: str,
    description: str,
    questions: list,
    admin_user: User = Depends(check_admin),
    db: Session = Depends(get_db)
):
    """Create a new questionnaire"""
    questionnaire = Questionnaire(
        name=name,
        description=description,
        questions=questions,
        version="1.0"
    )
    
    db.add(questionnaire)
    db.commit()
    db.refresh(questionnaire)
    
    return questionnaire

@router.get("/audit-logs")
async def get_audit_logs(
    admin_user: User = Depends(check_admin),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get audit logs"""
    logs = db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).limit(limit).all()
    
    return {"count": len(logs), "logs": logs}
