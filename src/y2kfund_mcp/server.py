#!/usr/bin/env python3
"""
Y2K Fund MCP Server
Main server entry point
"""

import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import PositionsTool


# Initialize server
app = Server("y2kfund-mcp")

# Initialize tools
positions_tool = PositionsTool()

# Store tools for easy access
TOOLS = {
    positions_tool.name: positions_tool,
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name=tool.name,
            description=tool.description,
            inputSchema=tool.input_schema,
        )
        for tool in TOOLS.values()
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    
    tool = TOOLS[name]
    result = await tool.execute(arguments)
    
    return [TextContent(type="text", text=result)]


async def run_server():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main():
    """Main entry point"""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
