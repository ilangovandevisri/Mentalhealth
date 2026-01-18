"""
Assessment service
"""
from typing import Dict, Any

class AssessmentService:
    """Service for managing assessments"""
    
    def validate_responses(self, responses: Dict[str, Any], questionnaire: Dict) -> bool:
        """Validate assessment responses against questionnaire"""
        # Check if all required questions are answered
        required_questions = questionnaire.get("required_questions", [])
        
        for question_id in required_questions:
            if question_id not in responses:
                return False
        
        return True
    
    def calculate_raw_score(self, responses: Dict[str, Any]) -> float:
        """Calculate raw score from responses"""
        # Basic scoring: sum of all response values
        total_score = 0
        response_count = 0
        
        for key, value in responses.items():
            if isinstance(value, (int, float)):
                total_score += value
                response_count += 1
        
        if response_count == 0:
            return 0
        
        return (total_score / (response_count * 5)) * 100  # Normalize to 0-100
