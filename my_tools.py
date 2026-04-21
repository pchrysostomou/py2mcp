import asyncio

def search_web(query: str, max_results: int = 5) -> list[str]:
    """Search the web and return results."""
    return [f"Result 1 for {query}", f"Result 2 for {query}"]

def read_file(path: str) -> str:
    """Read a file from disk and return its contents."""
    return f"Contents of {path}"

async def async_fetch_data(url: str, timeout: int = 10) -> dict:
    """
    Fetch data asynchronously from an API.
    
    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.
    """
    await asyncio.sleep(0.1)
    return {"data": f"Data from {url}", "status": 200}
