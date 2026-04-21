import pytest
from py2mcp.parser import parse_file

def test_parse_simple_function(tmp_path):
    source = '''
def greet(name: str, loud: bool = False) -> str:
    """Greet someone by name."""
    pass
'''
    f = tmp_path / "tools.py"
    f.write_text(source)

    functions = parse_file(str(f))

    assert len(functions) == 1
    assert functions[0].name == "greet"
    assert functions[0].docstring == "Greet someone by name."
    assert len(functions[0].parameters) == 2
    
    assert functions[0].parameters[0].name == "name"
    assert functions[0].parameters[0].type_hint == "str"
    assert functions[0].parameters[0].required == True
    
    assert functions[0].parameters[1].name == "loud"
    assert functions[0].parameters[1].type_hint == "bool"
    assert functions[0].parameters[1].required == False
    assert functions[0].parameters[1].default == False

def test_parse_async_function(tmp_path):
    source = '''
async def fetch_data(url: str):
    pass
'''
    f = tmp_path / "tools.py"
    f.write_text(source)
    functions = parse_file(str(f))
    
    assert len(functions) == 1
    assert functions[0].name == "fetch_data"
    assert functions[0].parameters[0].name == "url"

def test_skip_private_functions(tmp_path):
    source = '''
def public_func(): pass
def _private_func(): pass
async def async_public(): pass
async def _async_private(): pass
'''
    f = tmp_path / "tools.py"
    f.write_text(source)
    functions = parse_file(str(f))
    
    assert len(functions) == 2
    assert {"public_func", "async_public"} == {f.name for f in functions}

def test_missing_type_hints(tmp_path):
    source = '''
def untyped(param1, param2=10): pass
'''
    f = tmp_path / "tools.py"
    f.write_text(source)
    functions = parse_file(str(f))
    
    assert len(functions) == 1
    p1 = functions[0].parameters[0]
    p2 = functions[0].parameters[1]
    
    assert p1.type_hint is None
    assert p1.required == True
    
    assert p2.type_hint is None
    assert p2.required == False
    assert p2.default == 10

def test_empty_file(tmp_path):
    f = tmp_path / "empty.py"
    f.write_text("# Just comments\n")
    functions = parse_file(str(f))
    assert len(functions) == 0
