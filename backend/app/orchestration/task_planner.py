"""
Task Planner - Creates execution plans for agent tasks
"""

from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskPlanner:
    """
    Creates detailed task plans based on routing decisions
    Breaks down complex requests into manageable subtasks
    """
    
    def __init__(self):
        logger.info("TaskPlanner initialized")
    
    async def create_plan(
        self,
        routing_decision: Dict[str, Any],
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a task execution plan
        
        Args:
            routing_decision: Router's decision on agent selection
            preprocessed_data: Preprocessed request data
            
        Returns:
            Task plan with subtasks and execution strategy
        """
        try:
            agent_type = routing_decision["agent_type"]
            intent = routing_decision.get("intent", "general")
            entities = preprocessed_data.get("entities", {})
            
            logger.debug(f"Creating task plan for {agent_type} agent with intent: {intent}")
            
            # Create plan based on agent type and intent
            if agent_type == "consumer":
                task_plan = await self._create_consumer_plan(intent, entities, preprocessed_data)
            elif agent_type == "provider":
                task_plan = await self._create_provider_plan(intent, entities, preprocessed_data)
            else:
                task_plan = await self._create_default_plan(preprocessed_data)
            
            # Add metadata
            task_plan["routing_decision"] = routing_decision
            task_plan["preprocessed_data"] = preprocessed_data
            task_plan["created_at"] = datetime.utcnow().isoformat()
            
            logger.info(
                f"Task plan created with {len(task_plan['subtasks'])} subtasks "
                f"for {agent_type} agent"
            )
            
            return task_plan
            
        except Exception as e:
            logger.error(f"Error creating task plan: {str(e)}")
            return self._create_default_plan(preprocessed_data)
    
    async def _create_consumer_plan(
        self,
        intent: str,
        entities: Dict[str, Any],
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create task plan for Consumer Agent
        """
        subtasks = []
        data_sources = []
        
        if intent == "service_search":
            # Service search workflow
            subtasks = [
                {
                    "task_id": "extract_requirements",
                    "description": "Extract service requirements from user message",
                    "priority": 1,
                    "required": True
                },
                {
                    "task_id": "query_neo4j",
                    "description": "Query Neo4j for service relationships and ontology",
                    "priority": 2,
                    "required": True,
                    "params": {
                        "services": entities.get("services", []),
                        "locations": entities.get("locations", [])
                    }
                },
                {
                    "task_id": "search_firestore",
                    "description": "Search Firestore for matching providers",
                    "priority": 3,
                    "required": True,
                    "params": {
                        "filters": {
                            "services": entities.get("services", []),
                            "locations": entities.get("locations", []),
                            "price_range": entities.get("price_range")
                        }
                    }
                },
                {
                    "task_id": "generate_recommendations",
                    "description": "Generate personalized recommendations using Vertex AI",
                    "priority": 4,
                    "required": True
                },
                {
                    "task_id": "format_response",
                    "description": "Format results for user-friendly presentation",
                    "priority": 5,
                    "required": True
                }
            ]
            
            data_sources = ["neo4j", "firestore", "vertex_ai"]
            
        elif intent == "general":
            # General inquiry workflow
            subtasks = [
                {
                    "task_id": "understand_query",
                    "description": "Understand general user query",
                    "priority": 1,
                    "required": True
                },
                {
                    "task_id": "generate_response",
                    "description": "Generate helpful response using LangChain",
                    "priority": 2,
                    "required": True
                }
            ]
            
            data_sources = ["vertex_ai", "langchain"]
        
        else:
            # Default consumer workflow
            subtasks = [
                {
                    "task_id": "process_query",
                    "description": "Process user query",
                    "priority": 1,
                    "required": True
                },
                {
                    "task_id": "generate_response",
                    "description": "Generate response",
                    "priority": 2,
                    "required": True
                }
            ]
            
            data_sources = ["vertex_ai"]
        
        return {
            "plan_type": "consumer",
            "intent": intent,
            "subtasks": subtasks,
            "data_sources": data_sources,
            "execution_strategy": "sequential",
            "estimated_duration_ms": len(subtasks) * 500,
            "requires_context": bool(entities.get("services") or entities.get("locations"))
        }
    
    async def _create_provider_plan(
        self,
        intent: str,
        entities: Dict[str, Any],
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create task plan for Provider Agent
        """
        subtasks = []
        data_sources = []
        
        if intent == "business_query":
            # Business analytics workflow
            subtasks = [
                {
                    "task_id": "identify_metrics",
                    "description": "Identify requested business metrics",
                    "priority": 1,
                    "required": True
                },
                {
                    "task_id": "fetch_provider_data",
                    "description": "Fetch provider data from Firestore",
                    "priority": 2,
                    "required": True,
                    "params": {
                        "user_id": preprocessed_data.get("user_id")
                    }
                },
                {
                    "task_id": "calculate_analytics",
                    "description": "Calculate business analytics and insights",
                    "priority": 3,
                    "required": True
                },
                {
                    "task_id": "query_market_trends",
                    "description": "Query Neo4j for market trends and competition",
                    "priority": 4,
                    "required": False
                },
                {
                    "task_id": "generate_insights",
                    "description": "Generate actionable insights using Vertex AI",
                    "priority": 5,
                    "required": True
                },
                {
                    "task_id": "format_report",
                    "description": "Format analytics report",
                    "priority": 6,
                    "required": True
                }
            ]
            
            data_sources = ["firestore", "neo4j", "vertex_ai", "mysql"]
            
        else:
            # Default provider workflow
            subtasks = [
                {
                    "task_id": "fetch_provider_context",
                    "description": "Fetch provider business context",
                    "priority": 1,
                    "required": True
                },
                {
                    "task_id": "process_request",
                    "description": "Process provider request",
                    "priority": 2,
                    "required": True
                },
                {
                    "task_id": "generate_response",
                    "description": "Generate business-focused response",
                    "priority": 3,
                    "required": True
                }
            ]
            
            data_sources = ["firestore", "vertex_ai"]
        
        return {
            "plan_type": "provider",
            "intent": intent,
            "subtasks": subtasks,
            "data_sources": data_sources,
            "execution_strategy": "sequential",
            "estimated_duration_ms": len(subtasks) * 600,
            "requires_provider_auth": True
        }
    
    async def _create_default_plan(
        self,
        preprocessed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create default fallback plan
        """
        return {
            "plan_type": "default",
            "intent": "unknown",
            "subtasks": [
                {
                    "task_id": "process_message",
                    "description": "Process user message",
                    "priority": 1,
                    "required": True
                },
                {
                    "task_id": "generate_response",
                    "description": "Generate generic response",
                    "priority": 2,
                    "required": True
                }
            ],
            "data_sources": ["vertex_ai"],
            "execution_strategy": "sequential",
            "estimated_duration_ms": 1000,
            "preprocessed_data": preprocessed_data
        }
