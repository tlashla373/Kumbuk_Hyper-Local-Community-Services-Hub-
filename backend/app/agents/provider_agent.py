"""
Provider Agent - Helps service providers manage their business
Mock implementation for demo
"""

from typing import Dict, Any, AsyncGenerator
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


class ProviderAgent:
    """Provider Agent for business analytics and inquiry management"""
    
    def __init__(self):
        logger.info("Provider Agent initialized")
        
        # Mock business data
        self.mock_business_data = {
            "total_inquiries": 127,
            "pending_inquiries": 8,
            "completed_jobs": 89,
            "this_month_revenue": 125000,
            "average_rating": 4.7,
            "response_rate": 92
        }
        
        self.mock_inquiries = [
            {
                "id": "inq_001",
                "customer": "Nimal Perera",
                "service": "Plumbing",
                "location": "Colombo 7",
                "status": "pending",
                "urgency": "high",
                "created": (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                "id": "inq_002",
                "customer": "Kamal Silva",
                "service": "Electrical",
                "location": "Nugegoda",
                "status": "pending",
                "urgency": "medium",
                "created": (datetime.now() - timedelta(hours=5)).isoformat()
            }
        ]
    
    async def execute(
        self,
        task_plan: Dict[str, Any],
        user_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """Execute provider agent task"""
        try:
            logger.info(f"Provider Agent executing for user {user_id}")
            
            intent = task_plan.get("intent", "general")
            preprocessed_data = task_plan.get("preprocessed_data", {})
            
            if intent == "business_query":
                return await self._handle_business_query(preprocessed_data)
            else:
                return await self._handle_general_query(preprocessed_data)
                
        except Exception as e:
            logger.error(f"Error in Provider Agent: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "I encountered an issue processing your request."
            }
    
    async def _handle_business_query(
        self,
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle business analytics queries"""
        
        message = preprocessed_data.get("message", "").lower()
        
        # Determine query type
        if any(word in message for word in ["inquiry", "inquiries", "request"]):
            return self._get_inquiry_summary()
        elif any(word in message for word in ["revenue", "earning", "income"]):
            return self._get_revenue_summary()
        elif any(word in message for word in ["rating", "review"]):
            return self._get_rating_summary()
        elif any(word in message for word in ["analytics", "dashboard", "performance"]):
            return self._get_full_analytics()
        else:
            return self._get_full_analytics()
    
    def _get_inquiry_summary(self) -> Dict[str, Any]:
        """Get inquiry summary"""
        pending = len([i for i in self.mock_inquiries if i["status"] == "pending"])
        urgent = len([i for i in self.mock_inquiries if i["urgency"] == "high"])
        
        message = f"You have {pending} pending inquiries"
        if urgent > 0:
            message += f", including {urgent} urgent request{'s' if urgent > 1 else ''}"
        message += ". "
        
        if pending > 0:
            latest = self.mock_inquiries[0]
            message += f"Latest: {latest['customer']} in {latest['location']} needs {latest['service']}."
        
        return {
            "success": True,
            "type": "inquiry_summary",
            "message": message,
            "inquiries": self.mock_inquiries[:5],
            "stats": {
                "total": self.mock_business_data["total_inquiries"],
                "pending": pending,
                "urgent": urgent
            }
        }
    
    def _get_revenue_summary(self) -> Dict[str, Any]:
        """Get revenue summary"""
        revenue = self.mock_business_data["this_month_revenue"]
        completed = self.mock_business_data["completed_jobs"]
        avg_per_job = revenue / completed if completed > 0 else 0
        
        message = f"This month, you've earned Rs. {revenue:,} from {completed} completed jobs (avg Rs. {avg_per_job:.0f} per job). "
        
        # Add trend
        last_month = revenue * random.uniform(0.85, 0.95)
        growth = ((revenue - last_month) / last_month) * 100
        
        if growth > 0:
            message += f"That's {growth:.1f}% higher than last month! 📈"
        else:
            message += f"Revenue is {abs(growth):.1f}% lower than last month."
        
        return {
            "success": True,
            "type": "revenue_summary",
            "message": message,
            "revenue": {
                "this_month": revenue,
                "last_month": int(last_month),
                "growth_percent": round(growth, 1),
                "completed_jobs": completed,
                "avg_per_job": int(avg_per_job)
            }
        }
    
    def _get_rating_summary(self) -> Dict[str, Any]:
        """Get rating summary"""
        rating = self.mock_business_data["average_rating"]
        response_rate = self.mock_business_data["response_rate"]
        
        message = f"Your current rating is ⭐ {rating}/5.0 with a {response_rate}% response rate. "
        
        if rating >= 4.5:
            message += "Excellent work! Keep maintaining this high quality service."
        elif rating >= 4.0:
            message += "Good performance! Focus on quick responses to improve further."
        else:
            message += "There's room for improvement. Consider faster responses and better communication."
        
        return {
            "success": True,
            "type": "rating_summary",
            "message": message,
            "rating": {
                "average": rating,
                "response_rate": response_rate,
                "total_reviews": 127
            },
            "tips": [
                "Respond to inquiries within 1 hour",
                "Send updates during long jobs",
                "Ask satisfied customers for reviews"
            ]
        }
    
    def _get_full_analytics(self) -> Dict[str, Any]:
        """Get full analytics dashboard"""
        message = f"Here's your business overview:\n\n"
        message += f"📊 Total Inquiries: {self.mock_business_data['total_inquiries']}\n"
        message += f"⏳ Pending: {self.mock_business_data['pending_inquiries']}\n"
        message += f"✅ Completed Jobs: {self.mock_business_data['completed_jobs']}\n"
        message += f"💰 Revenue (This Month): Rs. {self.mock_business_data['this_month_revenue']:,}\n"
        message += f"⭐ Average Rating: {self.mock_business_data['average_rating']}/5.0\n"
        message += f"📈 Response Rate: {self.mock_business_data['response_rate']}%"
        
        return {
            "success": True,
            "type": "analytics_dashboard",
            "message": message,
            "analytics": self.mock_business_data,
            "recent_inquiries": self.mock_inquiries[:3]
        }
    
    async def _handle_general_query(
        self,
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle general queries"""
        message = preprocessed_data.get("message", "").lower()
        
        if any(word in message for word in ["hello", "hi", "hey"]):
            response_text = "Hello! I'm your KumbuK business assistant. I can help you manage inquiries, track revenue, view analytics, and improve your service ratings. What would you like to know?"
        elif any(word in message for word in ["help", "how"]):
            response_text = "I can help you with:\n• View pending inquiries\n• Track revenue and earnings\n• Check your ratings and reviews\n• Get business analytics\n\nJust ask me about any of these!"
        else:
            response_text = "I'm here to help you manage your service business! Ask me about inquiries, revenue, ratings, or analytics."
        
        return {
            "success": True,
            "type": "text",
            "message": response_text,
            "suggestions": [
                "Show pending inquiries",
                "How much did I earn this month?",
                "What's my current rating?"
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
