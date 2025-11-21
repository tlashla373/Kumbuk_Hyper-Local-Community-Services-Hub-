"""
FastAPI Routes for Orchestration Layer
Main API endpoints for the AI agent system
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import json
from datetime import datetime

from app.orchestration.bedrock_aggregator import BedrockAggregator
# from app.core.auth import get_current_user  # Commented out for now - implement auth later

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# Temporary stub for authentication - replace with real auth later
async def get_current_user() -> str:
    """Stub function for authentication - returns a test user ID"""
    return "test_user_123"

# Initialize orchestrator
orchestrator = BedrockAggregator()


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool
    request_id: str
    response: Dict[str, Any]
    agent_type: str
    timestamp: str
    session_id: str


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Send a message to the AI agent system
    
    Flow:
    1. Receives user message
    2. Routes through orchestration layer
    3. Returns agent response
    """
    try:
        logger.info(f"Received message from user {user_id}")
        
        # Process through orchestration layer
        result = await orchestrator.process_request(
            user_id=user_id,
            message=request.message,
            session_id=request.session_id,
            context=request.context
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Processing failed")
            )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time chat
    
    Provides streaming responses for better UX
    """
    await websocket.accept()
    logger.info(f"WebSocket connection established for user {user_id}")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            logger.debug(f"WebSocket message from {user_id}: {message_data}")
            
            # Send acknowledgment
            await websocket.send_json({
                "type": "ack",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Process through orchestration layer
            result = await orchestrator.process_request(
                user_id=user_id,
                message=message_data.get("message", ""),
                session_id=message_data.get("session_id"),
                context=message_data.get("context")
            )
            
            # Send response
            await websocket.send_json({
                "type": "response",
                "data": result,
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        except:
            pass


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    user_id: str = Depends(get_current_user)
):
    """
    Get session context and history
    """
    try:
        context = await orchestrator.get_session_context(session_id, user_id)
        return {
            "success": True,
            "session": context
        }
    except Exception as e:
        logger.error(f"Error getting session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/session/{session_id}")
async def clear_session(
    session_id: str,
    user_id: str = Depends(get_current_user)
):
    """
    Clear session data
    """
    try:
        success = await orchestrator.clear_session(session_id, user_id)
        return {
            "success": success,
            "message": "Session cleared" if success else "Failed to clear session"
        }
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/stream")
async def stream_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Stream responses in real-time
    Uses Server-Sent Events (SSE)
    """
    async def event_generator():
        try:
            # This will be implemented with Firebase Realtime Database
            await orchestrator.stream_response(
                user_id=user_id,
                message=request.message,
                session_id=request.session_id
            )
            
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for orchestration layer
    """
    try:
        # Check orchestrator health
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "orchestrator": "ok",
                "router": "ok",
                "preprocessor": "ok",
                "task_planner": "ok",
                "dispatcher": "ok"
            }
        }
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
