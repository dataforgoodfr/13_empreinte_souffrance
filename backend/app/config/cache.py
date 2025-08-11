import json
import time
from dataclasses import dataclass
from threading import Lock
from typing import Any, Optional


@dataclass
class CacheEntry:
    data: Any
    timestamp: float
    ttl_seconds: int

    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl_seconds


class SimpleCache:
    """
    A simple in-memory cache with TTL (Time To Live) support.
    Thread-safe for concurrent access.
    """

    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}
        self._lock = Lock()

    def _generate_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        key_data = {"args": args, "kwargs": kwargs}
        return json.dumps(key_data, sort_keys=True, default=str)

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache if it exists and is not expired."""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None

            if entry.is_expired():
                del self._cache[key]
                return None

            return entry.data

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Set a value in cache with TTL."""
        with self._lock:
            self._cache[key] = CacheEntry(data=value, timestamp=time.time(), ttl_seconds=ttl_seconds)

    def delete(self, key: str) -> bool:
        """Delete a key from cache. Returns True if key existed."""
        with self._lock:
            return self._cache.pop(key, None) is not None

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """Remove expired entries. Returns number of entries removed."""
        with self._lock:
            expired_keys = [key for key, entry in self._cache.items() if entry.is_expired()]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)


# Global cache instance
knowledge_panel_cache = SimpleCache()
