from datetime import UTC, datetime, timedelta

from tpr_screener.evidence import EvidenceInput, EvidenceQuality, assess_evidence


def test_missing_evidence() -> None:
    assert assess_evidence(EvidenceInput(present=False)).quality == EvidenceQuality.MISSING


def test_not_applicable_is_explicit() -> None:
    result = assess_evidence(EvidenceInput(present=False, applicable=False))
    assert result.quality == EvidenceQuality.NOT_APPLICABLE


def test_stale_evidence() -> None:
    now = datetime(2026, 8, 19, tzinfo=UTC)
    result = assess_evidence(
        EvidenceInput(
            present=True,
            collected_at=now - timedelta(days=91),
            max_age_days=90,
            verified=True,
        ),
        now=now,
    )
    assert result.quality == EvidenceQuality.STALE
    assert result.age_days == 91


def test_verified_evidence() -> None:
    result = assess_evidence(EvidenceInput(present=True, verified=True))
    assert result.quality == EvidenceQuality.VERIFIED
