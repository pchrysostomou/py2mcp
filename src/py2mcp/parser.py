import ast
from dataclasses import dataclass
from typing import Any

@dataclass
class Parameter:
    name: str
    type_hint: str | None
    default: Any
    required: bool

@dataclass
class FunctionInfo:
    name: str
    docstring: str | None
    parameters: list[Parameter]
    return_type: str | None

def parse_file(filepath: str) -> list[FunctionInfo]:
    """Parse a Python file and extract all public functions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)
    functions = []

    for node in ast.walk(tree):
        # Top-level public functions and async functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith('_'):
            functions.append(_extract_function(node))

    return functions

def _extract_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionInfo:
    docstring = ast.get_docstring(node)

    parameters = []
    args = node.args

    # Align default values from the right side
    defaults_offset = len(args.args) - len(args.defaults)

    for i, arg in enumerate(args.args):
        if arg.arg == 'self':
            continue

        has_default = i >= defaults_offset
        default_value = None

        if has_default:
            default_node = args.defaults[i - defaults_offset]
            default_value = _extract_default(default_node)

        type_hint = None
        if arg.annotation:
            try:
                type_hint = ast.unparse(arg.annotation)
            except Exception:
                pass # Fallback in case of weird annotation formats

        parameters.append(Parameter(
            name=arg.arg,
            type_hint=type_hint,
            default=default_value,
            required=not has_default
        ))

    return_type = None
    if node.returns:
        try:
            return_type = ast.unparse(node.returns)
        except Exception:
            pass

    return FunctionInfo(
        name=node.name,
        docstring=docstring,
        parameters=parameters,
        return_type=return_type
    )

def _extract_default(node: ast.expr) -> Any:
    """Extract the actual value from a default AST node."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.List):
        return []
    if isinstance(node, ast.Dict):
        return {}
    return None
