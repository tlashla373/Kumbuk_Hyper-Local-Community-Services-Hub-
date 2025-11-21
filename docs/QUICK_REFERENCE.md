# KumbuK - Quick Reference Card

## 🚀 Start Commands

### Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```
**URL**: http://localhost:8000  
**Docs**: http://localhost:8000/docs

### Frontend
```powershell
nx start consumer-app
```
**Action**: Scan QR code with Expo Go

### Test Backend
```powershell
cd backend
python test_backend.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/message` | Send chat message |
| WS | `/ws/{user_id}` | WebSocket connection |
| GET | `/health` | Health check |
| GET | `/session/{session_id}` | Get session state |

---

## 💬 Test Messages

### Consumer Agent
```
"Find me a plumber in Colombo"
"I need an electrician in Kandy"
"Show me painters"
"Hello"
```

### Provider Agent
```
"Show pending inquiries"
"How much did I earn this month?"
"What's my current rating?"
"Show analytics"
```

---

## 📁 Key Files

### Backend
- `app/main.py` - FastAPI app
- `app/agents/consumer_agent.py` - Consumer agent
- `app/agents/provider_agent.py` - Provider agent
- `app/orchestration/bedrock_aggregator.py` - Main orchestrator
- `requirements.txt` - Dependencies

### Frontend
- `apps/consumer-app/src/components/AgentChat.tsx` - Chat UI
- `apps/consumer-app/src/screens/ChatScreen.tsx` - Chat screen

---

## 🔧 Configuration

### Change Backend URL (Frontend)
Edit `apps/consumer-app/src/screens/ChatScreen.tsx`:
```tsx
apiUrl="http://YOUR_IP:8000"
```

### Change Port (Backend)
```powershell
python -m uvicorn app.main:app --reload --port 9000
```

---

## 🐛 Common Issues

### Backend won't start
```powershell
pip install -r requirements.txt
```

### Frontend won't connect
- Check backend is running
- Use computer's IP instead of localhost on mobile
- Example: `http://192.168.1.100:8000`

### WebSocket fails
- App automatically falls back to HTTP
- Check network/firewall settings

---

## 📊 Project Structure

```
backend/
  app/
    main.py              # Entry point
    agents/              # AI agents
    orchestration/       # Orchestration layer
    api/routes/          # API endpoints
    services/            # Mock services
  requirements.txt       # Dependencies

apps/
  consumer-app/
    src/
      components/        # AgentChat
      screens/           # ChatScreen
```

---

## 🎯 Architecture Flow

```
User → AgentChat → WebSocket/HTTP → FastAPI
         ↓
   BedRock Aggregator
         ↓
   Router → Preprocessor → Task Planner
         ↓
   Dispatcher → Consumer/Provider Agent
         ↓
   Handler → Response → AgentChat → User
```

---

## 📝 Quick Setup

```powershell
# 1. Setup (one time)
.\start-kumbuk.ps1

# 2. Run Backend (Terminal 1)
cd backend; .\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

# 3. Run Frontend (Terminal 2)
nx start consumer-app

# 4. Test (Terminal 3)
cd backend; python test_backend.py
```

---

## 🌐 URLs

- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Frontend: Expo QR code

---

## 🔑 Mock Users

- Consumer: `consumer_123`
- Provider: `provider_456`
- Test: `test_user_001`

---

## 📚 Documentation

- `README_INTEGRATION.md` - Full guide
- `INTEGRATION_SUMMARY.md` - Detailed summary
- `requirement_explanation.md` - Python basics
- `AI_Agent_Architecture_Guide.md` - Architecture

---

## ✅ Checklist

Before starting:
- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Expo Go app on phone
- [ ] Dependencies installed

To run:
- [ ] Backend running (port 8000)
- [ ] Frontend started (Expo)
- [ ] QR code scanned
- [ ] Chat interface loaded

---

**Need Help?** Check `README_INTEGRATION.md` for detailed troubleshooting!
