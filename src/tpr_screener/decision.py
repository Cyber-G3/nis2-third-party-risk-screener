from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .models import ControlProfile, ControlState, Level, SupplierProfile
from .risk import RiskAssessment


class Decision(StrEnum):
    APPROVE = "APPROVE"
    APPROVE_WITH_CONDITIONS = "APPROVE_WITH_CONDITIONS"
    ENHANCED_DUE_DILIGENCE = "ENHANCED_DUE_DILIGENCE"
    ESCALATE = "ESCALATE"
    REASSESS = "REASSESS"
    DO_NOT_ONBOARD = "DO_NOT_ONBOARD"


@dataclass(frozen=True)
class DecisionResult:
    decision: Decision
    reason_codes: tuple[str, ...]


def decide_supplier(
    profile: SupplierProfile,
    controls: ControlProfile,
    residual: RiskAssessment,
) -> DecisionResult:
    reasons: list[str] = []

    critical_access_without_mfa = (
        profile.access_level.value in {"PRIVILEGED", "ADMINISTRATIVE"}
        and controls.mfa == ControlState.NO
    )
    critical_service_no_continuity = (
        profile.service_criticality == Level.CRITICAL
        and controls.business_continuity == ControlState.NO
    )

    if residual.score >= 90 and (critical_access_without_mfa or critical_service_no_continuity):
        reasons.append("unacceptable_critical_risk_combination")
        return DecisionResult(Decision.DO_NOT_ONBOARD, tuple(reasons))

    if residual.level == Level.CRITICAL:
        reasons.append("critical_residual_risk")
        return DecisionResult(Decision.ESCALATE, tuple(reasons))

    unknowns = sum(
        value == ControlState.UNKNOWN
        for value in controls.model_dump().values()
    )
    if unknowns >= 6:
        reasons.append("insufficient_control_information")
        return DecisionResult(Decision.REASSESS, tuple(reasons))

    if residual.level == Level.HIGH:
        reasons.append("high_residual_risk")
        return DecisionResult(Decision.ENHANCED_DUE_DILIGENCE, tuple(reasons))

    if residual.level == Level.MEDIUM:
        reasons.append("medium_residual_risk")
        return DecisionResult(Decision.APPROVE_WITH_CONDITIONS, tuple(reasons))

    reasons.append("low_residual_risk")
    return DecisionResult(Decision.APPROVE, tuple(reasons))
