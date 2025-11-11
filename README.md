# Y2K Fund MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Model Context Protocol (MCP) server for querying Y2K Fund trading data directly in Claude Desktop. Get real-time positions, market prices, options data, and more.

## Features

### Available Tools

- **`get_positions`** - Query latest stock positions by symbol
  - Returns quantity, market value, unrealized P&L, average cost
  - Shows data across all accounts with legal entity information

### Coming Soon

- `get_market_price` - Real-time market prices
- `get_call_options` - Call options data and analysis
- `get_put_options` - Put options data and analysis
- `get_trades` - Historical trade data
- `get_margin_impact` - Margin requirements and impact

## Installation

### Prerequisites

- Python 3.10 or higher
- [Claude Desktop](https://claude.ai/download) installed
- `uvx` (comes with [uv](https://github.com/astral-sh/uv)) or `pip`

### Quick Install (Recommended)

1. **Install via Claude Desktop Config**

   Open your Claude Desktop configuration file:
   
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add Y2K Fund MCP Server**

   ```json
   {
     "mcpServers": {
       "y2kfund": {
         "command": "uvx",
         "args": [
           "--from",
           "git+https://github.com/y2kfund/y2kfund-mcp",
           "y2kfund-mcp"
         ]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

   The server will auto-install on first use.

### Alternative: Manual Installation

```bash
# Install from GitHub
pip install git+https://github.com/y2kfund/y2kfund-mcp.git

# Or clone and install locally
git clone https://github.com/y2kfund/y2kfund-mcp.git
cd y2kfund-mcp
pip install -e .
```

Then update your Claude config to use the direct command:

```json
{
  "mcpServers": {
    "y2kfund": {
      "command": "y2kfund-mcp"
    }
  }
}
```

## Usage

Once installed, you can ask Claude natural language questions:

### Example Queries

**Get Positions:**
```
"Get my MSFT positions"
"Show positions for META"
"What are my AAPL holdings?"
```

**Analyze Positions:**
```
"Show me all my TSLA positions and calculate the total P&L"
"Compare my MSFT and GOOG positions"
"What's my biggest position loss?"
```

## Tool Reference

### `get_positions`

Get latest stock positions by symbol from Y2K Fund accounts.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Stock ticker symbol (e.g., MSFT, META, AAPL) |

**Example Response:**

```
Found 2 position(s) for MSFT:

Position 1:
  Account: Y2K Fund LLC
  Quantity: 1,500 shares
  Market Value: $758,637.41
  Current Price: $505.76
  Avg Cost: $523.13
  Unrealized P&L: -$26,053.08
  P&L %: -3.32%

Position 2:
  Account: Y2K Fund LP
  Quantity: 10,055 shares
  Market Value: $5,085,238.31
  Current Price: $505.74
  Avg Cost: $521.05
  Unrealized P&L: -$153,943.86
  P&L %: -2.95%

Total Summary:
  Total Shares: 11,555
  Total Market Value: $5,843,875.72
  Total Unrealized P&L: -$179,996.94
```

## API Endpoint

This MCP server connects to: `https://ibkr-data-fetch.y2k.fund`

The API is publicly accessible and returns real-time data from Y2K Fund's trading accounts.

## Development

### Project Structure

```
y2kfund-mcp/
├── src/
│   └── y2kfund_mcp/
│       ├── __init__.py
│       ├── server.py          # Main MCP server
│       ├── config.py          # API configuration
│       └── tools/
│           ├── __init__.py
│           ├── base.py        # Base tool class
│           └── positions.py   # Positions tool
├── examples/
│   └── claude_config.json     # Example configuration
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

### Adding New Tools

1. Create a new tool file in `src/y2kfund_mcp/tools/`
2. Inherit from `BaseTool`
3. Implement required properties and `execute()` method
4. Register in `src/y2kfund_mcp/server.py`

Example:

```python
# tools/market_price.py
from .base import BaseTool

class MarketPriceTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_market_price"
    
    @property
    def description(self) -> str:
        return "Get current market price for a symbol"
    
    @property
    def input_schema(self):
        return {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            },
            "required": ["symbol"]
        }
    
    async def execute(self, arguments):
        data = await self.api_call("/query/price", params=arguments)
        return f"Price: ${data['price']}"
```

### Running Locally

```bash
# Clone the repo
git clone https://github.com/y2kfund/y2kfund-mcp.git
cd y2kfund-mcp

# Install dependencies
pip install -e .

# Run the server
python -m y2kfund_mcp.server
```

## Troubleshooting

### "Server not responding"

1. Check Claude Desktop logs:
   - **macOS**: `~/Library/Logs/Claude/mcp*.log`
   - **Windows**: `%APPDATA%\Claude\Logs\mcp*.log`

2. Verify installation:
   ```bash
   uvx --from git+https://github.com/y2kfund/y2kfund-mcp y2kfund-mcp --version
   ```

3. Test API endpoint:
   ```bash
   curl "https://ibkr-data-fetch.y2k.fund/query/positions?symbol=MSFT"
   ```

### "Unknown tool" error

Make sure you've restarted Claude Desktop after updating the configuration.

### API Connection Issues

The server requires internet access to connect to `https://ibkr-data-fetch.y2k.fund`. Check your firewall settings.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/y2kfund/y2kfund-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/y2kfund/y2kfund-mcp/discussions)
- **Website**: [https://y2k.fund](https://y2k.fund)

## Changelog

### v1.0.0 (2025-11-11)

- Initial release
- Added `get_positions` tool for querying stock positions
- Support for user-specific account aliases
- Comprehensive P&L calculations and summaries

---

**Made with ❤️ by Y2K Fund**
