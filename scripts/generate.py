import threading
from collections import deque
from typing import Any


class TokenBucket:
    """Thread-safe token bucket rate limiter."""

    def __init__(self, rate: float, capacity: float) -> None:
        self._rate = rate
        self._capacity = capacity
        self._tokens = capacity
        self._lock = threading.Lock()
        self._last = __import__("time").monotonic()

    def consume(self, tokens: float = 1.0) -> bool:
        with self._lock:
            now = __import__("time").monotonic()
            self._tokens = min(
                self._capacity,
                self._tokens + (now - self._last) * self._rate,
            )
            self._last = now
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
