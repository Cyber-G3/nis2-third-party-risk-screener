from tpr_screener.models import (
    AccessLevel,
    ControlProfile,
    ControlState,
    DataSensitivity,
    Geography,
    Level,
    SupplierProfile,
    SupplierType,
)
from tpr_screener.risk import assess_inherent_risk, assess_residual_risk


def critical_supplier() -> SupplierProfile:
    return SupplierProfile(
        supplier_id="SUP-001",
        supplier_name="Critical SaaS",
        supplier_type=SupplierType.SAAS,
        service_description="Critical business platform",
        service_criticality=Level.CRITICAL,
        data_sensitivity=DataSensitivity.RESTRICTED,
        access_level=AccessLevel.PRIVILEGED,
        operational_dependency=Level.CRITICAL,
        internet_dependency=True,
        single_source=True,
        subcontractors_used=True,
        fourth_party_visibility=ControlState.UNKNOWN,
        geography=Geography.THIRD_COUNTRY,
    )


def test_critical_supplier_reaches_critical_inherent_risk() -> None:
    result = assess_inherent_risk(critical_supplier())
    assert result.score == 100
    assert result.level == Level.CRITICAL
    assert "single_source_dependency" in result.reason_codes


def test_strong_controls_reduce_residual_risk() -> None:
    inherent = assess_inherent_risk(critical_supplier())
    controls = ControlProfile(**{field: ControlState.YES for field in ControlProfile.model_fields})
    residual = assess_residual_risk(inherent, controls)
    assert residual.score == 45
    assert residual.level == Level.MEDIUM


def test_unknown_controls_do_not_create_false_risk_reduction() -> None:
    inherent = assess_inherent_risk(critical_supplier())
    residual = assess_residual_risk(inherent, ControlProfile())
    assert residual.score == inherent.score
    assert "control_evidence_unknown" in residual.reason_codes


def test_not_applicable_controls_are_excluded() -> None:
    inherent = assess_inherent_risk(critical_supplier())
    controls = ControlProfile(**{field: ControlState.NOT_APPLICABLE for field in ControlProfile.model_fields})
    residual = assess_residual_risk(inherent, controls)
    assert residual.score == inherent.score
    assert "no_applicable_controls_assessed" in residual.reason_codes
