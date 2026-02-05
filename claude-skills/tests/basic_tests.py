#!/usr/bin/env python3
"""
Simple tests for Claude Code Skills.

These tests verify basic functionality without requiring API keys.
"""

import sys
from pathlib import Path

# Add shared tools to path
shared_path = Path(__file__).parent.parent / "shared"
sys.path.insert(0, str(shared_path))


def test_config():
    """Test configuration management."""
    from shared.config import SkillConfig

    # Test get_user_agent (doesn't require API key)
    ua = SkillConfig.get_user_agent()
    assert ua and len(ua) > 0
    print(f"✓ User agent: {ua[:50]}...")


def test_cache():
    """Test cache service."""
    from shared.cache import CacheService, generate_cache_key
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        cache = CacheService(cache_dir=tmpdir)

        # Test set/get
        key = "test_key"
        value = {"test": "data"}

        assert cache.set(key, value, ttl=60)
        retrieved = cache.get(key)
        assert retrieved == value
        print("✓ Cache set/get works")

        # Test generate_cache_key
        key2 = generate_cache_key("http://example.com", "content")
        assert key2 and len(key2) > 0
        print(f"✓ Cache key generation: {key2[:50]}...")

        # Test cache expiration
        assert cache.set("expire_test", {"data": "test"}, ttl=0)
        import time

        time.sleep(0.1)
        assert cache.get("expire_test") is None
        print("✓ Cache expiration works")


def test_json_parser():
    """Test JSON parsing utilities."""
    from shared.json_parser import parse_ai_json_response, safe_parse_json

    # Test parse_ai_json_response
    json_str = '{"title": "Test", "tags": ["a", "b"]}'
    result = parse_ai_json_response(json_str)
    assert result["title"] == "Test"
    assert result["tags"] == ["a", "b"]
    print("✓ JSON parser works (plain JSON)")

    # Test with markdown code block
    json_with_md = '```json\n{"title": "Test"}\n```'
    result = parse_ai_json_response(json_with_md)
    assert result["title"] == "Test"
    print("✓ JSON parser works (markdown)")

    # Test safe_parse_json
    assert safe_parse_json('{"a": 1}', {}) == {"a": 1}
    assert safe_parse_json('invalid', "default") == "default"
    print("✓ Safe JSON parse works")


def test_retry():
    """Test retry decorator."""
    from shared.retry import retry

    attempts = []

    @retry(max_attempts=3, initial_delay=0.01)
    def failing_function():
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("Not yet")
        return "success"

    result = failing_function()
    assert result == "success"
    assert len(attempts) == 3
    print(f"✓ Retry mechanism works (3 attempts)")


def test_imports():
    """Test that all main modules can be imported."""
    # Test shared imports
    from shared import SkillConfig, CacheService, retry, parse_ai_json_response

    print("✓ All shared modules can be imported")

    # Test skill main modules (syntax check only)
    skill_paths = [
        Path(__file__).parent.parent / "extract-metadata" / "main.py",
        Path(__file__).parent.parent / "generate-card" / "main.py",
    ]

    for skill_path in skill_paths:
        assert skill_path.exists()
        # Try to compile (syntax check)
        with open(skill_path) as f:
            code = f.read()
        compile(code, str(skill_path), "exec")
        print(f"✓ {skill_path.parent.name}/main.py syntax OK")


if __name__ == "__main__":
    print("=" * 60)
    print("Claude Code Skills - Basic Tests")
    print("=" * 60)
    print()

    tests = [
        ("Configuration", test_config),
        ("Cache Service", test_cache),
        ("JSON Parser", test_json_parser),
        ("Retry Mechanism", test_retry),
        ("Module Imports", test_imports),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        print(f"\n[Test] {name}")
        print("-" * 60)
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback

            traceback.print_exc()
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)
