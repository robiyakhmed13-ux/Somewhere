from app.moderation.content_filter import rule_filter
from app.moderation.moderation_engine import ModerationResult


def moderate_text(text: str) -> ModerationResult:
    allowed, pattern = rule_filter(text)
    if not allowed:
        return ModerationResult(
            allowed=False,
            risk_type="blocked_phrase",
            risk_score=0.99,
            action="block",
            reason=f"Matched blocked phrase: {pattern}",
        )

    # Placeholder model moderation stage.
    return ModerationResult(
        allowed=True,
        risk_type=None,
        risk_score=0.0,
        action="allow",
    )
