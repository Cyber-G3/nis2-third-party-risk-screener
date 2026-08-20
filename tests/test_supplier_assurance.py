from datetime import date, timedelta

from tpr_screener.assurance import (
    EvidenceState,
    ReassessmentTrigger,
    SupplierAssuranceInput,
    SupplierEvidenceRecord,
    assess_supplier_assurance,
)
from tpr_screener.models import (
    DataSensitivity,
    Level,
    SupplierProfile,
    SupplierType,
)


def _supplier(*, criticality: Level = Level.MEDIUM, single_source: bool = False) -> SupplierProfile:
    return SupplierProfile(
        supplier_id="supplier-1",
        supplier_name="Example Supplier",
        supplier_type=SupplierType.SAAS,
        service_description="Example service",
        service_criticality=criticality,
        data_sensitivity=DataSensitivity.CONFIDENTIAL,
        operational_dependency=Level.HIGH,
        single_source=single_source,
    )


def test_expired_evidence_triggers_reassessment_and_remediation() -> None:
    today = date(2026, 8, 20)
    result = assess_supplier_assurance(
        SupplierAssuranceInput(
            supplier=_supplier(),
            evidence=[
                SupplierEvidenceRecord(
                    evidence_id="soc2",
                    evidence_type="assurance-report",
                    title="SOC 2 report",
                    valid_until=today - timedelta(days=1),
                )
            ],
            as_of=today,
        )
    )
    assert result.schema_version == "1.0"
    assert result.evidence_status[0].state is EvidenceState.EXPIRED
    assert ReassessmentTrigger.EVIDENCE_EXPIRED in result.triggers
    assert "SUPPLIER_EVIDENCE_EXPIRED" in result.reason_codes
    assert result.reassessment_required is True
    assert result.remediation_required is True
    assert result.closure_evidence_required is True


def test_critical_single_source_supplier_is_flagged() -> None:
    today = date(2026, 8, 20)
    result = assess_supplier_assurance(
        SupplierAssuranceInput(
            supplier=_supplier(criticality=Level.CRITICAL, single_source=True),
            as_of=today,
        )
    )
    assert ReassessmentTrigger.CRITICAL_SERVICE in result.triggers
    assert ReassessmentTrigger.SINGLE_SOURCE in result.triggers
    assert result.assurance_level is Level.CRITICAL
    assert result.remediation_required is True


def test_expiring_evidence_is_visible_before_expiry_without_forcing_remediation() -> None:
    today = date(2026, 8, 20)
    result = assess_supplier_assurance(
        SupplierAssuranceInput(
            supplier=_supplier(),
            evidence=[
                SupplierEvidenceRecord(
                    evidence_id="iso-cert",
                    evidence_type="certification",
                    title="ISO certificate",
                    valid_until=today + timedelta(days=20),
                )
            ],
            as_of=today,
        )
    )
    assert result.evidence_status[0].state is EvidenceState.EXPIRING
    assert result.assurance_level is Level.MEDIUM
    assert result.remediation_required is False
    assert result.closure_evidence_required is False


def test_supplier_incident_requires_closure_evidence() -> None:
    today = date(2026, 8, 20)
    result = assess_supplier_assurance(
        SupplierAssuranceInput(
            supplier=_supplier(),
            supplier_incident_open=True,
            as_of=today,
        )
    )
    assert ReassessmentTrigger.SUPPLIER_INCIDENT in result.triggers
    assert result.remediation_required is True
    assert result.closure_evidence_required is True
