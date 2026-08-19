from __future__ import annotations

from dataclasses import dataclass

from .models import AccessLevel, DataSensitivity, SupplierProfile, SupplierType


@dataclass(frozen=True)
class Question:
    question_id: str
    prompt: str
    domain: str
    required: bool = True
    evidence_hint: str | None = None


BASE_QUESTIONS = (
    Question("GOV-001", "Is there an assigned security owner for the service?", "governance"),
    Question("IR-001", "Is there a contractual incident notification commitment?", "incident-response", evidence_hint="Contract/SLA clause"),
    Question("VM-001", "Is vulnerability management formally implemented?", "vulnerability-management", evidence_hint="Policy and remediation records"),
    Question("BC-001", "Is business continuity and recovery tested?", "resilience", evidence_hint="BCP/DR test record"),
    Question("MON-001", "Is the supplier security posture periodically reviewed?", "supplier-monitoring", evidence_hint="Review record"),
    Question("EXIT-001", "Is there a documented exit, portability or transition approach?", "exit-portability", evidence_hint="Exit/transition plan"),
)


def build_questionnaire(profile: SupplierProfile) -> tuple[Question, ...]:
    questions = list(BASE_QUESTIONS)

    if profile.access_level in {AccessLevel.PRIVILEGED, AccessLevel.ADMINISTRATIVE}:
        questions.extend(
            [
                Question("IAM-001", "Is MFA enforced for privileged access?", "identity-access", evidence_hint="MFA configuration"),
                Question("PAM-001", "Are privileged accounts controlled and periodically reviewed?", "privileged-access", evidence_hint="PAM/access review evidence"),
                Question("LOG-001", "Are privileged activities logged and monitored?", "logging-monitoring", evidence_hint="Audit logs/SIEM evidence"),
            ]
        )

    if profile.data_sensitivity in {DataSensitivity.CONFIDENTIAL, DataSensitivity.RESTRICTED}:
        questions.extend(
            [
                Question("ENC-001", "Is sensitive data encrypted in transit and at rest where applicable?", "data-protection", evidence_hint="Encryption configuration"),
                Question("RET-001", "Are retention and secure deletion requirements defined?", "data-protection", evidence_hint="Retention/deletion policy"),
            ]
        )

    if profile.supplier_type in {SupplierType.CLOUD, SupplierType.SAAS}:
        questions.extend(
            [
                Question("CLD-001", "Are tenant isolation and cloud security responsibilities documented?", "cloud-security", evidence_hint="Architecture/shared responsibility documentation"),
                Question("SUB-001", "Is a current list of subprocessors available?", "fourth-party-risk", evidence_hint="Subprocessor register"),
            ]
        )

    if profile.supplier_type in {SupplierType.SOFTWARE, SupplierType.SAAS, SupplierType.CLOUD}:
        questions.extend(
            [
                Question("SDLC-001", "Is a secure development lifecycle implemented?", "software-supply-chain", evidence_hint="Secure SDLC standard"),
                Question("TEST-001", "Is security testing performed before material releases?", "security-testing", evidence_hint="Test/pentest evidence"),
            ]
        )

    if profile.supplier_type in {SupplierType.MSP, SupplierType.MSSP}:
        questions.extend(
            [
                Question("SEG-001", "Are management-plane and customer environments appropriately segregated?", "network-security", evidence_hint="Architecture/network controls"),
                Question("STAFF-001", "Are personnel security requirements defined for privileged operators?", "personnel-security", evidence_hint="Personnel security procedure"),
            ]
        )

    if profile.subcontractors_used is True or profile.subcontractors_used is None:
        questions.append(Question("4P-001", "Are material subcontractors governed and monitored?", "fourth-party-risk", evidence_hint="Subcontractor governance evidence"))

    seen: set[str] = set()
    unique: list[Question] = []
    for question in questions:
        if question.question_id not in seen:
            unique.append(question)
            seen.add(question.question_id)
    return tuple(unique)
