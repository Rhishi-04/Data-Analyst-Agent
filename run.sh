#!/bin/bash

# Check if Ollama is running
echo "Checking Ollama status..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Ollama is not running. Please start Ollama first:"
    echo "  ollama serve"
    exit 1
fi

# Check if model is available
MODEL=${OLLAMA_MODEL:-llama3.2}
echo "Checking if model '$MODEL' is available..."
if ! curl -s http://localhost:11434/api/tags | grep -q "$MODEL"; then
    echo "Model '$MODEL' not found. Pulling..."
    ollama pull $MODEL
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "Starting Data Analyst Agent..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
