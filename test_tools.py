def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def greet(name: str, loud: bool = False) -> str:
    """Greet someone by name."""
    return name.upper() if loud else name

async def fetch_url(url: str, timeout: int = 10) -> dict:
    """Fetch data from a URL."""
    return {}
