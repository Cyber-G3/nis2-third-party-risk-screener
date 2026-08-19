from tpr_screener.models import AccessLevel, DataSensitivity, Level, SupplierProfile, SupplierType
from tpr_screener.questionnaire import build_questionnaire


def ids(profile: SupplierProfile) -> set[str]:
    return {q.question_id for q in build_questionnaire(profile)}


def test_privileged_saas_gets_adaptive_questions() -> None:
    profile = SupplierProfile(
        supplier_id="sup-1",
        supplier_name="Admin SaaS",
        supplier_type=SupplierType.SAAS,
        service_description="Production SaaS",
        service_criticality=Level.HIGH,
        access_level=AccessLevel.PRIVILEGED,
        data_sensitivity=DataSensitivity.RESTRICTED,
        subcontractors_used=True,
    )
    question_ids = ids(profile)
    assert {"IAM-001", "PAM-001", "LOG-001", "ENC-001", "CLD-001", "SUB-001", "SDLC-001", "4P-001"} <= question_ids


def test_low_risk_professional_service_keeps_base_questionnaire() -> None:
    profile = SupplierProfile(
        supplier_id="sup-2",
        supplier_name="Advisor",
        supplier_type=SupplierType.PROFESSIONAL_SERVICE,
        service_description="Advisory",
        service_criticality=Level.LOW,
        subcontractors_used=False,
    )
    question_ids = ids(profile)
    assert "GOV-001" in question_ids
    assert "PAM-001" not in question_ids
    assert "CLD-001" not in question_ids
