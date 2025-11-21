# KumbuK Backend

FastAPI backend with AI agent orchestration for KumbuK service platform.

## Quick Start

```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload
```

**Backend API**: http://localhost:8000  
**API Docs**: http://localhost:8000/docs

## Architecture

- FastAPI for REST + WebSocket APIs
- AI Agent system with orchestration
- Mock services for local development
- Pydantic for data validation

## Testing

```powershell
# Run tests
python test_backend.py
```

## Documentation

See [project documentation](../docs/) for architecture and integration guides.
