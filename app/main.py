import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.api.new_endpoints import router as new_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Agentic Data Analyst API",
    description="A modern, agentic AI-powered data analysis system using Ollama",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(new_router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Agentic Data Analyst API is running",
        "version": "2.0.0",
        "docs": "/docs",
        "features": [
            "Agentic AI data analysis",
            "Dynamic tool discovery",
            "Natural language processing",
            "Open source with Ollama",
            "No hardcoded task types"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/tools")
async def list_tools():
    """List all available tools"""
    from app.tools.registry import tool_manager
    return tool_manager.list_available_tools()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
