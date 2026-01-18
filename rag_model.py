"""
RAG (Retrieval-Augmented Generation) Model Implementation
Uses embeddings and transformers for intelligent resource retrieval
"""
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import json

class RAGModel:
    """RAG model for mental health knowledge retrieval and generation"""
    
    def __init__(self):
        # Load pre-trained models
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        self.knowledge_base = self._initialize_knowledge_base()
        self.embeddings_cache = {}
    
    def _initialize_knowledge_base(self) -> List[Dict[str, str]]:
        """Initialize knowledge base for mental health"""
        return [
            {
                "id": "kn_001",
                "title": "Depression Symptoms and Signs",
                "content": "Depression is characterized by persistent sadness, loss of interest in activities, changes in sleep patterns, fatigue, feelings of worthlessness, difficulty concentrating, and sometimes thoughts of death or suicide.",
                "category": "depression"
            },
            {
                "id": "kn_002",
                "title": "Anxiety Disorder Management",
                "content": "Anxiety disorders can be managed through cognitive-behavioral therapy, medication, lifestyle changes including regular exercise, meditation, and breathing techniques.",
                "category": "anxiety"
            },
            {
                "id": "kn_003",
                "title": "Crisis Support Resources",
                "content": "In crisis situations, contact the National Suicide Prevention Lifeline at 988 (US), Crisis Text Line by texting HOME to 741741, or go to the nearest emergency room.",
                "category": "crisis"
            },
            {
                "id": "kn_004",
                "title": "Sleep Hygiene Practices",
                "content": "Good sleep hygiene includes maintaining consistent sleep schedule, creating a dark and quiet environment, avoiding caffeine before bed, limiting screen time, and exercise regularly.",
                "category": "lifestyle"
            },
            {
                "id": "kn_005",
                "title": "Mindfulness and Meditation",
                "content": "Mindfulness meditation can help reduce anxiety and depression by focusing on the present moment, observing thoughts without judgment, and practicing regular breathing exercises.",
                "category": "coping"
            }
        ]
    
    def embed_knowledge_base(self):
        """Create embeddings for all knowledge base items"""
        for item in self.knowledge_base:
            text = f"{item['title']} {item['content']}"
            embedding = self.embedder.encode(text)
            self.embeddings_cache[item['id']] = embedding
    
    def retrieve_relevant_context(
        self,
        query: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieve most relevant documents from knowledge base"""
        if not self.embeddings_cache:
            self.embed_knowledge_base()
        
        # Encode query
        query_embedding = self.embedder.encode(query)
        
        # Calculate similarities
        similarities = {}
        for item_id, doc_embedding in self.embeddings_cache.items():
            # Cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding) + 1e-10
            )
            similarities[item_id] = similarity
        
        # Get top-k most similar
        top_items = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for item_id, score in top_items:
            for item in self.knowledge_base:
                if item['id'] == item_id:
                    results.append({
                        **item,
                        "relevance_score": float(score)
                    })
                    break
        
        return results
    
    def generate_response(
        self,
        query: str,
        context: List[Dict[str, str]]
    ) -> str:
        """Generate contextual response using retrieved documents"""
        # Prepare context
        context_text = " ".join([item['content'] for item in context])
        
        # Use QA model to generate answer
        try:
            result = self.qa_pipeline(
                question=query,
                context=context_text
            )
            return result['answer']
        except Exception as e:
            return f"Unable to generate response: {str(e)}"
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """End-to-end query processing"""
        # Retrieve relevant documents
        context = self.retrieve_relevant_context(query, top_k=3)
        
        # Generate response
        response = self.generate_response(query, context)
        
        return {
            "query": query,
            "response": response,
            "context": context,
            "model_used": "RAG with Transformers"
        }

class EmbeddingService:
    """Service for creating and managing embeddings"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def encode_text(self, text: str) -> np.ndarray:
        """Encode text to embedding"""
        return self.model.encode(text)
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Encode batch of texts"""
        return self.model.encode(texts)
    
    def similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        emb1 = self.encode_text(text1)
        emb2 = self.encode_text(text2)
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-10)
