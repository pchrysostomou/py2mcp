import ast
from pathlib import Path

def validate_file(filepath: str) -> list[str]:
    """Validate a Python file before processing. Returns list of errors."""
    errors = []
    path = Path(filepath)

    if not path.exists():
        errors.append(f"File not found: {filepath}")
        return errors  # Early exit

    if path.suffix != '.py':
        errors.append(f"Expected .py file, got: {path.suffix}")

    try:
        source = path.read_text(encoding='utf-8')
        tree = ast.parse(source)
    except SyntaxError as e:
        errors.append(f"Syntax error in {filepath}: {e}")
        return errors

    if not errors:
        public_funcs = [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith('_')
        ]
        if not public_funcs:
            errors.append(f"No public functions found in {filepath}")

    return errors
