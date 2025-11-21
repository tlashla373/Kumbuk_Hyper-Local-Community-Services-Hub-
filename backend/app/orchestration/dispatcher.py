"""
Agent Dispatcher - Dispatches tasks to appropriate specialized agents
"""

from typing import Dict, Any, AsyncGenerator
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentDispatcher:
    """
    Dispatches tasks to specialized agents (Consumer or Provider)
    Manages agent lifecycle and execution
    """
    
    def __init__(self):
        self.consumer_agent = None
        self.provider_agent = None
        logger.info("AgentDispatcher initialized")
    
    async def dispatch(
        self,
        task_plan: Dict[str, Any],
        agent_type: str,
        user_id: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Dispatch task plan to appropriate agent
        
        Args:
            task_plan: Execution plan with subtasks
            agent_type: Type of agent to dispatch to
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            Agent response
        """
        try:
            logger.info(f"Dispatching to {agent_type} agent for user {user_id}")
            
            start_time = datetime.utcnow()
            
            # Lazy load agents
            if agent_type == "consumer":
                agent = await self._get_consumer_agent()
            elif agent_type == "provider":
                agent = await self._get_provider_agent()
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            # Execute task plan through agent
            response = await agent.execute(
                task_plan=task_plan,
                user_id=user_id,
                session_id=session_id
            )
            
            # Add execution metadata
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            response["execution_metadata"] = {
                "agent_type": agent_type,
                "execution_time_seconds": execution_time,
                "tasks_completed": len(task_plan.get("subtasks", [])),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(
                f"{agent_type} agent completed execution in {execution_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in dispatch: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "agent_type": agent_type,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def dispatch_stream(
        self,
        task_plan: Dict[str, Any],
        agent_type: str,
        user_id: str,
        session_id: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream responses from agent execution
        """
        try:
            logger.info(f"Streaming from {agent_type} agent for user {user_id}")
            
            # Get appropriate agent
            if agent_type == "consumer":
                agent = await self._get_consumer_agent()
            elif agent_type == "provider":
                agent = await self._get_provider_agent()
            else:
                yield {"error": f"Unknown agent type: {agent_type}"}
                return
            
            # Stream execution
            async for chunk in agent.execute_stream(
                task_plan=task_plan,
                user_id=user_id,
                session_id=session_id
            ):
                yield chunk
                
        except Exception as e:
            logger.error(f"Error in streaming dispatch: {str(e)}")
            yield {"error": str(e)}
    
    async def _get_consumer_agent(self):
        """
        Get or create Consumer Agent instance
        """
        if self.consumer_agent is None:
            # Import here to avoid circular imports
            from ..agents.consumer_agent import ConsumerAgent
            self.consumer_agent = ConsumerAgent()
            logger.info("Consumer Agent initialized")
        
        return self.consumer_agent
    
    async def _get_provider_agent(self):
        """
        Get or create Provider Agent instance
        """
        if self.provider_agent is None:
            # Import here to avoid circular imports
            from ..agents.provider_agent import ProviderAgent
            self.provider_agent = ProviderAgent()
            logger.info("Provider Agent initialized")
        
        return self.provider_agent
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check health status of all agents
        """
        health_status = {
            "dispatcher": "healthy",
            "agents": {}
        }
        
        try:
            if self.consumer_agent:
                health_status["agents"]["consumer"] = await self.consumer_agent.health_check()
            else:
                health_status["agents"]["consumer"] = "not_initialized"
            
            if self.provider_agent:
                health_status["agents"]["provider"] = await self.provider_agent.health_check()
            else:
                health_status["agents"]["provider"] = "not_initialized"
                
        except Exception as e:
            health_status["error"] = str(e)
            health_status["dispatcher"] = "unhealthy"
        
        return health_status
