"""Utility functions for parsing AI JSON responses."""

import json
import re
from typing import Any, Dict


def parse_ai_json_response(response_text: str) -> Dict[str, Any]:
    """Parse JSON response from AI models with robust error handling.

    This function handles various formats of AI responses:
    - Plain JSON
    - JSON wrapped in markdown code blocks (```json ... ```)
    - JSON embedded in other text

    Args:
        response_text: Raw response text from AI model

    Returns:
        Parsed JSON as a dictionary

    Raises:
        ValueError: If JSON cannot be extracted or parsed
        json.JSONDecodeError: If extracted string is not valid JSON

    Examples:
        >>> response = '{"title": "Test"}'
        >>> parse_ai_json_response(response)
        {'title': 'Test'}

        >>> response = '```json\\n{"title": "Test"}\\n```'
        >>> parse_ai_json_response(response)
        {'title': 'Test'}
    """
    if not response_text or not isinstance(response_text, str):
        raise ValueError(f"Invalid response type: {type(response_text)}")

    # Pattern 1: ```json ... ``` (with json specifier)
    pattern_json = r"```json\s*(.+?)\s*```"
    if match := re.search(pattern_json, response_text, re.DOTALL):
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass  # Try next pattern

    # Pattern 2: ``` ... ``` (without json specifier)
    pattern_code = r"```\s*(.+?)\s*```"
    if match := re.search(pattern_code, response_text, re.DOTALL):
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass  # Try next pattern

    # Pattern 3: Direct JSON parsing
    try:
        return json.loads(response_text.strip())
    except json.JSONDecodeError:
        pass  # Try fallback

    # Pattern 4: Extract JSON object from mixed text
    # Matches from first { to last }
    pattern_object = r"\{.+\}"
    if match := re.search(pattern_object, response_text, re.DOTALL):
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass  # Final fallback

    # All patterns failed
    raise ValueError(
        f"Unable to parse AI response as JSON. "
        f"Response preview (first 200 chars): {response_text[:200]}..."
    )


def safe_parse_json(text: str, default: Any = None) -> Any:
    """Safely parse JSON with fallback to default value.

    Args:
        text: JSON string to parse
        default: Default value if parsing fails

    Returns:
        Parsed JSON object or default value

    Examples:
        >>> safe_parse_json('{"a": 1}', {})
        {'a': 1}
        >>> safe_parse_json('invalid', {})
        {}
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default
