"""
A2A Server Helper Functions
Provides common functionality for A2A (Agent-to-Agent) server implementations.
"""

from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class AgentRequest(BaseModel):
    """Standard request format for A2A communication."""
    message: str
    context: Dict[str, Any] = {}
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    """Standard response format for A2A communication."""
    message: str
    status: str
    data: Dict[str, Any] = {}

def create_agent_server(name: str, description: str, task_manager) -> FastAPI:
    """
    Create a standardized FastAPI server for an A2A agent.
    
    Args:
        name: Agent name
        description: Agent description
        task_manager: TaskManager instance that handles requests
        
    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title=f"{name} A2A Server",
        description=description,
        version="1.0.0"
    )
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "agent": name}
    
    @app.post("/run", response_model=AgentResponse)
    async def run_task(request: AgentRequest):
        """Main endpoint for processing agent tasks."""
        try:
            logger.info(f"Processing request: {request.message[:100]}...")
            
            result = await task_manager.process_task(
                message=request.message,
                context=request.context,
                session_id=request.session_id
            )
            
            return AgentResponse(**result)
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing request: {str(e)}"
            )
    
    @app.get("/")
    async def root():
        """Root endpoint with agent information."""
        return {
            "agent": name,
            "description": description,
            "endpoints": ["/health", "/run"],
            "status": "ready"
        }
    
    return app