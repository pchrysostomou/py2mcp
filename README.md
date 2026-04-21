<div align="center">

# py2mcp

**Turn any Python file into an MCP server automatically.**

[![PyPI version](https://img.shields.io/pypi/v/py2mcp.svg)](https://pypi.org/project/py2mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/py2mcp.svg)](https://pypi.org/project/py2mcp/)
[![CI](https://github.com/yourusername/py2mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/py2mcp/actions)

<img src="./demo.gif" alt="py2mcp demonstration" width="800">

*(Add your VHS terminal GIF here!)*

</div>

## The Problem

Building an [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol) tool server usually involves writing massive amounts of JSON Schema boilerplate and configuration, even for simple scripts. You spend more time writing protocol handlers than actual logic.

**py2mcp** solves this instantly. You write the Python function — we generate the schema, start the server, and bridge the data automatically via AST parsing.

## Installation

```bash
pip install py2mcp
```

## How It Works: Before & After

**Before py2mcp:** Writing 80 lines of nested JSON Schemas, FastMCP app decorators, and async wrappers just to expose two functions to Claude Desktop.

**After py2mcp:** You just write normal Python.

```python
# tools.py
import requests

def search_wikipedia(query: str, limit: int = 5) -> list[str]:
    """Search Wikipedia and return article titles."""
    # your logic here...

async def execute_sql(query: str) -> dict:
    """Run an async SQL query on the database."""
    # your logic here...
```

Run the magic command:

```bash
$ py2mcp tools.py

✓ Parsed 2 functions from tools.py
  • search_wikipedia
  • execute_sql
✓ Starting MCP server (stdio)
```

And your tools are immediately available to Claude, Cursor, and VS Code!

## Client Configuration (Claude Desktop)

To use your Python file directly with Claude Desktop, just add this snippet to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my_python_tools": {
      "command": "py2mcp",
      "args": [
        "/absolute/path/to/your/tools.py"
      ]
    }
  }
}
```

## Features

- **No decorator boilerplate:** The AST parser reads `def` and `async def` signatures natively.
- **Smart Type Inference:** Translates Python type hints (like `list[str]`) directly to JSON Schema Arrays.
- **Docstring Fallback:** Parses Google-style or Sphinx docstrings to deduce schemas if native hints are missing.
- **Async Native:** Fully supports async I/O bounded tool functions.
- **Preview Output:** Use `py2mcp --dry-run tools.py` to inspect the generated JSON schema without starting the server.

## License

MIT
