from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class EvidenceQuality(StrEnum):
    VERIFIED = "VERIFIED"
    PRESENT = "PRESENT"
    STALE = "STALE"
    INCOMPLETE = "INCOMPLETE"
    MISSING = "MISSING"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class EvidenceInput:
    present: bool
    applicable: bool = True
    complete: bool = True
    verified: bool = False
    collected_at: datetime | None = None
    max_age_days: int | None = None
    provenance_present: bool = True


@dataclass(frozen=True)
class EvidenceResult:
    quality: EvidenceQuality
    age_days: int | None
    reason_codes: tuple[str, ...]


def assess_evidence(item: EvidenceInput, *, now: datetime | None = None) -> EvidenceResult:
    if not item.applicable:
        return EvidenceResult(EvidenceQuality.NOT_APPLICABLE, None, ("not_applicable",))
    if not item.present:
        return EvidenceResult(EvidenceQuality.MISSING, None, ("missing",))

    reasons: list[str] = []
    age_days: int | None = None
    if not item.complete:
        reasons.append("incomplete")
    if not item.provenance_present:
        reasons.append("provenance_missing")

    if item.collected_at is not None:
        reference = now or datetime.now(UTC)
        collected = item.collected_at
        if collected.tzinfo is None:
            collected = collected.replace(tzinfo=UTC)
        age_days = max(0, (reference - collected).days)
        if item.max_age_days is not None and age_days > item.max_age_days:
            reasons.append("stale")

    if "stale" in reasons:
        quality = EvidenceQuality.STALE
    elif "incomplete" in reasons or "provenance_missing" in reasons:
        quality = EvidenceQuality.INCOMPLETE
    elif item.verified:
        quality = EvidenceQuality.VERIFIED
        reasons.append("verified")
    else:
        quality = EvidenceQuality.PRESENT
        reasons.append("present_unverified")

    return EvidenceResult(quality, age_days, tuple(reasons))
