from tpr_screener.assessment import assess_supplier
from tpr_screener.contract import ClauseState, ContractClause
from tpr_screener.models import (
    AccessLevel,
    ControlProfile,
    ControlState,
    DataSensitivity,
    Level,
    SupplierAssessmentInput,
    SupplierProfile,
    SupplierType,
)
from tpr_screener.tiering import SupplierTier


def test_end_to_end_assessment() -> None:
    result = assess_supplier(
        SupplierAssessmentInput(
            profile=SupplierProfile(
                supplier_id="sup-1",
                supplier_name="Critical SaaS",
                supplier_type=SupplierType.SAAS,
                service_description="Production platform",
                service_criticality=Level.CRITICAL,
                operational_dependency=Level.HIGH,
                access_level=AccessLevel.PRIVILEGED,
                data_sensitivity=DataSensitivity.RESTRICTED,
                single_source=True,
                subcontractors_used=True,
            ),
            controls=ControlProfile(
                mfa=ControlState.YES,
                privileged_access_management=ControlState.PARTIAL,
                incident_notification_commitment=ControlState.YES,
                vulnerability_management=ControlState.YES,
                security_testing=ControlState.PARTIAL,
                encryption=ControlState.YES,
                backup_recovery=ControlState.YES,
                business_continuity=ControlState.PARTIAL,
                supplier_monitoring=ControlState.YES,
                assurance_evidence=ControlState.PARTIAL,
                exit_portability=ControlState.NO,
                subcontractor_governance=ControlState.PARTIAL,
            ),
        ),
        contract_clauses=(
            ContractClause("CTR-001", "Security", ClauseState.PRESENT, "ref", "fix"),
            ContractClause("CTR-002", "Incident", ClauseState.PARTIAL, "ref", "fix"),
        ),
    )

    assert result.tiering.tier == SupplierTier.TIER_1_CRITICAL
    assert result.inherent_risk.score >= result.residual_risk.score
    assert len(result.questionnaire) > 6
    assert result.contract is not None
    assert result.contract.total_applicable == 2
