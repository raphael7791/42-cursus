"""Prompt value extraction utilities."""

import re
from typing import Optional


def extract_quoted_strings(prompt: str) -> list[str]:
    """Extract strings between quotes from the prompt."""
    matches = re.findall(
        r"'([^']*)'|\"([^\"]*)\"", prompt
    )
    return [
        m[0] or m[1] for m in matches if m[0] or m[1]
    ]


def extract_numbers(prompt: str) -> list[str]:
    """Extract all numbers from the prompt."""
    return re.findall(r"-?\d+\.?\d*", prompt)


def extract_regex_pattern(prompt: str) -> Optional[str]:
    """Map natural language descriptions to regex."""
    lower = prompt.lower()
    if "number" in lower or "digit" in lower:
        return r"\d+"
    if "vowel" in lower:
        return "[aeiouAEIOU]"
    if "space" in lower or "whitespace" in lower:
        return r"\s+"
    if "letter" in lower:
        return "[a-zA-Z]"
    quoted = extract_quoted_strings(prompt)
    for q in quoted:
        if len(q.split()) <= 2:
            return re.escape(q)
    return None


def extract_replacement(prompt: str) -> Optional[str]:
    """Extract replacement from 'with X' pattern."""
    match = re.search(
        r"\bwith\s+(\S+)", prompt, re.IGNORECASE
    )
    if not match:
        return None
    word = match.group(1).strip("'\"")
    mappings = {
        "asterisks": "*",
        "asterisk": "*",
        "stars": "*",
        "underscores": "_",
        "dashes": "-",
        "hyphens": "-",
        "dots": ".",
        "periods": ".",
    }
    return mappings.get(word.lower(), word)


def extract_string_value(
    prompt: str,
    pname: str,
    func_name: str,
) -> Optional[str]:
    """Extract a string parameter value from prompt.

    Returns None if no candidate found (falls back
    to free generation).
    """
    if pname == "regex":
        return extract_regex_pattern(prompt)

    if pname == "replacement":
        return extract_replacement(prompt)

    quoted = extract_quoted_strings(prompt)

    if pname in ("source_string", "s", "query"):
        if quoted:
            return max(quoted, key=len)

    if pname == "template":
        m = re.search(
            r"[Tt]emplate:?\s*(.+)", prompt
        )
        if m:
            return m.group(1).strip()

    if pname in ("path", "file"):
        m = re.search(
            r"((?:/[\w./_-]+)+|[A-Z]:\\[\w.\\_-]+)",
            prompt,
        )
        if m:
            return m.group(1)

    if pname == "encoding":
        m = re.search(
            r"(?:with\s+)?(\S+)\s+encoding",
            prompt, re.IGNORECASE,
        )
        if m:
            return m.group(1)

    if pname == "database":
        m = re.search(
            r"(?:on\s+the\s+)?(\w+)\s+database",
            prompt, re.IGNORECASE,
        )
        if m:
            return m.group(1)

    if pname == "name" and "greet" in func_name.lower():
        words = prompt.strip().split()
        if words:
            return words[-1].strip("'\"")

    if quoted:
        return quoted[0]

    return None
