from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .models import AccessLevel, DataSensitivity, Level, SupplierProfile


class SupplierTier(StrEnum):
    TIER_1_CRITICAL = "TIER_1_CRITICAL"
    TIER_2_HIGH = "TIER_2_HIGH"
    TIER_3_STANDARD = "TIER_3_STANDARD"
    TIER_4_LOW = "TIER_4_LOW"


@dataclass(frozen=True)
class TieringResult:
    tier: SupplierTier
    score: int
    reason_codes: tuple[str, ...]


def classify_supplier(profile: SupplierProfile) -> TieringResult:
    """Classify supplier criticality without making a legal applicability decision."""
    score = 0
    reasons: list[str] = []

    service_points = {
        Level.LOW: 0,
        Level.MEDIUM: 10,
        Level.HIGH: 22,
        Level.CRITICAL: 35,
    }[profile.service_criticality]
    score += service_points
    reasons.append(f"service_criticality:{profile.service_criticality.value.lower()}")

    dependency_points = {
        Level.LOW: 0,
        Level.MEDIUM: 7,
        Level.HIGH: 15,
        Level.CRITICAL: 25,
    }[profile.operational_dependency]
    score += dependency_points
    reasons.append(f"operational_dependency:{profile.operational_dependency.value.lower()}")

    access_points = {
        AccessLevel.NONE: 0,
        AccessLevel.USER: 7,
        AccessLevel.PRIVILEGED: 18,
        AccessLevel.ADMINISTRATIVE: 25,
    }[profile.access_level]
    score += access_points
    if access_points:
        reasons.append(f"access:{profile.access_level.value.lower()}")

    data_points = {
        DataSensitivity.NONE: 0,
        DataSensitivity.INTERNAL: 4,
        DataSensitivity.CONFIDENTIAL: 10,
        DataSensitivity.RESTRICTED: 17,
    }[profile.data_sensitivity]
    score += data_points
    if data_points:
        reasons.append(f"data:{profile.data_sensitivity.value.lower()}")

    if profile.single_source:
        score += 12
        reasons.append("single_source")
    if profile.internet_dependency:
        score += 5
        reasons.append("internet_dependency")
    if profile.subcontractors_used is True:
        score += 5
        reasons.append("subcontractors_used")
    elif profile.subcontractors_used is None:
        score += 3
        reasons.append("subcontractors_unknown")

    score = min(score, 100)
    if score >= 70:
        tier = SupplierTier.TIER_1_CRITICAL
    elif score >= 45:
        tier = SupplierTier.TIER_2_HIGH
    elif score >= 20:
        tier = SupplierTier.TIER_3_STANDARD
    else:
        tier = SupplierTier.TIER_4_LOW

    return TieringResult(tier=tier, score=score, reason_codes=tuple(reasons))
