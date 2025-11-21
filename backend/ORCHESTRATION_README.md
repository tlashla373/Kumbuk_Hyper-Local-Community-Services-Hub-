# 🎯 Orchestration Layer Implementation

## 📋 Overview

The orchestration layer is the **central nervous system** of the Kumbuk AI Agent System. It coordinates all agent interactions, manages request flow, and ensures seamless communication between the frontend, agents, and data sources.

## 🏗️ Architecture Components

Based on the system architecture diagram, the orchestration layer consists of:

### 1. **BedRock Aggregator** (`bedrock_aggregator.py`)
- **Role**: Main entry point and coordinator
- **Responsibilities**:
  - Aggregates requests from frontend
  - Coordinates entire workflow
  - Manages session state
  - Saves conversations to Firebase

### 2. **Router** (`router.py`)
- **Role**: Intent classification and agent selection
- **Responsibilities**:
  - Classifies user intent using Vertex AI
  - Routes to Consumer or Provider agent
  - Provides confidence scores
  - Handles fallback routing

### 3. **Pre-Processor** (`preprocessor.py`)
- **Role**: Request preparation and enrichment
- **Responsibilities**:
  - Cleans and normalizes text
  - Extracts entities (locations, services, prices)
  - Loads user context from Firebase
  - Enriches with session history

### 4. **Task Planner** (`task_planner.py`)
- **Role**: Creates execution plans for agents
- **Responsibilities**:
  - Breaks down complex requests
  - Creates subtasks for agents
  - Determines data sources needed
  - Estimates execution time

### 5. **Handler** (`handler.py`)
- **Role**: Response formatting and error handling
- **Responsibilities**:
  - Formats agent responses
  - Enriches with metadata
  - Handles errors gracefully
  - Provides user-friendly messages

### 6. **Dispatcher** (`dispatcher.py`)
- **Role**: Agent execution manager
- **Responsibilities**:
  - Dispatches tasks to agents
  - Manages agent lifecycle
  - Supports streaming responses
  - Monitors agent health

---

## 🔄 Request Flow

```
┌─────────────────┐
│  User Request   │
│  (Frontend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ BedRock Aggregator  │ ◄── Entry Point
│  process_request()  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Pre-Processor     │ ◄── Step 1: Clean & Enrich
│  - Extract entities │
│  - Load context     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│      Router         │ ◄── Step 2: Route to Agent
│  - Classify intent  │
│  - Select agent     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Task Planner      │ ◄── Step 3: Create Plan
│  - Build subtasks   │
│  - Set data sources │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│    Dispatcher       │ ◄── Step 4: Execute
│  - Dispatch to      │
│    Consumer/        │
│    Provider Agent   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Agent Execution     │ ◄── Agent processes task
│  - Query Neo4j      │
│  - Search Firestore │
│  - Use Vertex AI    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│     Handler         │ ◄── Step 5: Format Response
│  - Format output    │
│  - Add metadata     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Save to Firebase   │ ◄── Step 6: Persist
│  - Realtime DB      │
│  - Firestore        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Return to User     │
│  (JSON Response)    │
└─────────────────────┘
```

---

## 🚀 Usage Examples

### Basic Chat Request

```python
from app.orchestration.bedrock_aggregator import BedrockAggregator

orchestrator = BedrockAggregator()

# Process a user message
result = await orchestrator.process_request(
    user_id="user123",
    message="Find me a plumber in Colombo under Rs. 5000",
    session_id="session_abc",
    context={}
)

print(result)
# Output:
# {
#   "success": True,
#   "request_id": "user123_1234567890.123",
#   "response": {
#     "type": "service_results",
#     "message": "I found 3 plumbers in Colombo within your budget...",
#     "providers": [...],
#     "recommendations": [...]
#   },
#   "agent_type": "consumer",
#   "session_id": "session_abc"
# }
```

### Streaming Response

```python
# Stream responses in real-time
async for chunk in orchestrator.stream_response(
    user_id="user123",
    message="How is my business performing?",
    session_id="session_xyz"
):
    print(chunk)
    # Chunks sent to Firebase Realtime Database
```

### API Endpoint Usage

```bash
# Send message via REST API
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "message": "I need a painter in Kandy",
    "session_id": "abc123"
  }'

# WebSocket connection
ws://localhost:8000/api/v1/chat/ws/user123
```

---

## 📊 Component Details

### BedRock Aggregator

**Key Methods:**
- `process_request()` - Main orchestration flow
- `stream_response()` - Real-time streaming
- `get_session_context()` - Retrieve session data
- `clear_session()` - Clear session state

**Example:**
```python
result = await orchestrator.process_request(
    user_id="user123",
    message="Find electricians",
    session_id=None,  # Auto-generated if None
    context={"location": "Galle"}
)
```

### Router

**Intent Classification:**
- `service_search` - Looking for services
- `business_query` - Provider analytics
- `general` - Greetings, help

**Example:**
```python
from app.orchestration.router import AgentRouter

router = AgentRouter()
routing_decision = await router.route(
    preprocessed_data={
        "message": "Find me a plumber",
        "user_role": "consumer"
    },
    user_id="user123"
)
# Returns: {"agent_type": "consumer", "confidence": 0.95, ...}
```

### Pre-Processor

**Entity Extraction:**
- **Locations**: Colombo, Kandy, Galle, etc.
- **Services**: Plumber, Electrician, Painter, etc.
- **Price Range**: Rs. 5000, under 10000, etc.
- **Time**: Today, urgent, weekend, etc.

**Example:**
```python
from app.orchestration.preprocessor import PreProcessor

preprocessor = PreProcessor()
preprocessed = await preprocessor.process(
    user_id="user123",
    message="Need a plumber in Colombo under Rs. 5000 today",
    session_id=None
)

print(preprocessed["entities"])
# {
#   "locations": ["Colombo"],
#   "services": ["Plumber"],
#   "price_range": {"amount": 5000, "currency": "LKR"},
#   "time_references": ["today"]
# }
```

### Task Planner

**Consumer Agent Plan:**
```python
{
    "plan_type": "consumer",
    "subtasks": [
        {"task_id": "extract_requirements", "priority": 1},
        {"task_id": "query_neo4j", "priority": 2},
        {"task_id": "search_firestore", "priority": 3},
        {"task_id": "generate_recommendations", "priority": 4}
    ],
    "data_sources": ["neo4j", "firestore", "vertex_ai"]
}
```

**Provider Agent Plan:**
```python
{
    "plan_type": "provider",
    "subtasks": [
        {"task_id": "fetch_provider_data", "priority": 1},
        {"task_id": "calculate_analytics", "priority": 2},
        {"task_id": "query_market_trends", "priority": 3},
        {"task_id": "generate_insights", "priority": 4}
    ],
    "data_sources": ["firestore", "neo4j", "vertex_ai", "mysql"]
}
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1

# Firebase
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-key.json

# Neo4j
NEO4J_URI=neo4j+s://your-instance.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# API
JWT_SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

---

## 🧪 Testing

### Unit Tests

```python
import pytest
from app.orchestration.bedrock_aggregator import BedrockAggregator

@pytest.mark.asyncio
async def test_process_request():
    orchestrator = BedrockAggregator()
    
    result = await orchestrator.process_request(
        user_id="test_user",
        message="Test message",
        session_id="test_session"
    )
    
    assert result["success"] == True
    assert "response" in result
    assert "agent_type" in result
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_flow():
    # Test complete orchestration flow
    orchestrator = BedrockAggregator()
    
    result = await orchestrator.process_request(
        user_id="test_user",
        message="Find plumbers in Colombo",
        session_id=None
    )
    
    assert result["agent_type"] == "consumer"
    assert "providers" in result["response"]
```

---

## 📈 Performance Monitoring

### Metrics to Track

1. **Response Time**: Time from request to response
2. **Agent Selection Accuracy**: Correct agent routing rate
3. **Error Rate**: Failed requests percentage
4. **Throughput**: Requests per second

### Health Check

```bash
curl http://localhost:8000/api/v1/chat/health
```

Response:
```json
{
    "status": "healthy",
    "components": {
        "orchestrator": "ok",
        "router": "ok",
        "preprocessor": "ok",
        "task_planner": "ok",
        "dispatcher": "ok"
    }
}
```

---

## 🔒 Security

1. **Authentication**: All endpoints require JWT token
2. **Rate Limiting**: Prevent abuse
3. **Input Validation**: Sanitize user input
4. **Error Handling**: Never expose internal errors

---

## 🚦 Next Steps

1. **Implement Agent Layer**:
   - Consumer Agent
   - Provider Agent
   - State Manager

2. **Connect Data Sources**:
   - Firebase Firestore integration
   - Neo4j Aura integration
   - MySQL integration

3. **Add LangChain Integration**:
   - Vertex AI connection
   - Conversation memory
   - Context management

4. **Frontend Integration**:
   - WebSocket client
   - Real-time updates
   - UI components

---

## 📚 API Reference

### POST /api/v1/chat/message
Send a message to the AI agent system

**Request:**
```json
{
    "message": "Find me a plumber",
    "session_id": "optional",
    "context": {}
}
```

**Response:**
```json
{
    "success": true,
    "request_id": "req_123",
    "response": {...},
    "agent_type": "consumer",
    "timestamp": "2025-10-31T...",
    "session_id": "session_123"
}
```

### WebSocket /api/v1/chat/ws/{user_id}
Real-time bidirectional communication

**Send:**
```json
{
    "message": "Hello",
    "session_id": "session_123"
}
```

**Receive:**
```json
{
    "type": "response",
    "data": {...},
    "timestamp": "..."
}
```

---

**Orchestration Layer Status**: ✅ Implemented
**Next Component**: 🤖 Agent Layer (Consumer & Provider Agents)
