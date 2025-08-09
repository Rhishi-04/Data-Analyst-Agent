import json
import logging
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentResponse
from app.tools.registry import tool_manager

logger = logging.getLogger(__name__)

class DataAnalystAgent(BaseAgent):
    """Main agent for data analysis tasks"""
    
    def __init__(self):
        super().__init__(
            name="DataAnalystAgent",
            system_prompt="""You are an expert data analyst agent. You can understand natural language requests and use various tools to analyze data, create visualizations, scrape web data, and provide insights.

Available tools:
- load_data: Load data from files (CSV, Excel, JSON, Parquet)
- analyze_data: Perform statistical analysis and generate insights
- visualize_data: Create charts and visualizations
- scrape_web: Extract data from web pages
- query_data: Query and filter datasets
- describe_data: Get data overview and statistics

When given a request:
1. Understand what the user wants to achieve
2. Determine which tools are needed
3. Use tools with appropriate parameters
4. Provide comprehensive analysis and insights
5. Explain your reasoning and findings

Use @tool_name(parameters) format to call tools."""
        )
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data analysis request"""
        user_request = input_data.get("request", "")
        files = input_data.get("files", {})
        
        # Build context
        context = {
            "available_files": list(files.keys()),
            "user_request": user_request
        }
        
        # Get agent response
        response = await self.think(user_request, context)
        
        # Execute any tool calls
        results = []
        for tool_call in response.tool_calls:
            tool_name = tool_call.get("tool")
            parameters = tool_call.get("parameters", {})
            
            tool = tool_manager.registry.get_tool(tool_name)
            if tool:
                if files and "file_path" not in parameters:
                    # Auto-detect file to use
                    for filename, filepath in files.items():
                        if any(ext in filename.lower() for ext in ['.csv', '.xlsx', '.json']):
                            parameters["file_path"] = filepath
                            break
                
                result = await tool.execute(parameters)
                results.append({
                    "tool": tool_name,
                    "parameters": parameters,
                    "result": result.dict()
                })
        
        # Generate final response
        final_response = await self._generate_final_response(
            user_request, results, files
        )
        
        return {
            "request": user_request,
            "analysis": final_response,
            "tool_results": results,
            "metadata": {
                "agent": self.name,
                "tools_used": len(results),
                "files_processed": len(files)
            }
        }
    
    async def _generate_final_response(
        self, 
        original_request: str, 
        tool_results: List[Dict[str, Any]], 
        files: Dict[str, Any]
    ) -> str:
        """Generate final analysis based on tool results"""
        
        context = {
            "original_request": original_request,
            "tool_results": tool_results,
            "files_processed": list(files.keys())
        }
        
        summary_prompt = f"""
Based on the analysis performed, provide a comprehensive summary of findings.
Original request: {original_request}
Tool results: {json.dumps(tool_results, indent=2)}
Files processed: {list(files.keys())}

Provide insights, key findings, and actionable recommendations.
"""
        
        response = await self.think(summary_prompt, context)
        return response.content
