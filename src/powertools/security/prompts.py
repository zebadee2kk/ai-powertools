"""
ai_powertools.security.prompts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lightweight helpers to enforce prompt‑safety rules before sending requests to
LLM providers.

Intended usage:

    from powertools.security.prompts import sanitize_prompt, check_prompt_safe, is_path_blocked

    safe_prompt = sanitize_prompt(raw_prompt)
    check_prompt_safe(safe_prompt, context="lodestar.routing")
    client.complete(safe_prompt)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


# Common secret patterns (simple heuristics, not exhaustive)
SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key[\s:=]+[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)secret[\s:=]+[A-Za-z0-9_\-]{16,}"),
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),  # Generic key-like prefix
]

# Paths that should never be sent to cloud providers
DEFAULT_BLOCKED_PATHS = [
    "secrets/",
    "infra/",
    "vault/",
    ".github/",
    "*.pem",
    "*.key",
    "*.crt",
    "*.pfx",
]


@dataclass
class PromptSafetyResult:
    has_secret: bool
    secret_matches: List[str]


def _match_secret_patterns(text: str) -> List[str]:
    matches: List[str] = []
    for pattern in SECRET_PATTERNS:
        for m in pattern.findall(text):
            snippet = str(m)
            if len(snippet) > 80:
                snippet = snippet[:77] + "..."
            matches.append(snippet)
    return matches


def sanitize_prompt(prompt: str) -> str:
    """Apply light scrubbing to a prompt.

    This does NOT guarantee removal of all secrets, but can remove obvious
    private key blocks and reduce accidental leaks.
    """

    # Remove full private key blocks
    prompt = re.sub(
        r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC )?PRIVATE KEY-----",
        "[REDACTED_PRIVATE_KEY]",
        prompt,
        flags=re.MULTILINE,
    )
    return prompt


def check_prompt_safe(prompt: str, *, context: str = "") -> PromptSafetyResult:
    """Check a prompt for obvious secrets.

    Raise a ValueError if secrets are detected so callers can fail closed.
    """

    matches = _match_secret_patterns(prompt)
    if matches:
        raise ValueError(
            f"Potential secrets detected in prompt (context={context}): "
            f"{len(matches)} matches. Aborting API call."
        )
    return PromptSafetyResult(has_secret=False, secret_matches=[])


def is_path_blocked(
    path: str | Path, blocked_patterns: Iterable[str] | None = None
) -> bool:
    """Return True if the given path should never be sent to a cloud LLM.

    Very simple glob‑like checks; callers are expected to enforce this before
    reading/sending file contents.
    """

    blocked_patterns = list(blocked_patterns or DEFAULT_BLOCKED_PATHS)
    path_str = str(path)

    for pattern in blocked_patterns:
        # Naive directory prefix check
        if pattern.endswith("/") and pattern in path_str:
            return True
        # Very simple suffix check for extensions
        if pattern.startswith("*.") and path_str.endswith(pattern[1:]):
            return True
    return False
