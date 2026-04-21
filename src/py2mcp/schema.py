from .parser import FunctionInfo, Parameter
from .docstring_parser import extract_types_from_docstring

TYPE_MAP = {
    'str': 'string',
    'int': 'integer',
    'float': 'number',
    'bool': 'boolean',
    'list': 'array',
    'dict': 'object',
    'None': 'null',
    'Any': 'string'
}

def generate_tool_schema(func: FunctionInfo) -> dict:
    """Convert a FunctionInfo into an MCP tool schema."""
    properties = {}
    required = []

    # Get fallback types from docstring if type hints are missing
    docstring_types = extract_types_from_docstring(func.docstring or "")

    for param in func.parameters:
        # Use docstring type if type_hint is missing
        actual_type = param.type_hint
        if not actual_type and param.name in docstring_types:
            actual_type = docstring_types[param.name]

        # Use inferred type from default value if both are missing
        if not actual_type and param.default is not None:
             actual_type = type(param.default).__name__

        prop = _param_to_json_schema(actual_type)
        properties[param.name] = prop

        if param.required:
            required.append(param.name)
        elif param.default is not None:
            prop['default'] = param.default

    schema = {
        'name': func.name,
        'description': func.docstring or f'Call {func.name}',
        'inputSchema': {
            'type': 'object',
            'properties': properties,
        }
    }

    if required:
        schema['inputSchema']['required'] = required

    return schema

def _param_to_json_schema(type_hint: str | None) -> dict:
    if not type_hint:
        return {'type': 'string'}  # fallback

    # Handle generic types: list[str], dict[str, int], Optional[str]
    if type_hint.startswith('list['):
        inner = type_hint[5:-1]
        return {
            'type': 'array',
            'items': {'type': TYPE_MAP.get(inner, 'string')}
        }

    if type_hint.startswith('Optional['):
        inner = type_hint[9:-1]
        return {'type': TYPE_MAP.get(inner, 'string')}

    if type_hint.startswith('dict'):
        return {'type': 'object'}

    base_type = type_hint.split('[')[0]
    return {'type': TYPE_MAP.get(base_type, 'string')}
