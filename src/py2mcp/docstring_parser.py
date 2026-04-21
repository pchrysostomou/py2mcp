import re

def extract_types_from_docstring(docstring: str) -> dict[str, str]:
    """Extract parameter types from Google-style docstrings."""
    types = {}
    if not docstring:
        return types

    # Google style: param (type): description
    pattern = r'(\w+)\s*\((\w+)\):'
    matches = re.findall(pattern, docstring)

    for param_name, type_name in matches:
        types[param_name] = type_name

    return types
