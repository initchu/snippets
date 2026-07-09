import time
from functools import wraps


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} finished in {elapsed:.4f}s")
        return result
    return wrapper

# 2026-07-09 06:58:58
