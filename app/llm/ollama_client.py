import httpx
import json
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, host: str = None, port: int = None, model: str = None):
        self.host = host or settings.ollama_host
        self.port = port or settings.ollama_port
        self.model = model or settings.ollama_model
        self.base_url = f"http://{self.host}:{self.port}"
        
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        context: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response from Ollama"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        if system:
            payload["system"] = system
        if context:
            payload["context"] = context
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=settings.timeout_seconds
                )
                response.raise_for_status()
                
                if stream:
                    return response
                else:
                    return response.json()
                    
            except httpx.RequestError as e:
                logger.error(f"Ollama request failed: {e}")
                raise
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Chat completion with Ollama"""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=settings.timeout_seconds
                )
                response.raise_for_status()
                
                if stream:
                    return response
                else:
                    return response.json()
                    
            except httpx.RequestError as e:
                logger.error(f"Ollama chat request failed: {e}")
                raise
    
    async def check_model(self) -> bool:
        """Check if model is available"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/tags",
                    timeout=10
                )
                response.raise_for_status()
                
                models = response.json().get("models", [])
                return any(model.get("name") == self.model for model in models)
                
        except Exception as e:
            logger.error(f"Failed to check model availability: {e}")
            return False
    
    async def pull_model(self) -> Dict[str, Any]:
        """Pull model if not available"""
        payload = {
            "name": self.model
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/pull",
                json=payload,
                timeout=300  # 5 minutes for model pull
            )
            response.raise_for_status()
            return response.json()
