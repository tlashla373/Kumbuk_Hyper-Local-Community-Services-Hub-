"""
BedRock Aggregator - Main entry point for orchestration layer
Aggregates requests from frontend and coordinates the entire agent workflow
"""

from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging
from ..core.config import settings
from .router import AgentRouter
from .handler import RequestHandler
from .preprocessor import PreProcessor
from .task_planner import TaskPlanner
from .dispatcher import AgentDispatcher
from ..services.firebase_service import FirebaseService
from ..services.state_manager import StateManager

logger = logging.getLogger(__name__)


class BedrockAggregator:
    """
    Central orchestrator that aggregates and manages all agent interactions
    Following the architecture diagram flow
    """
    
    def __init__(self):
        self.router = AgentRouter()
        self.handler = RequestHandler()
        self.preprocessor = PreProcessor()
        self.task_planner = TaskPlanner()
        self.dispatcher = AgentDispatcher()
        self.firebase_service = FirebaseService()
        self.state_manager = StateManager()
        
        logger.info("BedrockAggregator initialized successfully")
    
    async def process_request(
        self, 
        user_id: str, 
        message: str, 
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main orchestration flow:
        1. Pre-process the request
        2. Route to appropriate agent
        3. Plan tasks
        4. Dispatch to agent
        5. Handle response
        6. Return aggregated result
        
        Args:
            user_id: User identifier
            message: User's input message
            session_id: Optional session identifier
            context: Additional context data
            
        Returns:
            Aggregated response from the agent system
        """
        try:
            request_id = f"{user_id}_{datetime.utcnow().timestamp()}"
            logger.info(f"Processing request {request_id} for user {user_id}")
            
            # Step 1: Pre-process the request
            logger.debug("Step 1: Pre-processing request")
            preprocessed_data = await self.preprocessor.process(
                user_id=user_id,
                message=message,
                session_id=session_id,
                context=context or {}
            )
            
            # Step 2: Route to appropriate agent type
            logger.debug("Step 2: Routing to agent")
            routing_decision = await self.router.route(
                preprocessed_data=preprocessed_data,
                user_id=user_id
            )
            
            # Step 3: Create task plan
            logger.debug("Step 3: Planning tasks")
            task_plan = await self.task_planner.create_plan(
                routing_decision=routing_decision,
                preprocessed_data=preprocessed_data
            )
            
            # Step 4: Dispatch to agent
            logger.debug("Step 4: Dispatching to agent")
            agent_response = await self.dispatcher.dispatch(
                task_plan=task_plan,
                agent_type=routing_decision["agent_type"],
                user_id=user_id,
                session_id=session_id or request_id
            )
            
            # Step 5: Handle and format response
            logger.debug("Step 5: Handling response")
            final_response = await self.handler.handle_response(
                agent_response=agent_response,
                routing_decision=routing_decision,
                user_id=user_id
            )
            
            # Step 6: Save to Firebase Realtime DB
            logger.debug("Step 6: Saving to Firebase")
            await self.firebase_service.save_conversation(
                user_id=user_id,
                request=message,
                response=final_response,
                agent_type=routing_decision["agent_type"],
                session_id=session_id or request_id
            )
            
            # Step 7: Update state
            await self.state_manager.update_session_state(
                session_id=session_id or request_id,
                user_id=user_id,
                data={
                    "last_agent": routing_decision["agent_type"],
                    "last_message": message,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
            logger.info(f"Request {request_id} processed successfully")
            
            return {
                "success": True,
                "request_id": request_id,
                "response": final_response,
                "agent_type": routing_decision["agent_type"],
                "timestamp": datetime.utcnow().isoformat(),
                "session_id": session_id or request_id
            }
            
        except Exception as e:
            logger.error(f"Error processing request for user {user_id}: {str(e)}", exc_info=True)
            
            # Error handling
            error_response = await self.handler.handle_error(
                error=e,
                user_id=user_id,
                message=message
            )
            
            return {
                "success": False,
                "error": str(e),
                "error_response": error_response,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def stream_response(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str] = None
    ):
        """
        Stream responses in real-time for better UX
        Uses Firebase Realtime Database for live updates
        """
        try:
            request_id = f"{user_id}_{datetime.utcnow().timestamp()}"
            
            # Send initial status
            await self.firebase_service.send_realtime_message(
                user_id=user_id,
                message={
                    "type": "status",
                    "status": "processing",
                    "request_id": request_id
                }
            )
            
            # Process with streaming
            preprocessed_data = await self.preprocessor.process(user_id, message, session_id)
            
            await self.firebase_service.send_realtime_message(
                user_id=user_id,
                message={"type": "status", "status": "routing"}
            )
            
            routing_decision = await self.router.route(preprocessed_data, user_id)
            
            await self.firebase_service.send_realtime_message(
                user_id=user_id,
                message={
                    "type": "status",
                    "status": "agent_processing",
                    "agent_type": routing_decision["agent_type"]
                }
            )
            
            # Continue with task planning and execution
            task_plan = await self.task_planner.create_plan(routing_decision, preprocessed_data)
            
            # Dispatch and stream response
            async for chunk in self.dispatcher.dispatch_stream(
                task_plan=task_plan,
                agent_type=routing_decision["agent_type"],
                user_id=user_id,
                session_id=session_id or request_id
            ):
                await self.firebase_service.send_realtime_message(
                    user_id=user_id,
                    message={
                        "type": "response_chunk",
                        "chunk": chunk,
                        "agent_type": routing_decision["agent_type"]
                    }
                )
            
            # Send completion
            await self.firebase_service.send_realtime_message(
                user_id=user_id,
                message={
                    "type": "status",
                    "status": "completed",
                    "request_id": request_id
                }
            )
            
        except Exception as e:
            logger.error(f"Error in streaming response: {str(e)}")
            await self.firebase_service.send_realtime_message(
                user_id=user_id,
                message={
                    "type": "error",
                    "error": str(e)
                }
            )
    
    async def get_session_context(self, session_id: str, user_id: str) -> Dict[str, Any]:
        """Get current session context and history"""
        try:
            state = await self.state_manager.get_session_state(session_id, user_id)
            history = await self.firebase_service.get_conversation_history(user_id, session_id)
            
            return {
                "state": state,
                "history": history,
                "session_id": session_id
            }
        except Exception as e:
            logger.error(f"Error getting session context: {str(e)}")
            return {"error": str(e)}
    
    async def clear_session(self, session_id: str, user_id: str) -> bool:
        """Clear session data"""
        try:
            await self.state_manager.clear_session(session_id, user_id)
            logger.info(f"Session {session_id} cleared for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error clearing session: {str(e)}")
            return False
