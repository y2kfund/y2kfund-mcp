"""Base tool class for Y2K Fund MCP tools"""

from typing import Any, Dict, Optional
import httpx
from ..config import API_BASE_URL, API_TIMEOUT, USER_AGENT


class BaseTool:
    """Base class for all Y2K Fund MCP tools"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
    
    @property
    def name(self) -> str:
        """Tool name - must be overridden"""
        raise NotImplementedError
    
    @property
    def description(self) -> str:
        """Tool description - must be overridden"""
        raise NotImplementedError
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        """Tool input schema - must be overridden"""
        raise NotImplementedError
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        """Execute the tool - must be overridden"""
        raise NotImplementedError
    
    async def api_call(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET"
    ) -> Dict[str, Any]:
        """Make HTTP request to Y2K Fund API"""
        url = f"{self.api_base_url}{endpoint}"
        
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
        
        async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
            if method.upper() == "GET":
                response = await client.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, json=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
