"""
Database initialization and seed data
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base
from app.models.models import Questionnaire

def init_db():
    """Initialize database with tables and seed data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Add seed data
    db = SessionLocal()
    
    # Create default PHQ-9 questionnaire
    phq9_questions = [
        {
            "id": "q1",
            "text": "Little interest or pleasure in doing things",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q2",
            "text": "Feeling down, depressed, or hopeless",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q3",
            "text": "Trouble falling or staying asleep, or sleeping too much",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q4",
            "text": "Feeling tired or having little energy",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q5",
            "text": "Poor appetite or overeating",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q6",
            "text": "Feeling bad about yourself or feeling like a failure",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q7",
            "text": "Trouble concentrating on things",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q8",
            "text": "Moving or speaking so slowly or restlessly",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        },
        {
            "id": "q9",
            "text": "Thoughts that you would be better off dead",
            "type": "rating",
            "scale": [0, 3, 6, 9],
            "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
        }
    ]
    
    phq9 = Questionnaire(
        name="PHQ-9 Depression Screening",
        description="Patient Health Questionnaire-9 for depression severity assessment",
        version="1.0",
        questions=phq9_questions
    )
    
    db.add(phq9)
    
    # Create GAD-7 questionnaire
    gad7_questions = [
        {
            "id": "g1",
            "text": "Feeling nervous, anxious, or on edge",
            "type": "rating",
            "scale": [0, 1, 2, 3],
            "labels": ["Not at all", "Several days", "More than half", "Nearly every day"]
        },
        {
            "id": "g2",
            "text": "Not being able to stop or control worrying",
            "type": "rating",
            "scale": [0, 1, 2, 3],
            "labels": ["Not at all", "Several days", "More than half", "Nearly every day"]
        },
        {
            "id": "g3",
            "text": "Worrying too much about different things",
            "type": "rating",
            "scale": [0, 1, 2, 3],
            "labels": ["Not at all", "Several days", "More than half", "Nearly every day"]
        },
        {
            "id": "g4",
            "text": "Trouble relaxing",
            "type": "rating",
            "scale": [0, 1, 2, 3],
            "labels": ["Not at all", "Several days", "More than half", "Nearly every day"]
        },
        {
            "id": "g5",
            "text": "Being so restless that it is hard to sit still",
            "type": "rating",
            "scale": [0, 1, 2, 3],
            "labels": ["Not at all", "Several days", "More than half", "Nearly every day"]
        },
        {
            "id": "g6",
            "text": "Becoming easily annoyed or irritable",
            "type": "rating",
            "scale": [0, 1, 2, 3],
            "labels": ["Not at all", "Several days", "More than half", "Nearly every day"]
        },
        {
            "id": "g7",
            "text": "Feeling afraid as if something awful might happen",
            "type": "rating",
            "scale": [0, 1, 2, 3],
            "labels": ["Not at all", "Several days", "More than half", "Nearly every day"]
        }
    ]
    
    gad7 = Questionnaire(
        name="GAD-7 Anxiety Screening",
        description="Generalized Anxiety Disorder-7 for anxiety severity assessment",
        version="1.0",
        questions=gad7_questions
    )
    
    db.add(gad7)
    db.commit()
    print("✓ Seed questionnaires added")
    db.close()

if __name__ == "__main__":
    init_db()
    print("✓ Database initialization complete!")
