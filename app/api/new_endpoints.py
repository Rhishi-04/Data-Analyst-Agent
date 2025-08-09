from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import asyncio
import logging
import json
from datetime import datetime
from app.agents.data_analyst_agent import DataAnalystAgent
from app.utils.file_handler import FileHandler

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
async def analyze_data(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Main endpoint for data analysis tasks.
    Accepts multipart/form-data with questions.txt and optional data files.
    Returns JSON object response as required by promptfoo evaluation.
    """
    try:
        # Initialize services
        file_handler = FileHandler()
        agent = DataAnalystAgent()
        
        # Process uploaded files
        processed_files = await file_handler.process_uploads(files)
        
        # Extract questions from questions.txt
        questions_content = processed_files.get('questions.txt', '')
        if not questions_content:
            raise HTTPException(
                status_code=400,
                detail="questions.txt file is required"
            )
        
        # Parse the request
        request_data = {
            "request": questions_content,
            "files": processed_files
        }
        
        # Execute analysis with 3-minute timeout
        try:
            result = await asyncio.wait_for(
                agent.process(request_data),
                timeout=180  # 3 minutes
            )
            
            # Ensure we return a proper JSON object for promptfoo
            if isinstance(result, dict):
                return result
            elif isinstance(result, str):
                try:
                    # Try to parse string as JSON
                    parsed = json.loads(result)
                    if isinstance(parsed, dict):
                        return parsed
                    else:
                        return {"result": str(result)}
                except:
                    return {"result": str(result)}
            else:
                return {"result": str(result)}
            
        except asyncio.TimeoutError:
            return {"error": "Task timed out"}
            
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return {"error": str(e)}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}
