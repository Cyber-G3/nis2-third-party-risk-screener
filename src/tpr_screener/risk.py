from __future__ import annotations

from dataclasses import dataclass

from .models import (
    AccessLevel,
    ControlProfile,
    ControlState,
    DataSensitivity,
    Geography,
    Level,
    SupplierProfile,
)


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: Level
    reason_codes: tuple[str, ...]


_LEVEL_SCORE = {Level.LOW: 5, Level.MEDIUM: 12, Level.HIGH: 20, Level.CRITICAL: 30}
_DATA_SCORE = {
    DataSensitivity.NONE: 0,
    DataSensitivity.INTERNAL: 5,
    DataSensitivity.CONFIDENTIAL: 12,
    DataSensitivity.RESTRICTED: 20,
}
_ACCESS_SCORE = {
    AccessLevel.NONE: 0,
    AccessLevel.USER: 6,
    AccessLevel.PRIVILEGED: 16,
    AccessLevel.ADMINISTRATIVE: 22,
}
_CONTROL_CREDIT = {
    ControlState.YES: 1.0,
    ControlState.PARTIAL: 0.5,
    ControlState.NO: 0.0,
    ControlState.UNKNOWN: 0.0,
    ControlState.NOT_APPLICABLE: 0.0,
}


def _level_for(score: int) -> Level:
    if score >= 80:
        return Level.CRITICAL
    if score >= 60:
        return Level.HIGH
    if score >= 35:
        return Level.MEDIUM
    return Level.LOW


def assess_inherent_risk(profile: SupplierProfile) -> RiskAssessment:
    score = 0
    reasons: list[str] = []

    score += _LEVEL_SCORE[profile.service_criticality]
    reasons.append(f"service_criticality:{profile.service_criticality.value.lower()}")

    score += _LEVEL_SCORE[profile.operational_dependency]
    reasons.append(f"operational_dependency:{profile.operational_dependency.value.lower()}")

    score += _DATA_SCORE[profile.data_sensitivity]
    if profile.data_sensitivity != DataSensitivity.NONE:
        reasons.append(f"data_sensitivity:{profile.data_sensitivity.value.lower()}")

    score += _ACCESS_SCORE[profile.access_level]
    if profile.access_level != AccessLevel.NONE:
        reasons.append(f"access_level:{profile.access_level.value.lower()}")

    if profile.internet_dependency:
        score += 8
        reasons.append("internet_dependency")
    if profile.single_source:
        score += 12
        reasons.append("single_source_dependency")
    if profile.subcontractors_used is True:
        score += 5
        reasons.append("subcontractors_used")
    if profile.subcontractors_used is None:
        score += 3
        reasons.append("subcontractor_status_unknown")
    if profile.fourth_party_visibility in {ControlState.NO, ControlState.UNKNOWN}:
        score += 7
        reasons.append("fourth_party_visibility_weak")
    if profile.geography == Geography.THIRD_COUNTRY:
        score += 6
        reasons.append("third_country_exposure")
    elif profile.geography == Geography.UNKNOWN:
        score += 3
        reasons.append("geography_unknown")

    score = min(100, score)
    return RiskAssessment(score=score, level=_level_for(score), reason_codes=tuple(reasons))


def assess_residual_risk(inherent: RiskAssessment, controls: ControlProfile) -> RiskAssessment:
    control_values = [
        controls.mfa,
        controls.privileged_access_management,
        controls.incident_notification_commitment,
        controls.vulnerability_management,
        controls.security_testing,
        controls.encryption,
        controls.backup_recovery,
        controls.business_continuity,
        controls.supplier_monitoring,
        controls.assurance_evidence,
        controls.exit_portability,
        controls.subcontractor_governance,
    ]
    applicable = [value for value in control_values if value != ControlState.NOT_APPLICABLE]
    if not applicable:
        return RiskAssessment(
            score=inherent.score,
            level=inherent.level,
            reason_codes=inherent.reason_codes + ("no_applicable_controls_assessed",),
        )

    effectiveness = sum(_CONTROL_CREDIT[value] for value in applicable) / len(applicable)
    reduction = round(inherent.score * effectiveness * 0.55)
    residual = max(0, inherent.score - reduction)

    reasons = list(inherent.reason_codes)
    reasons.append(f"control_effectiveness:{round(effectiveness * 100)}pct")
    if any(value == ControlState.UNKNOWN for value in applicable):
        reasons.append("control_evidence_unknown")
    if any(value == ControlState.NO for value in applicable):
        reasons.append("control_gaps_present")

    return RiskAssessment(score=residual, level=_level_for(residual), reason_codes=tuple(reasons))
