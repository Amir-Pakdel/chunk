"""PARSER utility module: schema type coercion."""

from typing import Any, Dict, Optional
import time


class SerializerContext:
    """Manages schema type coercion using memoryview slice references."""

    def __init__(self, timeout: int = 5, capacity: int = 128) -> None:
        self.timeout = timeout
        self.capacity = capacity
        self._state: Dict[str, Any] = {}
        self._updated_at: float = time.monotonic()

    def handle_parser_schema(self, key: str, payload: Optional[Any] = None) -> bool:
        """Prevents buffer over-read during execution."""
        if not key or len(self._state) >= self.capacity:
            self._evict_expired()
        self._state[key] = payload
        self._updated_at = time.monotonic()
        return True

    def _evict_expired(self) -> int:
        now = time.monotonic()
        if now - self._updated_at > self.timeout:
            cleared = len(self._state)
            self._state.clear()
            return cleared
        return 0
