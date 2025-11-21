"""
Main FastAPI Application
Entry point for the Kumbuk AI Agent System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Kumbuk AI Agent System",
    description="Orchestration layer for Consumer and Provider AI agents",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
try:
    from app.api.routes import orchestration
    app.include_router(orchestration.router, prefix="/api")
    logger.info("Orchestration routes loaded successfully")
except ImportError as e:
    logger.error(f"Error loading orchestration routes: {str(e)}")
    logger.info("Routes will be available after modules are properly installed")
except Exception as e:
    logger.error(f"Unexpected error loading routes: {str(e)}")

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Kumbuk AI Agent System",
        "status": "running",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "kumbuk-ai-agents"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Kumbuk AI Agent System...")
    logger.info("Orchestration layer initialized")
    logger.info("API Documentation: http://localhost:8000/api/docs")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Kumbuk AI Agent System...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
