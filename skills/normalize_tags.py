"""Skill: Normalize tags using Claude AI."""
import json
import os
from typing import Dict, List

from anthropic import Anthropic


def normalize_tags(tags: List[str], custom_rules: Dict[str, List[str]] = None) -> List[str]:
    """Normalize tags to consistent format using Claude AI.

    Args:
        tags: List of raw tags
        custom_rules: Optional custom normalization rules

    Returns:
        List of normalized tags (lowercase, standardized)
    """
    # Default normalization rules
    default_rules = {
        "llm": ["llm", "large language model", "大模型", "gpt", "chatgpt", "openai"],
        "kubernetes": ["kubernetes", "k8s", "k8s"],
        "ai": ["ai", "artificial intelligence", "人工智能"],
        "machine_learning": ["machine learning", "ml", "机器学习"],
        "deep_learning": ["deep learning", "dl", "深度学习"],
        "cloud_native": ["cloud native", "云原生"],
        "microservices": ["microservice", "microservices", "微服务"],
        "devops": ["devops", "运维"],
        "security": ["security", "安全"],
        "database": ["database", "db", "数据库"],
        "frontend": ["frontend", "front-end", "前端"],
        "backend": ["backend", "back-end", "后端"],
    }

    rules = custom_rules or default_rules

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = Anthropic(api_key=api_key)

    # Format rules for the prompt
    rules_text = json.dumps(rules, indent=2)

    prompt = f"""You are a tag normalizer. Normalize the following tags to consistent, lowercase formats.

Input tags: {json.dumps(tags)}

Follow these normalization rules (map variants to standard form):
{rules_text}

For each input tag:
1. Check if it matches any variant in the rules (case-insensitive)
2. If matched, use the standard form (the key)
3. If not matched, convert to lowercase and remove special characters
4. Remove duplicates
5. Return 3-7 most relevant tags

Respond ONLY with a JSON array of normalized tags, no additional text.

Example:
Input: ["LLM", "K8s", "Python", "Machine Learning"]
Output: ["llm", "kubernetes", "python", "machine_learning"]"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=1024, messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text

        # Parse JSON response
        try:
            normalized = json.loads(response_text)
        except json.JSONDecodeError:
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                normalized = json.loads(response_text[json_start:json_end].strip())
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.rfind("```")
                normalized = json.loads(response_text[json_start:json_end].strip())
            else:
                # Fallback: simple normalization
                normalized = [tag.lower().replace(" ", "_").replace("-", "_") for tag in tags]

        if not isinstance(normalized, list):
            raise ValueError("Response is not a list")

        return normalized

    except Exception as e:
        # Fallback to simple normalization
        print(f"Warning: AI normalization failed, using simple fallback: {e}")
        return [tag.lower().replace(" ", "_").replace("-", "_") for tag in tags]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python normalize_tags.py tag1 tag2 tag3 ...")
        sys.exit(1)

    tags = sys.argv[1:]

    try:
        normalized = normalize_tags(tags)
        print(json.dumps(normalized, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
