"""Positions tool for querying stock positions by symbol"""

import json
from typing import Any, Dict
from .base import BaseTool


class PositionsTool(BaseTool):
    """Tool for getting latest stock positions by symbol"""
    
    @property
    def name(self) -> str:
        return "get_positions"
    
    @property
    def description(self) -> str:
        return (
            "Get latest stock positions by symbol from Y2K Fund accounts. "
            "Returns position data including quantity, market value, unrealized P&L, "
            "average price, and account information (legal entity). "
            "Data is fetched from the most recent snapshot."
        )
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., MSFT, META, AAPL, GOOG, TSLA)",
                },
                "user_id": {
                    "type": "string",
                    "description": "Optional user ID for filtering by user-specific account aliases",
                },
            },
            "required": ["symbol"],
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        """Execute the positions query"""
        symbol = arguments.get("symbol", "").upper()
        user_id = arguments.get("user_id")
        
        if not symbol:
            return "Error: Symbol is required"
        
        try:
            # Build query parameters
            params = {"symbol": symbol}
            if user_id:
                params["user_id"] = user_id
            
            # Make API call
            data = await self.api_call("/query/positions", params=params)
            
            # Format response
            if data.get("success"):
                positions = data.get("positions", [])
                count = data.get("positions_count", 0)
                
                if count == 0:
                    return f"No positions found for symbol: {symbol}"
                
                # Create summary
                result = f"Found {count} position(s) for {symbol}:\n\n"
                
                # Add position details
                for i, pos in enumerate(positions, 1):
                    result += f"Position {i}:\n"
                    result += f"  Account: {pos.get('legal_entity', 'N/A')}\n"
                    result += f"  Quantity: {pos.get('qty', 0):,.0f} shares\n"
                    result += f"  Market Value: ${pos.get('market_value', 0):,.2f}\n"
                    result += f"  Current Price: ${pos.get('price', 0):,.2f}\n"
                    result += f"  Avg Cost: ${pos.get('avgPrice', 0):,.2f}\n"
                    result += f"  Unrealized P&L: ${pos.get('unrealized_pnl', 0):,.2f}\n"
                    result += f"  P&L %: {((pos.get('price', 0) / pos.get('avgPrice', 1) - 1) * 100):.2f}%\n"
                    result += "\n"
                
                # Add totals
                total_qty = sum(p.get('qty', 0) for p in positions)
                total_value = sum(p.get('market_value', 0) for p in positions)
                total_pnl = sum(p.get('unrealized_pnl', 0) for p in positions)
                
                result += f"Total Summary:\n"
                result += f"  Total Shares: {total_qty:,.0f}\n"
                result += f"  Total Market Value: ${total_value:,.2f}\n"
                result += f"  Total Unrealized P&L: ${total_pnl:,.2f}\n"
                
                # Add raw data as JSON for advanced users
                result += f"\nRaw Data (JSON):\n```json\n{json.dumps(positions, indent=2)}\n```"
                
                return result
            else:
                error_msg = data.get("error", "Unknown error")
                return f"Error: {error_msg}"
        
        except Exception as e:
            return f"Error fetching positions: {str(e)}"
