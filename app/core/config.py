from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Ollama Settings
    ollama_host: str = "localhost"
    ollama_port: int = 11434
    ollama_model: str = "llama3.2"
    
    # Agent Settings
    max_iterations: int = 10
    timeout_seconds: int = 300
    
    # Memory Settings
    memory_enabled: bool = True
    max_memory_entries: int = 1000
    
    # Tool Settings
    tool_timeout: int = 60
    max_concurrent_tools: int = 5
    
    # Vector Store Settings
    vector_store_path: str = "./data/vector_store"

settings = Settings()
