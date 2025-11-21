"""
Prompt Processor - Semantic analysis of user chat using Vertex AI Gemini-Pro
Extracts semantic meaning, intent, entities, and sentiment from user messages
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import json

try:
    from langchain_google_vertexai import ChatVertexAI
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    logging.warning(f"LangChain not available: {str(e)}. Using fallback processor.")

from app.core.config import settings

logger = logging.getLogger(__name__)


class PromptProcessor:
    """
    Advanced semantic processing of user chat messages using Vertex AI Gemini-Pro.
    Extracts:
    - Semantic intent and meaning
    - Named entities (locations, services, time, price)
    - User sentiment and urgency
    - Contextual understanding
    - Action items and next steps
    """
    
    def __init__(self):
        """Initialize the Prompt Processor with Vertex AI Gemini-Pro"""
        self.model_name = "gemini-pro"
        self.llm = None
        
        if LANGCHAIN_AVAILABLE and settings.GOOGLE_CLOUD_PROJECT:
            try:
                self.llm = ChatVertexAI(
                    model_name=self.model_name,
                    project=settings.GOOGLE_CLOUD_PROJECT,
                    location=settings.VERTEX_AI_LOCATION,
                    temperature=0.2,  # Lower temperature for more consistent analysis
                    max_output_tokens=1024,
                    top_p=0.8,
                    top_k=40
                )
                logger.info(f"✅ Prompt Processor initialized with Vertex AI {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Vertex AI: {str(e)}")
                self.llm = None
        else:
            logger.warning("⚠️ Prompt Processor running in fallback mode (no Vertex AI)")
    
    async def process_chat(
        self,
        message: str,
        user_id: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user chat message to extract semantic meaning
        
        Args:
            message: Raw user message
            user_id: User identifier
            conversation_history: Previous messages in conversation
            user_context: Additional user context (role, location, preferences)
            
        Returns:
            Semantic analysis result with intent, entities, sentiment, etc.
        """
        try:
            logger.info(f"Processing chat for user {user_id}")
            
            if self.llm:
                # Use Vertex AI Gemini-Pro for semantic analysis
                result = await self._process_with_gemini(
                    message, 
                    conversation_history, 
                    user_context
                )
            else:
                # Fallback to rule-based processing
                result = await self._process_with_fallback(
                    message,
                    user_context
                )
            
            # Add metadata
            result["user_id"] = user_id
            result["timestamp"] = datetime.utcnow().isoformat()
            result["processor"] = "gemini-pro" if self.llm else "fallback"
            
            logger.info(f"✅ Processed: Intent={result.get('intent')}, Confidence={result.get('confidence')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return await self._process_with_fallback(message, user_context)
    
    async def _process_with_gemini(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]],
        user_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process message using Vertex AI Gemini-Pro LLM
        """
        try:
            # Build context string
            context_str = self._build_context_string(conversation_history, user_context)
            
            # Create system prompt for semantic analysis
            system_prompt = self._create_semantic_analysis_prompt()
            
            # Create human message with context
            human_message_content = f"""
CONTEXT:
{context_str}

USER MESSAGE:
{message}

Please analyze this message and provide a semantic analysis in JSON format.
"""
            
            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_message_content)
            ]
            
            # Get response from Gemini-Pro
            logger.debug("Calling Vertex AI Gemini-Pro...")
            response = await self.llm.agenerate([messages])
            result_text = response.generations[0][0].text
            
            # Parse JSON response
            parsed_result = self._parse_gemini_response(result_text)
            
            # Add raw response for debugging
            parsed_result["raw_llm_response"] = result_text
            
            return parsed_result
            
        except Exception as e:
            logger.error(f"Error in Gemini processing: {str(e)}")
            raise
    
    def _create_semantic_analysis_prompt(self) -> str:
        """
        Create comprehensive system prompt for semantic analysis
        """
        return """You are a semantic analysis AI for KumbuK, a hyper-local services platform in Sri Lanka.

Your task is to analyze user messages and extract semantic meaning, intent, and entities.

ANALYZE THE MESSAGE FOR:

1. PRIMARY INTENT (choose one):
   - service_search: User looking for a service provider
   - business_query: Provider asking about business/analytics
   - inquiry_management: About managing customer inquiries
   - community_info: Asking about local events/news
   - general_conversation: Greetings, help, general questions
   - complaint_feedback: Issues or feedback

2. ENTITIES:
   - locations: Sri Lankan cities/areas (Colombo, Kandy, Galle, etc.)
   - service_types: Services needed (plumber, electrician, painter, etc.)
   - price_range: Budget or price mentions
   - time_urgency: When service is needed (today, urgent, tomorrow, etc.)
   - quality_requirements: Quality expectations (experienced, certified, best, etc.)

3. SENTIMENT:
   - positive, neutral, negative, urgent

4. URGENCY LEVEL:
   - low, medium, high, critical

5. SEMANTIC MEANING:
   - What is the user really asking for?
   - What is the underlying need?

6. SUGGESTED ACTIONS:
   - What should the system do next?

7. CONFIDENCE:
   - How confident are you in this analysis? (0.0 to 1.0)

RESPOND IN THIS JSON FORMAT:
{
    "intent": "service_search",
    "intent_confidence": 0.95,
    "semantic_meaning": "User needs an electrician in Colombo urgently",
    "entities": {
        "locations": ["Colombo"],
        "service_types": ["electrician", "electrical"],
        "price_range": {"min": 0, "max": 5000, "currency": "LKR"},
        "time_urgency": ["urgent", "today"],
        "quality_requirements": ["experienced"]
    },
    "sentiment": "neutral",
    "urgency_level": "high",
    "key_phrases": ["need electrician", "Colombo", "urgent"],
    "suggested_actions": ["search_providers", "filter_by_location", "prioritize_available"],
    "confidence": 0.90,
    "reasoning": "Clear service request with location and urgency"
}

IMPORTANT:
- For Sri Lanka context: cities include Colombo, Kandy, Galle, Negombo, Jaffna, etc.
- Services: plumber, electrician, carpenter, painter, cleaner, tutor, photographer, etc.
- Respond ONLY with valid JSON
- Be precise and accurate
"""
    
    def _build_context_string(
        self,
        conversation_history: Optional[List[Dict[str, str]]],
        user_context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build context string from conversation history and user context
        """
        context_parts = []
        
        # Add user context
        if user_context:
            role = user_context.get("role", "consumer")
            location = user_context.get("location", "Unknown")
            context_parts.append(f"User Role: {role}")
            context_parts.append(f"User Location: {location}")
        
        # Add conversation history (last 3 messages)
        if conversation_history:
            context_parts.append("\nRecent Conversation:")
            for msg in conversation_history[-3:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts) if context_parts else "No additional context"
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON response from Gemini-Pro
        """
        try:
            # Try to extract JSON from response
            # Handle cases where LLM adds extra text around JSON
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                parsed = json.loads(json_str)
                return parsed
            else:
                raise ValueError("No JSON found in response")
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            logger.debug(f"Response text: {response_text}")
            # Return fallback structure
            return {
                "intent": "general_conversation",
                "intent_confidence": 0.5,
                "semantic_meaning": "Unable to parse LLM response",
                "entities": {},
                "sentiment": "neutral",
                "urgency_level": "low",
                "confidence": 0.5,
                "error": "JSON parsing failed",
                "raw_response": response_text
            }
    
    async def _process_with_fallback(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Fallback rule-based semantic processing (when Vertex AI not available)
        """
        message_lower = message.lower()
        
        # Intent detection
        intent = "general_conversation"
        intent_confidence = 0.6
        
        service_keywords = ["find", "need", "looking for", "want", "search", "plumber", 
                          "electrician", "carpenter", "painter", "service"]
        business_keywords = ["analytics", "revenue", "earnings", "performance", 
                           "dashboard", "inquiries", "customers"]
        
        if any(kw in message_lower for kw in service_keywords):
            intent = "service_search"
            intent_confidence = 0.7
        elif any(kw in message_lower for kw in business_keywords):
            intent = "business_query"
            intent_confidence = 0.7
        
        # Entity extraction
        entities = self._extract_entities_fallback(message_lower)
        
        # Sentiment detection
        sentiment = "neutral"
        if any(w in message_lower for w in ["urgent", "emergency", "asap", "quickly", "immediately"]):
            sentiment = "urgent"
            urgency_level = "high"
        elif any(w in message_lower for w in ["please", "help", "need"]):
            urgency_level = "medium"
        else:
            urgency_level = "low"
        
        return {
            "intent": intent,
            "intent_confidence": intent_confidence,
            "semantic_meaning": f"Fallback analysis: {intent} detected",
            "entities": entities,
            "sentiment": sentiment,
            "urgency_level": urgency_level,
            "key_phrases": message_lower.split()[:5],
            "suggested_actions": ["route_to_agent"],
            "confidence": 0.6,
            "reasoning": "Fallback rule-based analysis"
        }
    
    def _extract_entities_fallback(self, message_lower: str) -> Dict[str, Any]:
        """
        Fallback entity extraction using rules
        """
        entities = {
            "locations": [],
            "service_types": [],
            "time_urgency": [],
            "quality_requirements": []
        }
        
        # Locations (Sri Lankan cities)
        cities = ["colombo", "kandy", "galle", "jaffna", "negombo", "anuradhapura", 
                 "trincomalee", "matara", "gampaha", "kurunegala"]
        entities["locations"] = [city.title() for city in cities if city in message_lower]
        
        # Services
        services = ["plumber", "plumbing", "electrician", "electrical", "carpenter", 
                   "painter", "cleaner", "tutor", "photographer"]
        entities["service_types"] = [svc.title() for svc in services if svc in message_lower]
        
        # Urgency
        urgency_words = ["urgent", "emergency", "asap", "today", "now", "quickly", "immediately"]
        entities["time_urgency"] = [word for word in urgency_words if word in message_lower]
        
        # Quality
        quality_words = ["best", "experienced", "certified", "professional", "expert", "reliable"]
        entities["quality_requirements"] = [word for word in quality_words if word in message_lower]
        
        return entities
    
    async def extract_action_items(self, semantic_result: Dict[str, Any]) -> List[str]:
        """
        Extract actionable items from semantic analysis
        """
        actions = []
        
        intent = semantic_result.get("intent", "")
        entities = semantic_result.get("entities", {})
        urgency = semantic_result.get("urgency_level", "low")
        
        if intent == "service_search":
            actions.append("search_service_providers")
            if entities.get("locations"):
                actions.append("filter_by_location")
            if urgency == "high":
                actions.append("prioritize_available_now")
        
        elif intent == "business_query":
            actions.append("fetch_business_analytics")
            actions.append("generate_insights")
        
        elif intent == "inquiry_management":
            actions.append("fetch_pending_inquiries")
        
        return actions

    async def health_check(self) -> Dict[str, Any]:
        """
        Health check for the prompt processor
        """
        return {
            "status": "healthy",
            "llm_available": self.llm is not None,
            "model": self.model_name if self.llm else "fallback",
            "langchain_available": LANGCHAIN_AVAILABLE
        }
