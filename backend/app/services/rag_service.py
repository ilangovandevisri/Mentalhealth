"""
RAG (Retrieval-Augmented Generation) Service for Mental Health Resources
Provides context-aware recommendations using embeddings and vector search
"""
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import json

class RAGService:
    """RAG service for mental health resource retrieval"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = self._load_knowledge_base()
        self.resource_embeddings = {}
        self._compute_embeddings()
    
    def _load_knowledge_base(self) -> Dict[str, List[Dict[str, str]]]:
        """Load mental health knowledge base"""
        return {
            "crisis": [
                {
                    "title": "National Suicide Prevention Lifeline",
                    "content": "24/7 support for people in suicidal crisis. Call 988 (US)",
                    "category": "crisis"
                },
                {
                    "title": "Crisis Text Line",
                    "content": "Text HOME to 741741 for free, confidential support 24/7",
                    "category": "crisis"
                }
            ],
            "therapy": [
                {
                    "title": "Cognitive Behavioral Therapy (CBT)",
                    "content": "Evidence-based therapy focusing on changing thought patterns and behaviors",
                    "category": "therapy"
                },
                {
                    "title": "Finding a Therapist",
                    "content": "Guide to finding mental health professionals and therapists in your area",
                    "category": "therapy"
                }
            ],
            "lifestyle": [
                {
                    "title": "Sleep Hygiene",
                    "content": "Tips for improving sleep quality and establishing healthy sleep patterns",
                    "category": "lifestyle"
                },
                {
                    "title": "Physical Exercise Benefits",
                    "content": "How regular exercise improves mental health and reduces anxiety",
                    "category": "lifestyle"
                },
                {
                    "title": "Nutrition for Mental Health",
                    "content": "Foods and nutrients that support mental wellbeing and mood",
                    "category": "lifestyle"
                }
            ],
            "coping": [
                {
                    "title": "Mindfulness Meditation",
                    "content": "Techniques for practicing mindfulness to reduce stress and anxiety",
                    "category": "coping"
                },
                {
                    "title": "Breathing Exercises",
                    "content": "Step-by-step breathing techniques for managing anxiety and panic",
                    "category": "coping"
                },
                {
                    "title": "Journaling for Mental Health",
                    "content": "How to use journaling as a tool for emotional processing and self-reflection",
                    "category": "coping"
                }
            ]
        }
    
    def _compute_embeddings(self):
        """Compute embeddings for all resources"""
        for category, resources in self.knowledge_base.items():
            for resource in resources:
                text = f"{resource['title']} {resource['content']}"
                embedding = self.model.encode(text)
                key = f"{category}_{resource['title']}"
                self.resource_embeddings[key] = embedding
    
    def get_relevant_resources(
        self,
        query: str,
        risk_level: str = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant resources based on query and risk level"""
        # Encode query
        query_embedding = self.model.encode(query)
        
        # Calculate similarity scores
        similarities = {}
        for key, resource_embedding in self.resource_embeddings.items():
            similarity = np.dot(query_embedding, resource_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(resource_embedding) + 1e-10
            )
            similarities[key] = similarity
        
        # Sort by similarity and get top resources
        sorted_resources = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        # Extract resources
        results = []
        for key, score in sorted_resources[:limit]:
            category = key.split('_')[0]
            for resource in self.knowledge_base[category]:
                if f"{category}_{resource['title']}" == key:
                    results.append({
                        **resource,
                        "relevance_score": float(score)
                    })
                    break
        
        return results
    
    def get_resources_by_risk_level(self, risk_level: str, limit: int = 5) -> List[Dict[str, str]]:
        """Get resources tailored to risk level"""
        risk_category_map = {
            "low": ["lifestyle", "coping"],
            "medium": ["coping", "therapy"],
            "high": ["therapy", "crisis"],
            "critical": ["crisis"]
        }
        
        categories = risk_category_map.get(risk_level, ["coping", "therapy"])
        results = []
        
        for category in categories:
            results.extend(self.knowledge_base.get(category, []))
            if len(results) >= limit:
                break
        
        return results[:limit]
