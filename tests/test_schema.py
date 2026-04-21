from py2mcp.parser import FunctionInfo, Parameter
from py2mcp.schema import generate_tool_schema

def test_required_parameter():
    func = FunctionInfo(
        name="search",
        docstring="Search something",
        parameters=[
            Parameter(name="query", type_hint="str", default=None, required=True),
        ],
        return_type="list"
    )
    schema = generate_tool_schema(func)
    assert schema['inputSchema']['required'] == ['query']
    assert schema['inputSchema']['properties']['query']['type'] == 'string'
    assert schema['description'] == "Search something"

def test_optional_with_default():
    func = FunctionInfo(
        name="search",
        docstring=None,
        parameters=[
            Parameter(name="limit", type_hint="int", default=10, required=False),
        ],
        return_type=None
    )
    schema = generate_tool_schema(func)
    assert 'required' not in schema['inputSchema']
    assert schema['inputSchema']['properties']['limit']['type'] == 'integer'
    assert schema['inputSchema']['properties']['limit']['default'] == 10

def test_fallback_to_docstring_types():
    doc = """Do something.
    
    Args:
        name (str): The name.
        age (int): The age.
    """
    func = FunctionInfo(
        name="do_something",
        docstring=doc,
        parameters=[
            # Missing native type hints
            Parameter(name="name", type_hint=None, default=None, required=True),
            Parameter(name="age", type_hint=None, default=None, required=True),
        ],
        return_type=None
    )
    schema = generate_tool_schema(func)
    props = schema['inputSchema']['properties']
    assert props['name']['type'] == 'string'
    assert props['age']['type'] == 'integer'

def test_fallback_to_default_value_type():
    func = FunctionInfo(
        name="do_something",
        docstring=None,
        parameters=[
            Parameter(name="is_active", type_hint=None, default=True, required=False),
            Parameter(name="count", type_hint=None, default=42, required=False),
        ],
        return_type=None
    )
    schema = generate_tool_schema(func)
    props = schema['inputSchema']['properties']
    
    assert props['is_active']['type'] == 'boolean'
    assert props['count']['type'] == 'integer'
    
def test_fallback_to_string_when_unknown():
    func = FunctionInfo(
        name="do_something",
        docstring=None,
        parameters=[
            Parameter(name="mystery", type_hint=None, default=None, required=True),
        ],
        return_type=None
    )
    schema = generate_tool_schema(func)
    assert schema['inputSchema']['properties']['mystery']['type'] == 'string'
