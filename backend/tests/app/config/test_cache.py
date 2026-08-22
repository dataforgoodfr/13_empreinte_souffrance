from unittest.mock import patch

import pytest

from app.config.cache import CacheEntry, SimpleCache


@pytest.fixture
def cache() -> SimpleCache:
    return SimpleCache()


def test_set_then_get_returns_the_stored_value(cache: SimpleCache):
    cache.set("key", {"foo": "bar"})

    assert cache.get("key") == {"foo": "bar"}


def test_get_missing_key_returns_none(cache: SimpleCache):
    assert cache.get("missing") is None


def test_get_returns_none_and_evicts_an_expired_entry(cache: SimpleCache):
    with patch("app.config.cache.time.time", return_value=1_000.0):
        cache.set("key", "value", ttl_seconds=10)

    with patch("app.config.cache.time.time", return_value=1_011.0):  # 11s later, past the 10s TTL
        assert cache.get("key") is None

    # The expired entry must be dropped from internal storage, not just hidden from get()
    assert "key" not in cache._cache


def test_get_returns_value_just_before_ttl_expires(cache: SimpleCache):
    with patch("app.config.cache.time.time", return_value=1_000.0):
        cache.set("key", "value", ttl_seconds=10)

    with patch("app.config.cache.time.time", return_value=1_009.0):  # 9s later, still within TTL
        assert cache.get("key") == "value"


def test_default_ttl_is_applied_when_not_specified(cache: SimpleCache):
    with patch("app.config.cache.time.time", return_value=1_000.0):
        cache.set("key", "value")

    entry: CacheEntry = cache._cache["key"]
    assert entry.ttl_seconds == 3600


def test_delete_existing_key_returns_true_and_removes_it(cache: SimpleCache):
    cache.set("key", "value")

    assert cache.delete("key") is True
    assert cache.get("key") is None


def test_delete_missing_key_returns_false(cache: SimpleCache):
    assert cache.delete("missing") is False


def test_clear_removes_all_entries(cache: SimpleCache):
    cache.set("a", 1)
    cache.set("b", 2)

    cache.clear()

    assert cache.get("a") is None
    assert cache.get("b") is None


def test_cleanup_expired_removes_only_expired_entries_and_returns_their_count(cache: SimpleCache):
    with patch("app.config.cache.time.time", return_value=1_000.0):
        cache.set("short_lived", "value", ttl_seconds=5)
        cache.set("long_lived", "value", ttl_seconds=1000)

    with patch("app.config.cache.time.time", return_value=1_010.0):  # short_lived is expired, long_lived isn't
        removed_count = cache.cleanup_expired()

        assert removed_count == 1
        assert "short_lived" not in cache._cache
        assert cache.get("long_lived") == "value"


def test_cleanup_expired_with_no_expired_entries_returns_zero(cache: SimpleCache):
    cache.set("key", "value", ttl_seconds=1000)

    assert cache.cleanup_expired() == 0
