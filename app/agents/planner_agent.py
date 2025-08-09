import logging
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)

class PlannerAgent(BaseAgent):
    """Agent that plans and orchestrates complex analysis tasks"""
    
    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            system_prompt="""You are a planning agent that breaks down complex data analysis tasks into manageable steps.

When given a request:
1. Analyze the complexity and requirements
2. Break down into logical steps
3. Determine which tools and agents are needed
4. Create an execution plan
5. Consider dependencies and data flow

Provide your plan in a structured format that can be executed by other agents."""
        )
        
    async def create_plan(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create execution plan for a request"""
        response = await self.think(request, context)
        
        # Parse plan from response
        plan = self._parse_plan(response.content)
        
        return {
            "original_request": request,
            "plan": plan,
            "complexity": self._assess_complexity(request),
            "estimated_time": self._estimate_time(plan)
        }
    
    def _parse_plan(self, content: str) -> List[Dict[str, Any]]:
        """Parse plan from agent response"""
        # Simple parsing - could be enhanced
        steps = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                steps.append({
                    "step": len(steps) + 1,
                    "description": line[2:].strip(),
                    "tools": self._extract_tools(line),
                    "dependencies": []
                })
        
        return steps
    
    def _extract_tools(self, text: str) -> List[str]:
        """Extract tool names from text"""
        tools = []
        tool_keywords = [
            "load", "analyze", "visualize", "scrape", "query", 
            "describe", "filter", "transform", "merge"
        ]
        
        for keyword in tool_keywords:
            if keyword in text.lower():
                tools.append(keyword)
        
        return tools
    
    def _assess_complexity(self, request: str) -> str:
        """Assess task complexity"""
        complexity_indicators = {
            "simple": ["basic", "simple", "overview", "summary"],
            "medium": ["analysis", "comparison", "trend", "correlation"],
            "complex": ["multiple", "advanced", "predictive", "machine learning"]
        }
        
        request_lower = request.lower()
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in request_lower for indicator in indicators):
                return level
        
        return "medium"
    
    def _estimate_time(self, plan: List[Dict[str, Any]]) -> int:
        """Estimate execution time in minutes"""
        base_time = 2  # Base time per step
        return len(plan) * base_time
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process planning request"""
        return await self.create_plan(
            input_data.get("request", ""),
            input_data.get("context", {})
        )
