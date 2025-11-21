"""
PreProcessor - Prepares and enriches incoming requests before routing
"""

from typing import Dict, Any, Optional
import logging
from datetime import datetime
import re

try:
    from app.services.prompt_processor import PromptProcessor
    PROMPT_PROCESSOR_AVAILABLE = True
except ImportError:
    PROMPT_PROCESSOR_AVAILABLE = False
    logging.warning("PromptProcessor not available")

logger = logging.getLogger(__name__)


class PreProcessor:
    """
    Preprocesses incoming requests:
    - Cleans and normalizes text
    - Extracts entities and keywords
    - Loads user context from Firebase
    - Enriches with session history
    """
    
    def __init__(self):
        logger.info("PreProcessor initialized")
        
        # Initialize Prompt Processor for semantic analysis
        if PROMPT_PROCESSOR_AVAILABLE:
            self.prompt_processor = PromptProcessor()
            logger.info("✅ Prompt Processor integrated")
        else:
            self.prompt_processor = None
            logger.warning("⚠️ Running without Prompt Processor")
    
    async def process(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Pre-process the incoming request
        
        Args:
            user_id: User identifier
            message: Raw user message
            session_id: Optional session identifier
            context: Additional context data
            
        Returns:
            Preprocessed data ready for routing
        """
        try:
            logger.debug(f"Pre-processing message for user {user_id}")
            
            # Step 1: Clean and normalize message
            cleaned_message = self._clean_message(message)
            
            # Step 2: Load user profile and session context
            user_profile = await self._get_user_profile(user_id)
            session_context = await self._get_session_context(session_id, user_id)
            
            # Step 3: SEMANTIC ANALYSIS using Prompt Processor (Gemini-Pro)
            semantic_analysis = None
            if self.prompt_processor:
                try:
                    semantic_analysis = await self.prompt_processor.process_chat(
                        message=cleaned_message,
                        user_id=user_id,
                        conversation_history=session_context.get("history", []),
                        user_context={
                            "role": user_profile.get("role"),
                            "location": user_profile.get("location"),
                            "preferences": user_profile.get("preferences")
                        }
                    )
                    logger.info(f"🧠 Semantic analysis complete: {semantic_analysis.get('intent')}")
                except Exception as e:
                    logger.error(f"Semantic analysis failed: {str(e)}")
                    semantic_analysis = None
            
            # Step 4: Extract entities (use semantic analysis if available, else fallback)
            if semantic_analysis and semantic_analysis.get("entities"):
                entities = semantic_analysis["entities"]
            else:
                entities = self._extract_entities(cleaned_message)
            
            # Step 5: Extract keywords
            keywords = self._extract_keywords(cleaned_message)
            
            # Step 6: Build preprocessed data with semantic analysis
            preprocessed_data = {
                "original_message": message,
                "message": cleaned_message,
                "user_id": user_id,
                "session_id": session_id,
                "user_role": user_profile.get("role", "consumer"),
                "user_profile": user_profile,
                "entities": entities,
                "keywords": keywords,
                "session_context": session_context,
                "context": context or {},
                "timestamp": datetime.utcnow().isoformat(),
                "semantic_analysis": semantic_analysis,  # NEW: Gemini-Pro semantic insights
                "metadata": {
                    "message_length": len(cleaned_message),
                    "has_entities": bool(entities),
                    "has_session": bool(session_context),
                    "has_semantic_analysis": semantic_analysis is not None,
                    "semantic_confidence": semantic_analysis.get("confidence") if semantic_analysis else None
                }
            }
            
            logger.info(
                f"Pre-processing complete for user {user_id}. "
                f"Entities: {len(entities)}, Keywords: {len(keywords)}"
            )
            
            return preprocessed_data
            
        except Exception as e:
            logger.error(f"Error in pre-processing: {str(e)}")
            # Return minimal preprocessed data on error
            return {
                "original_message": message,
                "message": message,
                "user_id": user_id,
                "session_id": session_id,
                "user_role": "consumer",
                "entities": {},
                "keywords": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _clean_message(self, message: str) -> str:
        """
        Clean and normalize the message text
        """
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', message).strip()
        
        # Remove special characters but keep common punctuation
        cleaned = re.sub(r'[^\w\s.,!?-]', '', cleaned)
        
        return cleaned
    
    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """
        Extract named entities from the message
        - Locations (cities, districts)
        - Service types
        - Price ranges
        - Time references
        """
        entities = {
            "locations": [],
            "services": [],
            "price_range": None,
            "time_references": []
        }
        
        message_lower = message.lower()
        
        # Sri Lankan locations
        sri_lankan_cities = [
            "colombo", "kandy", "galle", "jaffna", "negombo",
            "anuradhapura", "trincomalee", "batticaloa", "matara",
            "gampaha", "kurunegala", "ratnapura", "badulla", "nuwara eliya"
        ]
        
        for city in sri_lankan_cities:
            if city in message_lower:
                entities["locations"].append(city.title())
        
        # Service types
        service_types = [
            "plumber", "plumbing", "electrician", "electrical",
            "carpenter", "carpentry", "painter", "painting",
            "cleaner", "cleaning", "gardener", "gardening",
            "mechanic", "catering", "photographer", "photography",
            "tuition", "tutor"
        ]
        
        for service in service_types:
            if service in message_lower:
                entities["services"].append(service.title())
        
        # Price range extraction
        price_match = re.search(r'(rs\.?|rupees?)\s*(\d+)', message_lower)
        if price_match:
            entities["price_range"] = {
                "amount": int(price_match.group(2)),
                "currency": "LKR"
            }
        
        # Time references
        time_keywords = ["today", "tomorrow", "weekend", "urgent", "emergency", "asap"]
        for keyword in time_keywords:
            if keyword in message_lower:
                entities["time_references"].append(keyword)
        
        return entities
    
    def _extract_keywords(self, message: str) -> list:
        """
        Extract important keywords from the message
        """
        # Remove common stopwords
        stopwords = {
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
            "you", "your", "yours", "yourself", "yourselves",
            "he", "him", "his", "himself", "she", "her", "hers", "herself",
            "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
            "what", "which", "who", "whom", "this", "that", "these", "those",
            "am", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "having", "do", "does", "did", "doing",
            "a", "an", "the", "and", "but", "if", "or", "because",
            "as", "until", "while", "of", "at", "by", "for", "with",
            "about", "against", "between", "into", "through", "during",
            "before", "after", "above", "below", "to", "from", "up", "down",
            "in", "out", "on", "off", "over", "under", "again", "further",
            "then", "once", "here", "there", "when", "where", "why", "how",
            "all", "both", "each", "few", "more", "most", "other", "some",
            "such", "no", "nor", "not", "only", "own", "same", "so",
            "than", "too", "very", "can", "will", "just", "should", "now"
        }
        
        # Tokenize and filter
        words = message.lower().split()
        keywords = [
            word.strip('.,!?')
            for word in words
            if word.strip('.,!?') not in stopwords and len(word) > 2
        ]
        
        return keywords[:10]  # Return top 10 keywords
    
    async def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user profile from Firebase
        TODO: Replace with actual Firebase service call
        """
        # Stub implementation
        return {
            "user_id": user_id,
            "role": "consumer",  # or "provider"
            "location": None,
            "preferences": {}
        }
    
    async def _get_session_context(
        self,
        session_id: Optional[str],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get session context and history
        TODO: Replace with actual Firebase/State Manager call
        """
        if not session_id:
            return {}
        
        # Stub implementation
        return {
            "session_id": session_id,
            "message_count": 0,
            "last_agent": None,
            "context_data": {}
        }
