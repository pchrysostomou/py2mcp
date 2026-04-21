import click
import sys
import json
from .runner import run_server
from .parser import parse_file
from .schema import generate_tool_schema
from .validator import validate_file

@click.group(invoke_without_command=True)
@click.argument('filepath', required=False)
@click.option('--transport', default='stdio',
              type=click.Choice(['stdio', 'http', 'sse']),
              help='Transport protocol')
@click.option('--dry-run', is_flag=True,
              help='Show generated schema without starting server')
@click.pass_context
def cli(ctx, filepath, transport, dry_run):
    """Convert any Python file into an MCP server."""

    if ctx.invoked_subcommand:
        return

    if not filepath:
        click.echo(ctx.get_help())
        sys.exit(0)

    errors = validate_file(filepath)
    if errors:
        for error in errors:
             click.echo(f"✗ {error}", err=True)
        sys.exit(1)

    if dry_run:
        functions = parse_file(filepath)
        schemas = [generate_tool_schema(f) for f in functions]
        click.echo(json.dumps(schemas, indent=2))
        return

    functions = parse_file(filepath)
    click.echo(f"✓ Parsed {len(functions)} functions from {filepath}", err=True)

    names = [f.name for f in functions]
    for name in names:
        click.echo(f"  • {name}", err=True)

    click.echo(f"✓ Starting MCP server ({transport})", err=True)
    click.echo("", err=True)

    if transport == 'stdio':
        click.echo("Add to your MCP config:", err=True)
        click.echo(json.dumps({
            "mcpServers": {
                "my_tools": {
                    "command": "py2mcp",
                    "args": [filepath]
                }
            }
        }, indent=2), err=True)
        click.echo("", err=True)

    # Use sse instead of http for fastmcp if 'http' is chosen. FastMCP uses 'sse'
    if transport == 'http':
        transport = 'sse'
        
    run_server(filepath, transport)

@cli.command()
@click.argument('filepath')
def inspect(filepath):
    """Show what tools would be generated from a file."""
    errors = validate_file(filepath)
    if errors:
        for error in errors:
             click.echo(f"✗ {error}", err=True)
        sys.exit(1)
        
    functions = parse_file(filepath)
    schemas = [generate_tool_schema(f) for f in functions]
    click.echo(json.dumps(schemas, indent=2))

def main():
    cli()
