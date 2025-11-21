# KumbuK System Architecture Diagrams

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                           │
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │  Consumer App    │              │  Provider App    │        │
│  │  (React Native)  │              │  (React Native)  │        │
│  │                  │              │                  │        │
│  │  - AgentChat UI  │              │  - Business UI   │        │
│  │  - Service Search│              │  - Analytics     │        │
│  │  - Bookings      │              │  - Inquiries     │        │
│  └────────┬─────────┘              └────────┬─────────┘        │
│           │                                  │                  │
│           │         WebSocket/HTTP           │                  │
│           └──────────────┬───────────────────┘                  │
└────────────────────────┼─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND LAYER                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                         │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │  │
│  │  │  REST  │  │   WS   │  │ Health │  │ Session│        │  │
│  │  │  API   │  │        │  │ Check  │  │  Mgmt  │        │  │
│  │  └────┬───┘  └───┬────┘  └────────┘  └────────┘        │  │
│  └───────┼──────────┼──────────────────────────────────────┘  │
│          │          │                                          │
│          └──────────┼──────────────┐                           │
│                     ▼              │                           │
│  ┌─────────────────────────────────┼────────────────────────┐ │
│  │     BedRock Aggregator          │                        │ │
│  │  (Main Orchestration Controller)│                        │ │
│  │                                 │                        │ │
│  │  Step 1: ┌──────────────┐      │                        │ │
│  │          │    Router     │──────┘                        │ │
│  │          │ (Intent Class)│                               │ │
│  │          └───────┬───────┘                               │ │
│  │                  │                                       │ │
│  │  Step 2: ┌──────▼───────┐                               │ │
│  │          │ Preprocessor  │                               │ │
│  │          │ (Entity Extrc)│                               │ │
│  │          └───────┬───────┘                               │ │
│  │                  │                                       │ │
│  │  Step 3: ┌──────▼───────┐                               │ │
│  │          │ Task Planner  │                               │ │
│  │          │ (Create Plan) │                               │ │
│  │          └───────┬───────┘                               │ │
│  │                  │                                       │ │
│  │  Step 4: ┌──────▼───────┐                               │ │
│  │          │  Dispatcher   │                               │ │
│  │          │ (Route Agent) │                               │ │
│  │          └───────┬───────┘                               │ │
│  │                  │                                       │ │
│  └──────────────────┼───────────────────────────────────────┘ │
│                     │                                         │
│  Step 5:            ▼                                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 AI AGENTS LAYER                         │ │
│  │                                                         │ │
│  │  ┌──────────────────┐         ┌──────────────────┐    │ │
│  │  │  Consumer Agent  │         │  Provider Agent  │    │ │
│  │  │                  │         │                  │    │ │
│  │  │ - Service Search │         │ - Analytics      │    │ │
│  │  │ - Recommendations│         │ - Inquiries      │    │ │
│  │  │ - Provider Match │         │ - Revenue Track  │    │ │
│  │  └────────┬─────────┘         └────────┬─────────┘    │ │
│  │           │                            │              │ │
│  └───────────┼────────────────────────────┼──────────────┘ │
│              │                            │                │
│  Step 6:     └────────────┬───────────────┘                │
│                           ▼                                │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Handler (Response Formatting)          │  │
│  │  - Format response by type                          │  │
│  │  - Add metadata                                     │  │
│  │  - Error handling                                   │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                  │
│  Step 7: Return Response│                                  │
│                         │                                  │
└─────────────────────────┼────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICES LAYER (Mock)                      │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐  │
│  │ Firebase Service │  │  State Manager   │  │   Others    │  │
│  │                  │  │                  │  │             │  │
│  │ - Conversations  │  │ - Sessions       │  │ - Analytics │  │
│  │ - User Profiles  │  │ - State Storage  │  │ - Logging   │  │
│  │ - Realtime Msgs  │  │ - CRUD Ops       │  │             │  │
│  └──────────────────┘  └──────────────────┘  └─────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Request Flow Sequence

```
USER                 FRONTEND              BACKEND                   AGENTS
 │                     │                     │                         │
 │  Type Message       │                     │                         │
 ├────────────────────>│                     │                         │
 │                     │                     │                         │
 │                     │  POST /message or   │                         │
 │                     │  WebSocket Message  │                         │
 │                     ├────────────────────>│                         │
 │                     │                     │                         │
 │                     │                     │  1. Router              │
 │                     │                     │  (Classify Intent)      │
 │                     │                     ├─────────┐               │
 │                     │                     │         │               │
 │                     │                     │<────────┘               │
 │                     │                     │  Intent: service_search │
 │                     │                     │                         │
 │                     │                     │  2. Preprocessor        │
 │                     │                     │  (Extract Entities)     │
 │                     │                     ├─────────┐               │
 │                     │                     │         │               │
 │                     │                     │<────────┘               │
 │                     │                     │  Entities: {services,   │
 │                     │                     │  locations}             │
 │                     │                     │                         │
 │                     │                     │  3. Task Planner        │
 │                     │                     │  (Create Plan)          │
 │                     │                     ├─────────┐               │
 │                     │                     │         │               │
 │                     │                     │<────────┘               │
 │                     │                     │  Plan: {agent, tasks}   │
 │                     │                     │                         │
 │                     │                     │  4. Dispatcher          │
 │                     │                     │  (Route to Agent)       │
 │                     │                     ├────────────────────────>│
 │                     │                     │                         │
 │                     │                     │  5. Agent Execute       │
 │                     │                     │                         │
 │                     │                     │                    ┌────┤
 │                     │                     │                    │    │
 │                     │                     │                    │ Search
 │                     │                     │                    │ Filter
 │                     │                     │                    │ Rank
 │                     │                     │                    │    │
 │                     │                     │                    └───>│
 │                     │                     │                         │
 │                     │                     │<────────────────────────┤
 │                     │                     │  Result: {providers}    │
 │                     │                     │                         │
 │                     │                     │  6. Handler             │
 │                     │                     │  (Format Response)      │
 │                     │                     ├─────────┐               │
 │                     │                     │         │               │
 │                     │                     │<────────┘               │
 │                     │                     │  Response: {message,    │
 │                     │                     │  providers, type}       │
 │                     │                     │                         │
 │                     │<────────────────────┤                         │
 │                     │  JSON Response      │                         │
 │                     │                     │                         │
 │<────────────────────┤                     │                         │
 │  Display Message    │                     │                         │
 │  + Provider Cards   │                     │                         │
 │                     │                     │                         │
```

---

## 3. Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    AgentChat Component                         │
│                                                                │
│  ┌─────────────┐                                              │
│  │   State     │                                              │
│  │ - messages  │                                              │
│  │ - inputText │                                              │
│  │ - isLoading │                                              │
│  │ - sessionId │                                              │
│  │ - ws        │                                              │
│  └─────┬───────┘                                              │
│        │                                                      │
│        │ ┌──────────────┐     ┌──────────────┐              │
│        ├─┤ WebSocket    │     │ HTTP Fetch   │              │
│        │ │ Connection   │     │ (Fallback)   │              │
│        │ └──────┬───────┘     └──────┬───────┘              │
│        │        │                    │                      │
│        │        └────────┬───────────┘                      │
│        │                 │                                  │
│  ┌─────▼─────────────────▼──────┐                          │
│  │      Message Handler          │                          │
│  │   - Parse response            │                          │
│  │   - Update messages state     │                          │
│  │   - Stop loading indicator    │                          │
│  └───────────────────────────────┘                          │
│                 │                                            │
│  ┌──────────────▼────────────┐                              │
│  │       UI Rendering        │                              │
│  │  ┌─────────────────────┐  │                              │
│  │  │  Header             │  │                              │
│  │  │  - Title            │  │                              │
│  │  │  - Status Indicator │  │                              │
│  │  └─────────────────────┘  │                              │
│  │                           │                              │
│  │  ┌─────────────────────┐  │                              │
│  │  │  Message List       │  │                              │
│  │  │  - User messages    │  │                              │
│  │  │  - Agent messages   │  │                              │
│  │  │  - Suggestions      │  │                              │
│  │  │  - Provider cards   │  │                              │
│  │  └─────────────────────┘  │                              │
│  │                           │                              │
│  │  ┌─────────────────────┐  │                              │
│  │  │  Input Area         │  │                              │
│  │  │  - Text input       │  │                              │
│  │  │  - Send button      │  │                              │
│  │  │  - Loading indicator│  │                              │
│  │  └─────────────────────┘  │                              │
│  └───────────────────────────┘                              │
└────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow Diagram

```
┌─────────────┐
│  User Input │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Message: "Find plumber in Colombo" │
└──────┬──────────────────────────────┘
       │
       ▼
┌──────────────────┐
│  Router          │ → Intent: service_search (0.95)
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Preprocessor    │ → Entities: {
└──────┬───────────┘     services: ["plumbing"],
       │                 locations: ["colombo"]
       │               }
       ▼
┌──────────────────┐
│  Task Planner    │ → Plan: {
└──────┬───────────┘     agent: "consumer",
       │                 subtasks: ["search", "filter"],
       │                 data_sources: ["neo4j", "firestore"]
       │               }
       ▼
┌──────────────────┐
│  Dispatcher      │ → Route to Consumer Agent
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Consumer Agent  │ → Execute:
└──────┬───────────┘     1. Search providers
       │                 2. Filter by location/service
       │                 3. Rank by rating
       │               → Result: {
       │                   providers: [
       │                     {name: "Silva Plumbing",
       │                      rating: 4.8, ...}
       │                   ]
       │                 }
       ▼
┌──────────────────┐
│  Handler         │ → Format: {
└──────┬───────────┘     type: "service_results",
       │                 message: "I found 1 plumber...",
       │                 providers: [...],
       │                 timestamp: "..."
       │               }
       ▼
┌─────────────────────────────────────┐
│  Response to Frontend               │
│  - Message text                     │
│  - Provider cards                   │
│  - Suggestions                      │
└─────────────────────────────────────┘
```

---

## 5. Technology Stack Diagram

```
┌───────────────────────────────────────────────────────────┐
│                      FRONTEND STACK                       │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ React Native │  │   Expo       │  │  TypeScript  │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Nx Tools   │  │  WebSocket   │  │  Fetch API   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────────┘
                           │
                           │ JSON/WebSocket
                           │
┌───────────────────────────▼───────────────────────────────┐
│                      BACKEND STACK                        │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   FastAPI    │  │  Uvicorn     │  │  Pydantic    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  WebSockets  │  │   Asyncio    │  │   Python     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────────┘
                           │
                           │ (Future Integration)
                           │
┌───────────────────────────▼───────────────────────────────┐
│                    CLOUD SERVICES (Planned)               │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Firebase   │  │  Vertex AI   │  │   Neo4j      │   │
│  │  (Firestore) │  │ (Gemini-Pro) │  │    Aura      │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐                      │
│  │ Firebase Auth│  │  Realtime DB │                      │
│  └──────────────┘  └──────────────┘                      │
└───────────────────────────────────────────────────────────┘
```

---

## 6. Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   BASE AGENT INTERFACE                  │
│                                                         │
│  - execute(task_plan, user_id, session_id)             │
│  - execute_stream(task_plan, user_id, session_id)      │
│  - health_check()                                       │
└────────────┬────────────────────────────────────────────┘
             │
             ├─────────────────┬─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
┌────────────────────┐ ┌────────────────┐ ┌─────────────┐
│  Consumer Agent    │ │ Provider Agent │ │ Future:     │
│                    │ │                │ │ - Admin     │
│ - Service Search   │ │ - Analytics    │ │ - Matching  │
│ - Recommendations  │ │ - Inquiries    │ │ - Payment   │
│ - Provider Match   │ │ - Revenue      │ │             │
│ - General Help     │ │ - Ratings      │ │             │
└────────────────────┘ └────────────────┘ └─────────────┘
```

---

## 7. Session Management

```
┌─────────────────────────────────────────────────────────┐
│                    Session Lifecycle                    │
│                                                         │
│  1. Create Session                                      │
│     └─> session_id = "session_{user_id}_{timestamp}"   │
│                                                         │
│  2. Initialize State                                    │
│     └─> state = {                                       │
│           last_intent: None,                            │
│           conversation_history: [],                     │
│           context: {}                                   │
│         }                                               │
│                                                         │
│  3. Update on Each Message                              │
│     └─> Add to conversation_history                     │
│     └─> Update last_intent                              │
│     └─> Merge context                                   │
│                                                         │
│  4. Retrieve State                                      │
│     └─> GET /session/{session_id}                       │
│                                                         │
│  5. Clear/Reset                                         │
│     └─> Manual or on timeout                            │
└─────────────────────────────────────────────────────────┘
```

---

**Last Updated**: December 2024
