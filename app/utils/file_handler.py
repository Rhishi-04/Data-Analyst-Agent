import tempfile
import os
import aiofiles
from typing import Dict, Any, List
import logging
from fastapi import UploadFile
import pandas as pd
import json

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
    async def process_uploads(self, files: List[UploadFile]) -> Dict[str, Any]:
        """Process uploaded files and return processed data"""
        processed_files = {}
        
        for file in files:
            if file.filename == "questions.txt":
                content = await file.read()
                processed_files["questions.txt"] = content.decode('utf-8')
            else:
                # Process other files based on extension
                content = await file.read()
                extension = file.filename.split('.')[-1].lower()
                
                if extension in ['csv', 'xlsx', 'json', 'parquet']:
                    processed_files[file.filename] = content
                else:
                    processed_files[file.filename] = content
        
        return processed_files
    
    async def save_temp_file(self, file: UploadFile) -> str:
        """Save uploaded file to temporary location"""
        temp_path = os.path.join(self.temp_dir, file.filename)
        async with aiofiles.open(temp_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        return temp_path
    
    async def load_data_file(self, file_path: str, file_type: str) -> pd.DataFrame:
        """Load data from file based on type"""
        try:
            if file_type == 'csv':
                return pd.read_csv(file_path)
            elif file_type == 'xlsx':
                return pd.read_excel(file_path)
            elif file_type == 'json':
                return pd.read_json(file_path)
            elif file_type == 'parquet':
                return pd.read_parquet(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            logger.error(f"Error loading data file: {str(e)}")
            raise
    
    def cleanup_temp_files(self, file_paths: List[str]) -> None:
        """Clean up temporary files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {file_path}: {str(e)}")
