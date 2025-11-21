"""
Mock State Manager for Demo
Manages session state and conversation context
"""

from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class StateManager:
    """Mock state manager for demonstration"""
    
    def __init__(self):
        # In-memory session storage
        self.sessions = {}
        logger.info("Mock State Manager initialized")
    
    async def get_session_state(
        self,
        session_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Get session state"""
        key = f"{user_id}_{session_id}"
        
        if key not in self.sessions:
            return {}
        
        return self.sessions[key]
    
    async def update_session_state(
        self,
        session_id: str,
        user_id: str,
        data: Dict[str, Any]
    ):
        """Update session state"""
        key = f"{user_id}_{session_id}"
        
        if key not in self.sessions:
            self.sessions[key] = {
                "created_at": datetime.utcnow().isoformat(),
                "message_count": 0
            }
        
        self.sessions[key].update(data)
        self.sessions[key]["message_count"] = self.sessions[key].get("message_count", 0) + 1
        self.sessions[key]["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Session state updated for {key}")
    
    async def clear_session(self, session_id: str, user_id: str):
        """Clear session state"""
        key = f"{user_id}_{session_id}"
        
        if key in self.sessions:
            del self.sessions[key]
            logger.info(f"Session cleared for {key}")
