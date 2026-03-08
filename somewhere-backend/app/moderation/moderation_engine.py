from dataclasses import dataclass


@dataclass
class ModerationResult:
    allowed: bool
    risk_type: str | None
    risk_score: float
    action: str
    reason: str | None = None
