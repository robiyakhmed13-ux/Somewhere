BANNED_PATTERNS = [
    "kill yourself",
    "i will find you",
    "go die",
]


def rule_filter(text: str) -> tuple[bool, str | None]:
    lowered = text.lower()
    for pattern in BANNED_PATTERNS:
        if pattern in lowered:
            return False, pattern
    return True, None
