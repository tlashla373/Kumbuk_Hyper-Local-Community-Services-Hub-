# KumbuK - Backend & Frontend Integration Guide

## 🚀 Quick Start

This guide will help you run the complete KumbuK application with backend and frontend integration.

## 📋 Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 16+** (for frontend)
- **npm or yarn** (package manager)
- **Expo Go app** (on your mobile device)

## 🔧 Setup Instructions

### 1. Backend Setup (FastAPI)

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be running at: **http://localhost:8000**

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 2. Frontend Setup (React Native + Expo)

```powershell
# Navigate to project root
cd ..

# Install dependencies
npm install

# Start the consumer app
nx start consumer-app
```

This will start the Expo development server and show a QR code.

### 3. Run on Mobile Device

1. Install **Expo Go** app from:
   - iOS: App Store
   - Android: Google Play Store

2. Scan the QR code with:
   - **iOS**: Camera app
   - **Android**: Expo Go app

3. The app will load on your device

## 🎯 Testing the Integration

### Option 1: Using the Chat Screen

1. After backend is running, navigate to the chat screen in the app
2. Type a message like:
   - "Find me a plumber in Colombo"
   - "I need an electrician in Kandy"
   - "Show me painters"

### Option 2: Using API Docs

Visit http://localhost:8000/docs to test endpoints directly:

1. **POST /message** - Send a chat message
2. **WebSocket /ws/{user_id}** - Real-time chat connection
3. **GET /session/{session_id}** - Get session state
4. **GET /health** - Check server health

## 📁 Project Structure

```
Kumbuk_Hyper-Local-Community-Services-Hub-/
│
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI app entry point
│   │   ├── agents/                      # AI agents
│   │   │   ├── consumer_agent.py        # Consumer service agent
│   │   │   └── provider_agent.py        # Provider business agent
│   │   ├── orchestration/               # Orchestration layer
│   │   │   ├── bedrock_aggregator.py    # Main orchestrator
│   │   │   ├── router.py                # Intent routing
│   │   │   ├── preprocessor.py          # Input processing
│   │   │   ├── task_planner.py          # Task planning
│   │   │   ├── dispatcher.py            # Agent dispatching
│   │   │   └── handler.py               # Response handling
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── orchestration.py     # API endpoints
│   │   └── services/
│   │       ├── firebase_service.py      # Mock Firebase
│   │       └── state_manager.py         # Session management
│   └── requirements.txt                 # Python dependencies
│
├── apps/
│   ├── consumer-app/
│   │   └── src/
│   │       ├── components/
│   │       │   └── AgentChat.tsx        # Chat UI component
│   │       └── screens/
│   │           └── ChatScreen.tsx       # Chat screen
│   └── provider-app/
│       └── (similar structure)
│
└── README_INTEGRATION.md                # This file
```

## 🔌 Integration Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   React Native  │         │   FastAPI        │
│   (Frontend)    │◄───────►│   Backend        │
│                 │         │                  │
│  AgentChat      │  HTTP   │  Orchestration   │
│  Component      │  WebSocket  Layer         │
└─────────────────┘         │                  │
                            │  - Router        │
                            │  - Preprocessor  │
                            │  - Task Planner  │
                            │  - Dispatcher    │
                            │  - Agents        │
                            └──────────────────┘
```

## 🔄 Communication Flow

1. **User Input**: User types message in React Native app
2. **Send to Backend**: App sends via WebSocket or HTTP POST
3. **Orchestration**: 
   - Router classifies intent
   - Preprocessor extracts entities
   - Task Planner creates execution plan
   - Dispatcher routes to appropriate agent
4. **Agent Execution**: Consumer/Provider agent processes request
5. **Response**: Handler formats response
6. **Display**: React Native renders response with suggestions/providers

## 🌐 API Endpoints

### REST Endpoints

- `POST /message` - Send a chat message
  ```json
  {
    "message": "Find me a plumber in Colombo",
    "user_id": "consumer_123",
    "session_id": "session_123"
  }
  ```

- `GET /health` - Health check
- `GET /session/{session_id}` - Get session state

### WebSocket

- `ws://localhost:8000/ws/{user_id}` - Real-time chat
  ```json
  {
    "message": "Find me a plumber",
    "session_id": "session_123"
  }
  ```

## 📱 Frontend Components

### AgentChat Component

Located at: `apps/consumer-app/src/components/AgentChat.tsx`

**Features:**
- Real-time chat interface
- WebSocket connection with fallback to HTTP
- Message history
- Typing indicators
- Suggestion chips
- Provider cards display
- Connection status indicator

**Usage:**
```tsx
import { AgentChat } from '../components/AgentChat';

<AgentChat 
  userId="consumer_123" 
  apiUrl="http://localhost:8000" 
/>
```

### ChatScreen

Located at: `apps/consumer-app/src/screens/ChatScreen.tsx`

Simple screen wrapper for the AgentChat component.

## 🤖 Backend Components

### Agents

1. **Consumer Agent** (`consumer_agent.py`)
   - Service search
   - Provider recommendations
   - Location-based filtering
   - Mock provider data

2. **Provider Agent** (`provider_agent.py`)
   - Business analytics
   - Inquiry management
   - Revenue tracking
   - Rating summaries

### Orchestration Layer

- **BedRock Aggregator**: Main coordinator
- **Router**: Intent classification
- **Preprocessor**: Entity extraction
- **Task Planner**: Execution planning
- **Dispatcher**: Agent routing
- **Handler**: Response formatting

## 🧪 Testing Examples

### Consumer Queries

```
"Find me a plumber in Colombo"
"I need an electrician in Kandy"
"Show me painters in Galle"
"Hello"
"How does this work?"
```

### Provider Queries (when provider agent is active)

```
"Show my pending inquiries"
"How much did I earn this month?"
"What's my current rating?"
"Show my analytics"
```

## 🐛 Troubleshooting

### Backend Won't Start

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9+
```

### Frontend Won't Connect

1. Check backend is running at http://localhost:8000
2. Update `apiUrl` in ChatScreen.tsx if using different host
3. For mobile device, use your computer's IP instead of localhost:
   ```tsx
   apiUrl="http://192.168.1.100:8000"
   ```

### WebSocket Connection Issues

- WebSocket might not work on some networks
- The app will automatically fallback to HTTP POST
- Check browser console for connection errors

### Module Import Errors

```powershell
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm install
# or
yarn install
```

## 🔐 Authentication (Coming Soon)

Currently using mock user IDs. Future integration with:
- Firebase Authentication
- Google Sign-In
- Phone number verification

## ☁️ Cloud Services (Mock Mode)

Currently using **mock services** for local development:

- ✅ In-memory state management
- ✅ Mock conversation storage
- ✅ Simulated provider data

**Production deployment** will use:
- 🔜 Firebase Firestore
- 🔜 Google Vertex AI (Gemini-Pro)
- 🔜 Neo4j Aura (Knowledge Graph)
- 🔜 Firebase Realtime Database

## 📊 Next Steps

1. ✅ Backend and frontend integration complete
2. ✅ Chat interface working
3. ✅ Mock agents responding
4. 🔜 Add Firebase authentication
5. 🔜 Integrate real Vertex AI
6. 🔜 Connect to Neo4j for ontology
7. 🔜 Implement real-time notifications
8. 🔜 Add provider app integration

## 🎨 Customization

### Change Backend URL

Edit `apps/consumer-app/src/screens/ChatScreen.tsx`:
```tsx
<AgentChat 
  userId={userId} 
  apiUrl="http://YOUR_IP:8000"  // Change this
/>
```

### Add New Agents

1. Create agent in `backend/app/agents/`
2. Add to dispatcher in `dispatcher.py`
3. Update router intent classification

### Customize UI

Edit styles in `apps/consumer-app/src/components/AgentChat.tsx`

## 📝 Notes

- This is a **development version** with mock services
- WebSocket URL is hardcoded (will be configurable)
- User authentication is mocked
- Cloud services are simulated

## 🆘 Support

If you encounter issues:

1. Check logs in terminal (backend and frontend)
2. Verify all dependencies are installed
3. Ensure ports 8000 (backend) and 8081 (Expo) are not in use
4. Check network connectivity for mobile device

## 📄 License

This project is part of KumbuK - Hyper-Local Community Services Hub

---

**Happy Coding! 🎉**
