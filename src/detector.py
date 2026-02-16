"""Prompt injection detection."""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DetectionResult:
    """Result of prompt injection detection."""

    is_detected: bool
    category: Optional[str] = None
    matches: list[str] = field(default_factory=list)
    score: float = 0.0


INJECTION_PATTERNS = [
    r"\bignore\s+(all\s+)?(previous\s+)?instructions\b",
    r"\bdisregard\s+(all\s+)?(the\s+)?(above\s+)?instructions?\b",
    r"\bnew\s+instructions\b",
    r"\bforget\s+(all\s+)?(your\s+)?instructions\b",
    r"\bignore\s+(all\s+)?(your\s+)?(previous\s+)?(system\s+)?(guidelines|rules|constraints)\b",
    r"\byou\s+(are\s+now|have\s+become)\s+",
    r"\bdo\s+anything\s+(now|mode)\b",
    r"\bno\s+(restrictions?|limitations?|content\s+policy)\b",
    r"\bbypass\s+(your\s+)?safety\b",
    r"\bstay\s+in\s+character\b",
    r"\bdeveloper\s+mode\b",
    r"\bprint\s+out\s+(your\s+)?(system\s+)?prompt\b",
    r"\breveal\s+(your\s+)?(hidden\s+)?(system\s+)?(instructions|prompt)\b",
    r"\brepeat\s+(your\s+)?(system\s+)?prompt\b",
    r"\bwhat\s+are\s+(your\s+)?(hidden\s+)?instructions\b",
    r"\boutput\s+everything\s+between\b",
    r"\blist\s+(them\s+)?all\b.*instructions",
    r"\bpretend\s+(to\s+be|you\s+are)\b",
    r"\bactivat(ed|ing)\s+(DAN|jailbreak)\b",
]

PATTERNS_BY_CATEGORY = {
    "injection": [
        r"\bignore\s+(all\s+)?(previous\s+)?instructions\b",
        r"\bdisregard\s+(all\s+)?(the\s+)?(above\s+)?instructions?\b",
        r"\bnew\s+instructions\b",
        r"\bforget\s+(all\s+)?(your\s+)?instructions\b",
        r"\bignore\s+(all\s+)?(your\s+)?(previous\s+)?(system\s+)?(guidelines|rules|constraints)\b",
    ],
    "jailbreak": [
        r"\bdo\s+anything\s+(now|mode)\b",
        r"\bno\s+(restrictions?|limitations?|content\s+policy)\b",
        r"\bbypass\s+(your\s+)?safety\b",
        r"\bstay\s+in\s+character\b",
        r"\bdeveloper\s+mode\b",
        r"\bpretend\s+(to\s+be|you\s+are)\b",
        r"\b(DAN|jailbreak)\s+(mode\s+)?(activat(ed|ing)|enable(d|ing)?)\b",
        r"\byou\s+(are\s+now|have\s+become)\s+",
    ],
    "extraction": [
        r"\b(print|output|reveal)\s+(out\s+)?(your\s+)?(\w+\s+)?(system\s+)?prompt\b",
        r"\breveal\s+(your\s+)?(hidden\s+)?(system\s+)?(instructions|prompt)\b",
        r"\brepeat\s+(your\s+)?(system\s+)?prompt\b",
        r"\bwhat\s+are\s+(your\s+)?(hidden\s+)?instructions\b",
        r"\boutput\s+everything\s+between\b",
        r"\blist\s+(them\s+)?all\b.*instructions",
    ],
}


def detect_injection(text: str) -> DetectionResult:
    """Detect prompt injection patterns in text.

    Args:
        text: The text to analyze.

    Returns:
        DetectionResult with detection status and details.
    """
    if not text:
        return DetectionResult(is_detected=False)

    text_lower = text.lower()
    matches: list[str] = []
    category_scores = {"injection": 0, "jailbreak": 0, "extraction": 0}

    for category, patterns in PATTERNS_BY_CATEGORY.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches.append(pattern)
                category_scores[category] += 1

    total_matches = len(matches)
    if total_matches == 0:
        return DetectionResult(is_detected=False)

    max_category = max(category_scores, key=lambda k: category_scores.get(k, 0))
    category = max_category if category_scores[max_category] > 0 else None
    score = min(total_matches / 3.0, 1.0)

    return DetectionResult(
        is_detected=True,
        category=category,
        matches=matches,
        score=score,
    )
