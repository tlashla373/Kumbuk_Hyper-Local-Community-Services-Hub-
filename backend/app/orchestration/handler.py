"""
Request Handler - Handles and formats agent responses
"""

from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RequestHandler:
    """
    Handles agent responses and formats them for frontend consumption
    Manages error handling and response enrichment
    """
    
    def __init__(self):
        logger.info("RequestHandler initialized")
    
    async def handle_response(
        self,
        agent_response: Dict[str, Any],
        routing_decision: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Handle and format agent response
        
        Args:
            agent_response: Raw response from agent
            routing_decision: Original routing decision
            user_id: User identifier
            
        Returns:
            Formatted response ready for frontend
        """
        try:
            logger.debug(f"Handling response for user {user_id}")
            
            # Extract response components
            success = agent_response.get("success", True)
            
            if not success:
                return await self.handle_error(
                    error=agent_response.get("error", "Unknown error"),
                    user_id=user_id,
                    message=""
                )
            
            # Format based on agent type
            agent_type = routing_decision["agent_type"]
            
            if agent_type == "consumer":
                formatted_response = await self._format_consumer_response(agent_response)
            elif agent_type == "provider":
                formatted_response = await self._format_provider_response(agent_response)
            else:
                formatted_response = await self._format_default_response(agent_response)
            
            # Add metadata
            formatted_response["metadata"] = {
                "agent_type": agent_type,
                "confidence": routing_decision.get("confidence", 1.0),
                "intent": routing_decision.get("intent", "unknown"),
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id
            }
            
            # Add execution info if available
            if "execution_metadata" in agent_response:
                formatted_response["execution_info"] = agent_response["execution_metadata"]
            
            logger.info(f"Response formatted successfully for user {user_id}")
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error handling response: {str(e)}")
            return await self.handle_error(e, user_id, "")
    
    async def _format_consumer_response(
        self,
        agent_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format response from Consumer Agent
        """
        response_type = agent_response.get("type", "text")
        
        if response_type == "service_results":
            # Format service provider results
            return {
                "type": "service_results",
                "message": agent_response.get("message", ""),
                "providers": agent_response.get("providers", []),
                "total_count": len(agent_response.get("providers", [])),
                "filters_applied": agent_response.get("filters", {}),
                "recommendations": agent_response.get("recommendations", []),
                "actions": [
                    {
                        "type": "view_provider",
                        "label": "View Details"
                    },
                    {
                        "type": "create_inquiry",
                        "label": "Send Inquiry"
                    }
                ]
            }
        
        elif response_type == "recommendation":
            # Format recommendations
            return {
                "type": "recommendation",
                "message": agent_response.get("message", ""),
                "recommendations": agent_response.get("recommendations", []),
                "reasoning": agent_response.get("reasoning", ""),
                "actions": [
                    {
                        "type": "view_details",
                        "label": "Learn More"
                    }
                ]
            }
        
        else:
            # Default text response
            return {
                "type": "text",
                "message": agent_response.get("message", agent_response.get("response", "")),
                "data": agent_response.get("data"),
                "suggestions": agent_response.get("suggestions", [])
            }
    
    async def _format_provider_response(
        self,
        agent_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format response from Provider Agent
        """
        response_type = agent_response.get("type", "text")
        
        if response_type == "business_analytics":
            # Format business analytics
            return {
                "type": "business_analytics",
                "message": agent_response.get("message", ""),
                "metrics": agent_response.get("metrics", {}),
                "insights": agent_response.get("insights", []),
                "trends": agent_response.get("trends", []),
                "recommendations": agent_response.get("recommendations", []),
                "chart_data": agent_response.get("chart_data"),
                "actions": [
                    {
                        "type": "view_dashboard",
                        "label": "Open Dashboard"
                    },
                    {
                        "type": "export_report",
                        "label": "Export Report"
                    }
                ]
            }
        
        elif response_type == "inquiry_management":
            # Format inquiry-related responses
            return {
                "type": "inquiry_management",
                "message": agent_response.get("message", ""),
                "inquiries": agent_response.get("inquiries", []),
                "pending_count": agent_response.get("pending_count", 0),
                "actions": [
                    {
                        "type": "respond_inquiry",
                        "label": "Respond"
                    },
                    {
                        "type": "view_details",
                        "label": "View Details"
                    }
                ]
            }
        
        else:
            # Default text response
            return {
                "type": "text",
                "message": agent_response.get("message", agent_response.get("response", "")),
                "data": agent_response.get("data"),
                "suggestions": agent_response.get("suggestions", [])
            }
    
    async def _format_default_response(
        self,
        agent_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format default response
        """
        return {
            "type": "text",
            "message": agent_response.get("message", agent_response.get("response", "I'm here to help!")),
            "data": agent_response.get("data"),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def handle_error(
        self,
        error: Exception,
        user_id: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Handle and format error responses
        """
        logger.error(f"Handling error for user {user_id}: {str(error)}")
        
        error_message = str(error)
        
        # Determine error type and user-friendly message
        if "timeout" in error_message.lower():
            user_message = "I'm taking a bit longer than expected. Please try again."
            error_type = "timeout"
        elif "authentication" in error_message.lower():
            user_message = "There was an authentication issue. Please log in again."
            error_type = "authentication"
        elif "not found" in error_message.lower():
            user_message = "I couldn't find what you're looking for. Could you provide more details?"
            error_type = "not_found"
        else:
            user_message = "I encountered an issue processing your request. Please try again or rephrase your question."
            error_type = "general"
        
        return {
            "type": "error",
            "message": user_message,
            "error_type": error_type,
            "error_details": error_message if logger.level == logging.DEBUG else None,
            "suggestions": [
                "Try rephrasing your question",
                "Check your internet connection",
                "Contact support if the issue persists"
            ],
            "timestamp": datetime.utcnow().isoformat(),
            "actions": [
                {
                    "type": "retry",
                    "label": "Try Again"
                },
                {
                    "type": "contact_support",
                    "label": "Contact Support"
                }
            ]
        }
