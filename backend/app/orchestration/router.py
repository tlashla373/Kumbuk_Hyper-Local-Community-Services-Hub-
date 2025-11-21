"""
Agent Router - Routes requests to appropriate agent based on intent classification
"""

from typing import Dict, Any
import logging
from datetime import datetime
# from langchain.chat_models import ChatVertexAI  # Commented for demo
# from langchain.schema import HumanMessage, SystemMessage  # Commented for demo

logger = logging.getLogger(__name__)


class AgentRouter:
    """
    Routes incoming requests to the appropriate agent (Consumer or Provider)
    Based on intent classification and user role
    """
    
    def __init__(self):
        # Initialize Vertex AI for intent classification (using mock for demo)
        self.llm = None  # Mock - replace with real ChatVertexAI when ready
        # self.llm = ChatVertexAI(
        #     model_name="gemini-pro",
        #     temperature=0.3,  # Lower temperature for more deterministic routing
        #     max_output_tokens=200
        # )
        logger.info("AgentRouter initialized (mock mode)")
    
    async def route(
        self,
        preprocessed_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Determine which agent should handle the request
        
        Args:
            preprocessed_data: Pre-processed request data
            user_id: User identifier
            
        Returns:
            Routing decision with agent type and confidence
        """
        try:
            message = preprocessed_data.get("message", "")
            user_role = preprocessed_data.get("user_role", "consumer")
            context = preprocessed_data.get("context", {})
            
            # Step 1: Check user role from Firebase
            if user_role == "provider":
                # Provider users default to Provider Agent
                return self._create_routing_decision(
                    agent_type="provider",
                    confidence=1.0,
                    reason="User is a registered service provider",
                    preprocessed_data=preprocessed_data
                )
            
            # Step 2: Use LLM for intent classification
            intent_classification = await self._classify_intent(message, context)
            
            # Step 3: Make routing decision
            if intent_classification["intent"] == "service_search":
                agent_type = "consumer"
            elif intent_classification["intent"] == "business_query":
                agent_type = "provider"
            elif intent_classification["intent"] == "general":
                # Default to consumer agent for general queries
                agent_type = "consumer"
            else:
                agent_type = "consumer"  # Default fallback
            
            logger.info(
                f"Routed user {user_id} to {agent_type} agent "
                f"with intent: {intent_classification['intent']}"
            )
            
            return self._create_routing_decision(
                agent_type=agent_type,
                confidence=intent_classification["confidence"],
                reason=intent_classification["reasoning"],
                intent=intent_classification["intent"],
                preprocessed_data=preprocessed_data
            )
            
        except Exception as e:
            logger.error(f"Error in routing: {str(e)}")
            # Fallback to consumer agent on error
            return self._create_routing_decision(
                agent_type="consumer",
                confidence=0.5,
                reason=f"Fallback due to error: {str(e)}",
                preprocessed_data=preprocessed_data
            )
    
    async def _classify_intent(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use rule-based classification for intent detection (mock for demo)
        In production, this would use Vertex AI/Gemini
        
        Returns:
            Classification result with intent, confidence, and reasoning
        """
        try:
            # For demo, using fallback classification (rule-based)
            return self._fallback_classification(message)
            
            # The following code would be used when Vertex AI is integrated:
            # system_prompt = """You are an intent classifier for a local services platform in Sri Lanka.
            
            # Classify the user's message into one of these intents:
            # 1. service_search - User is looking for a service provider (plumber, electrician, etc.)
            # 2. business_query - User is asking about business operations, analytics, or provider management
            # 3. general - General questions or greetings
            
            # Respond in JSON format:
            # {
            #     "intent": "service_search|business_query|general",
            #     "confidence": 0.0-1.0,
            #     "reasoning": "Brief explanation"
            # }
            
            # Examples:
            # - "Find me a plumber in Colombo" → service_search
            # - "How is my business performing?" → business_query
            # - "Hello" → general
            # """
            
            # messages = [
            #     SystemMessage(content=system_prompt),
            #     HumanMessage(content=f"Classify this message: {message}")
            # ]
            
            # response = await self.llm.agenerate([messages])
            # result_text = response.generations[0][0].text
            
            # # Parse JSON response
            # import json
            # try:
            #     classification = json.loads(result_text)
            #     return {
            #         "intent": classification.get("intent", "general"),
            #         "confidence": float(classification.get("confidence", 0.7)),
            #         "reasoning": classification.get("reasoning", "No reasoning provided")
            #     }
            # except json.JSONDecodeError:
            #     # Fallback parsing if LLM doesn't return valid JSON
            #     return self._fallback_classification(message)
                
        except Exception as e:
            logger.error(f"Error in intent classification: {str(e)}")
            return self._fallback_classification(message)
    
    def _fallback_classification(self, message: str) -> Dict[str, Any]:
        """
        Rule-based fallback classification if LLM fails
        """
        message_lower = message.lower()
        
        # Service search keywords
        service_keywords = [
            "find", "looking for", "need", "want", "search",
            "plumber", "electrician", "carpenter", "painter",
            "service", "help with", "repair", "fix"
        ]
        
        # Business query keywords
        business_keywords = [
            "business", "analytics", "performance", "customers",
            "bookings", "revenue", "my services", "dashboard",
            "inquiries", "manage", "pricing"
        ]
        
        # Check for service search
        if any(keyword in message_lower for keyword in service_keywords):
            return {
                "intent": "service_search",
                "confidence": 0.7,
                "reasoning": "Matched service search keywords"
            }
        
        # Check for business query
        if any(keyword in message_lower for keyword in business_keywords):
            return {
                "intent": "business_query",
                "confidence": 0.7,
                "reasoning": "Matched business query keywords"
            }
        
        # Default to general
        return {
            "intent": "general",
            "confidence": 0.6,
            "reasoning": "No specific keywords matched"
        }
    
    def _create_routing_decision(
        self,
        agent_type: str,
        confidence: float,
        reason: str,
        preprocessed_data: Dict[str, Any],
        intent: str = "unknown"
    ) -> Dict[str, Any]:
        """
        Create standardized routing decision object
        """
        return {
            "agent_type": agent_type,
            "confidence": confidence,
            "reason": reason,
            "intent": intent,
            "timestamp": datetime.utcnow().isoformat(),
            "preprocessed_data": preprocessed_data,
            "routing_metadata": {
                "user_role": preprocessed_data.get("user_role"),
                "message_length": len(preprocessed_data.get("message", "")),
                "has_context": bool(preprocessed_data.get("context"))
            }
        }
