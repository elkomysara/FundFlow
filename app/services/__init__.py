"""
ImaraFund Business Logic Services
Intelligent matching and AI advisory capabilities
"""

from app.services.intelligent_matcher import IntelligentMatcher
from app.services.gemini_service import GeminiAdvisor

__all__ = ['IntelligentMatcher', 'GeminiAdvisor']


# OLD (doesn't work):
model_attempts = [
    "gemini-1.5-flash",          
    "gemini-1.5-pro",            
    "gemini-2.0-flash-exp",      
    "gemini-pro"                 
]

# NEW (works with your API):
model_attempts = [
    "models/gemini-2.5-flash",         
    "models/gemini-2.0-flash",         
    "models/gemini-flash-latest",      
    "models/gemini-pro-latest",        
]
