# Agentic Data Analyst API

A modern, open-source data analytics agent powered by Ollama and agentic AI principles. This system provides dynamic, intelligent data analysis without hardcoded task types.

## Features

- **Agentic AI**: Autonomous agents that can reason and plan
- **Dynamic Tool Discovery**: No hardcoded task types - tools are discovered and used dynamically
- **Open Source**: Uses Ollama for local LLM inference
- **Natural Language Processing**: Ask questions in plain English
- **Flexible Architecture**: Easy to extend with new capabilities
- **Memory System**: Maintains context across interactions

## Architecture

```
app/
├── agents/           # Agentic AI components
├── tools/            # Dynamic tool system
├── llm/              # Ollama integration
├── api/              # REST API endpoints
└── core/             # Configuration
```

## Quick Start

### Prerequisites

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama**:
   ```bash
   ollama serve
   ```

3. **Pull a model** (e.g., llama3.2):
   ```bash
   ollama pull llama3.2
   ```

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd data-analyst-agent
   chmod +x run.sh
   ./run.sh
   ```

2. **Manual setup**:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

## Usage

### API Endpoints

#### Analyze Data
```bash
curl -X POST http://localhost:8000/api/v2/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Analyze the sales data and show me trends over time",
    "files": {
      "sales_data.csv": "/path/to/sales_data.csv"
    }
  }'
```

#### List Available Tools
```bash
curl http://localhost:8000/tools
```

### Example Requests

1. **Basic Analysis**:
   ```json
   {
     "request": "Load my CSV file and give me a summary of the data"
   }
   ```

2. **Advanced Analysis**:
   ```json
   {
     "request": "Find correlations between customer age and purchase amount, then create a visualization"
   }
   ```

3. **Web Scraping**:
   ```json
   {
     "request": "Scrape product prices from this website and analyze the data"
   }
   ```

## Configuration

Create a `.env` file:

```bash
# Ollama settings
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
OLLAMA_MODEL=llama3.2

# API settings
API_HOST=0.0.0.0
API_PORT=8000

# Agent settings
MAX_ITERATIONS=10
TIMEOUT_SECONDS=300
```

## Development

### Adding New Tools

Create a new tool in `app/tools/`:

```python
from app.tools.base_tool import BaseTool, ToolResult, ToolMetadata

class MyCustomTool(BaseTool):
    def _get_metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="my_custom_tool",
            description="Description of what this tool does",
            parameters={"param1": {"type": "string", "description": "Parameter description"}},
            required=["param1"]
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        # Your tool logic here
        return ToolResult(success=True, data={"result": "success"})
```

### Adding New Agents

Create a new agent in `app/agents/`:

```python
from app.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CustomAgent",
            system_prompt="Your agent instructions here"
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Your agent logic here
        pass
```

## Docker Support

```bash
docker build -t agentic-data-analyst .
docker run -p 8000:8000 -e OLLAMA_HOST=host.docker.internal agentic-data-analyst
```

## Troubleshooting

### Common Issues

1. **Ollama not running**:
   ```bash
   ollama serve
   ```

2. **Model not found**:
   ```bash
   ollama pull llama3.2
   ```

3. **Port conflicts**:
   - Change port in `.env` file
   - Use `lsof -ti:8000 | xargs kill -9` to free port

## License

MIT License - see LICENSE file for details.
