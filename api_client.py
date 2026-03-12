"""REST API client helpers."""
import time
import functools
from typing import Callable, Any


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator: retry a function on failure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator


def build_headers(token: str | None = None, content_type: str = 'application/json') -> dict:
    """Build standard HTTP headers."""
    headers = {'Content-Type': content_type, 'Accept': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers


def paginate(fetch_fn: Callable, page_size: int = 100) -> list:
    """Paginate through API results."""
    results = []
    page = 1
    while True:
        batch = fetch_fn(page=page, per_page=page_size)
        if not batch:
            break
        results.extend(batch)
        if len(batch) < page_size:
            break
        page += 1
    return results
