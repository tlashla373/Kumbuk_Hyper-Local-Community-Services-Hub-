"""
Consumer Agent - Helps consumers find local services
Mock implementation for demo
"""

from typing import Dict, Any, AsyncGenerator
import logging
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class ConsumerAgent:
    """Consumer Agent for service discovery and recommendations"""
    
    def __init__(self):
        logger.info("Consumer Agent initialized")
        
        # Mock service providers data
        self.mock_providers = [
            {
                "id": "prov_001",
                "name": "Silva Plumbing Services",
                "category": "Plumbing",
                "location": "Colombo",
                "rating": 4.8,
                "price_range": "Rs. 3000-5000",
                "available": True,
                "reviews": 127
            },
            {
                "id": "prov_002",
                "name": "Quick Fix Electricians",
                "category": "Electrical",
                "location": "Kandy",
                "rating": 4.6,
                "price_range": "Rs. 2500-4500",
                "available": True,
                "reviews": 89
            },
            {
                "id": "prov_003",
                "name": "Bright Home Painters",
                "category": "Painting",
                "location": "Galle",
                "rating": 4.9,
                "price_range": "Rs. 4000-8000",
                "available": False,
                "reviews": 156
            }
        ]
    
    async def execute(
        self,
        task_plan: Dict[str, Any],
        user_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Execute consumer agent task"""
        try:
            logger.info(f"Consumer Agent executing for user {user_id}")
            
            intent = task_plan.get("intent", "general")
            preprocessed_data = task_plan.get("preprocessed_data", {})
            entities = preprocessed_data.get("entities", {})
            
            if intent == "service_search":
                return await self._handle_service_search(entities, preprocessed_data)
            else:
                return await self._handle_general_query(preprocessed_data)
                
        except Exception as e:
            logger.error(f"Error in Consumer Agent: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "I encountered an issue processing your request."
            }
    
    async def _handle_service_search(
        self,
        entities: Dict[str, Any],
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle service search requests"""
        
        services = entities.get("services", [])
        locations = entities.get("locations", [])
        
        # Filter providers based on entities
        matching_providers = []
        for provider in self.mock_providers:
            matches = True
            
            if services and provider["category"] not in [s.title() for s in services]:
                matches = False
            
            if locations and provider["location"] not in [l.title() for l in locations]:
                matches = False
            
            if matches:
                matching_providers.append(provider)
        
        # Generate response
        if matching_providers:
            service_str = services[0] if services else "service provider"
            location_str = locations[0] if locations else "your area"
            
            message = f"I found {len(matching_providers)} {service_str}{'s' if len(matching_providers) > 1 else ''} in {location_str}. "
            
            if len(matching_providers) > 1:
                top_provider = max(matching_providers, key=lambda x: x["rating"])
                message += f"Based on ratings, I recommend {top_provider['name']} (⭐ {top_provider['rating']}, {top_provider['reviews']} reviews)."
            
            return {
                "success": True,
                "type": "service_results",
                "message": message,
                "providers": matching_providers,
                "recommendations": matching_providers[:3]
            }
        else:
            return {
                "success": True,
                "type": "text",
                "message": "I couldn't find exact matches, but I can help you explore other service providers in your area. Could you provide more details about what you're looking for?"
            }
    
    async def _handle_general_query(
        self,
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle general queries"""
        message = preprocessed_data.get("message", "")
        
        # Simple response based on keywords
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            response_text = "Hello! I'm your KumbuK assistant. I can help you find local service providers like plumbers, electricians, painters, and more. What service are you looking for?"
        elif any(word in message_lower for word in ["help", "how"]):
            response_text = "I can help you find local service providers in Sri Lanka! Just tell me what service you need and your location. For example: 'Find me a plumber in Colombo' or 'I need an electrician in Kandy'."
        else:
            response_text = "I'm here to help you find local services! You can ask me to find plumbers, electricians, painters, cleaners, and many other service providers. What do you need today?"
        
        return {
            "success": True,
            "type": "text",
            "message": response_text,
            "suggestions": [
                "Find a plumber in Colombo",
                "Show me electricians in Kandy",
                "I need a painter"
            ]
        }
    
    async def execute_stream(
        self,
        task_plan: Dict[str, Any],
        user_id: str,
        session_id: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream execution for real-time responses"""
        result = await self.execute(task_plan, user_id, session_id)
        yield result
    
    async def health_check(self) -> str:
        """Health check"""
        return "healthy"
