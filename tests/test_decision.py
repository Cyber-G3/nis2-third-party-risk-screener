from tpr_screener.decision import Decision, decide_supplier
from tpr_screener.models import (
    AccessLevel,
    ControlProfile,
    ControlState,
    DataSensitivity,
    Level,
    SupplierProfile,
    SupplierType,
)
from tpr_screener.risk import RiskAssessment


def profile() -> SupplierProfile:
    return SupplierProfile(
        supplier_id="SUP-002",
        supplier_name="Example MSP",
        supplier_type=SupplierType.MSP,
        service_description="Managed infrastructure support",
        service_criticality=Level.HIGH,
        data_sensitivity=DataSensitivity.CONFIDENTIAL,
        access_level=AccessLevel.PRIVILEGED,
        operational_dependency=Level.HIGH,
    )


def test_high_residual_risk_requires_enhanced_due_diligence() -> None:
    controls = ControlProfile(**{field: ControlState.YES for field in ControlProfile.model_fields})
    result = decide_supplier(profile(), controls, RiskAssessment(70, Level.HIGH, ()))
    assert result.decision == Decision.ENHANCED_DUE_DILIGENCE


def test_many_unknowns_trigger_reassessment() -> None:
    result = decide_supplier(profile(), ControlProfile(), RiskAssessment(45, Level.MEDIUM, ()))
    assert result.decision == Decision.REASSESS


def test_critical_privileged_supplier_without_mfa_can_be_rejected() -> None:
    controls = ControlProfile(mfa=ControlState.NO)
    result = decide_supplier(profile(), controls, RiskAssessment(95, Level.CRITICAL, ()))
    assert result.decision == Decision.DO_NOT_ONBOARD
