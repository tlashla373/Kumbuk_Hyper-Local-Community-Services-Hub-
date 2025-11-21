"""
Mock Firebase Service for Demo
Replace with real Firebase integration when ready
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FirebaseService:
    """Mock Firebase service for demonstration"""
    
    def __init__(self):
        # In-memory storage for demo
        self.conversations = {}
        self.users = {}
        logger.info("Mock Firebase Service initialized")
    
    async def save_conversation(
        self,
        user_id: str,
        request: str,
        response: Dict[str, Any],
        agent_type: str,
        session_id: str
    ):
        """Save conversation to mock storage"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            "request": request,
            "response": response,
            "agent_type": agent_type,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Conversation saved for user {user_id}")
    
    def send_realtime_message(self, user_id: str, message: Dict[str, Any]):
        """Mock real-time message sending"""
        logger.info(f"Realtime message sent to user {user_id}: {message.get('type')}")
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get mock user profile"""
        return {
            "user_id": user_id,
            "role": "consumer",
            "name": "Demo User",
            "location": "Colombo"
        }
    
    async def get_conversation_history(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get conversation history from mock storage"""
        if user_id not in self.conversations:
            return []
        
        conversations = self.conversations[user_id]
        
        if session_id:
            conversations = [c for c in conversations if c["session_id"] == session_id]
        
        return conversations[-limit:]
