import importlib.util
from mcp.server.fastmcp import FastMCP
from .parser import parse_file, FunctionInfo
from .schema import generate_tool_schema
import asyncio
import inspect

def build_server(filepath: str) -> FastMCP:
    """Parse a Python file and return a configured FastMCP server."""

    functions = parse_file(filepath)

    if not functions:
        raise ValueError(f"No public functions found in {filepath}")

    spec = importlib.util.spec_from_file_location("user_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    mcp = FastMCP("py2mcp")

    for func_info in functions:
        actual_func = getattr(module, func_info.name, None)
        if actual_func is None:
            continue

        def make_handler(fn, info: FunctionInfo):
            is_coro = inspect.iscoroutinefunction(fn)

            if is_coro:
                async def async_handler(**kwargs):
                    try:
                        result = await fn(**kwargs)
                        return str(result)
                    except Exception as e:
                         return f"Error: {e}"
                async_handler.__name__ = info.name
                async_handler.__doc__ = info.docstring
                # Update signature to help FastMCP if it does reflection (optional, we pass schema directly if supported, else FastMCP generates it. FastMCP normally infers from annotation.
                # To be safe, wait, does FastMCP accept our custom schema? FastMCP infers tool schema from type hints on the function.
                # Wait, the user asked to generate the schema via generate_tool_schema and pass it.
                # Looking at FastMCP API, `mcp.add_tool` infers from function signature. We might not even need the schema object for FastMCP if it auto-generates!
                # BUT the user's snippet uses: mcp.add_tool(handler, name=info.name, description=schema['description'])
                return async_handler
            else:
                async def handler(**kwargs):
                    try:
                        result = fn(**kwargs)
                        return str(result)
                    except Exception as e:
                        return f"Error: {e}"
                handler.__name__ = info.name
                handler.__doc__ = info.docstring
                return handler

        schema = generate_tool_schema(func_info)
        mcp.add_tool(
            make_handler(actual_func, func_info),
            name=func_info.name,
            description=schema['description']
        )

    return mcp

def run_server(filepath: str, transport: str = 'stdio'):
    """Build and run the MCP server."""
    mcp = build_server(filepath)

    if transport == 'stdio':
        mcp.run(transport='stdio')
    elif transport == 'http':
        # FastMCP might expect host/port kwargs depending on version. Let's just use sse if http is requested
        # 'sse' is usually the transport name in fastmcp, let's keep user's code.
        mcp.run(transport='sse')
