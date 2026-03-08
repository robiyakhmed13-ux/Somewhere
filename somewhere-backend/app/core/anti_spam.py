def is_repetitive_content(text: str, recent_texts: list[str]) -> bool:
    normalized = " ".join(text.lower().strip().split())
    normalized_recent = [" ".join(t.lower().strip().split()) for t in recent_texts]
    return normalized_recent.count(normalized) >= 2


def too_many_links(text: str) -> bool:
    return text.count("http://") + text.count("https://") > 1


def suspicious_message(text: str, recent_texts: list[str]) -> tuple[bool, str | None]:
    if too_many_links(text):
        return True, "too_many_links"
    if is_repetitive_content(text, recent_texts):
        return True, "repetitive_content"
    return False, None
