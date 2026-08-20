from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field

from tpr_screener.models import Level, SupplierProfile

SUPPLIER_ASSURANCE_SCHEMA_VERSION = "1.0"


class EvidenceState(StrEnum):
    CURRENT = "CURRENT"
    EXPIRING = "EXPIRING"
    EXPIRED = "EXPIRED"
    MISSING = "MISSING"
    UNKNOWN = "UNKNOWN"


class ReassessmentTrigger(StrEnum):
    SCHEDULED = "SCHEDULED"
    EVIDENCE_EXPIRED = "EVIDENCE_EXPIRED"
    CRITICAL_SERVICE = "CRITICAL_SERVICE"
    SUPPLIER_INCIDENT = "SUPPLIER_INCIDENT"
    MATERIAL_CHANGE = "MATERIAL_CHANGE"
    SINGLE_SOURCE = "SINGLE_SOURCE"


class SupplierEvidenceRecord(BaseModel):
    evidence_id: str
    evidence_type: str
    title: str
    valid_until: date | None = None
    required: bool = True


class SupplierAssuranceInput(BaseModel):
    supplier: SupplierProfile
    evidence: list[SupplierEvidenceRecord] = Field(default_factory=list)
    next_reassessment: date | None = None
    supplier_incident_open: bool = False
    material_change: bool = False
    as_of: date


class SupplierEvidenceStatus(BaseModel):
    evidence_id: str
    title: str
    state: EvidenceState
    days_until_expiry: int | None = None


class SupplierAssuranceResult(BaseModel):
    schema_version: str = SUPPLIER_ASSURANCE_SCHEMA_VERSION
    supplier_id: str
    assurance_level: Level
    evidence_status: list[SupplierEvidenceStatus] = Field(default_factory=list)
    triggers: list[ReassessmentTrigger] = Field(default_factory=list)
    reason_codes: list[str] = Field(default_factory=list)
    reassessment_required: bool
    remediation_required: bool
    closure_evidence_required: bool


def _evidence_state(record: SupplierEvidenceRecord, as_of: date) -> SupplierEvidenceStatus:
    if record.valid_until is None:
        return SupplierEvidenceStatus(
            evidence_id=record.evidence_id,
            title=record.title,
            state=EvidenceState.UNKNOWN,
            days_until_expiry=None,
        )

    days = (record.valid_until - as_of).days
    if days < 0:
        state = EvidenceState.EXPIRED
    elif days <= 30:
        state = EvidenceState.EXPIRING
    else:
        state = EvidenceState.CURRENT
    return SupplierEvidenceStatus(
        evidence_id=record.evidence_id,
        title=record.title,
        state=state,
        days_until_expiry=days,
    )


def assess_supplier_assurance(data: SupplierAssuranceInput) -> SupplierAssuranceResult:
    """Evaluate deterministic evidence freshness and supplier reassessment triggers."""
    statuses = [_evidence_state(record, data.as_of) for record in data.evidence]
    triggers: list[ReassessmentTrigger] = []
    reason_codes: list[str] = []

    if any(status.state is EvidenceState.EXPIRED for status in statuses):
        triggers.append(ReassessmentTrigger.EVIDENCE_EXPIRED)
        reason_codes.append("SUPPLIER_EVIDENCE_EXPIRED")

    if data.next_reassessment is not None and data.next_reassessment <= data.as_of:
        triggers.append(ReassessmentTrigger.SCHEDULED)
        reason_codes.append("SUPPLIER_REASSESSMENT_DUE")

    if data.supplier.service_criticality in {Level.HIGH, Level.CRITICAL}:
        triggers.append(ReassessmentTrigger.CRITICAL_SERVICE)
        reason_codes.append("CRITICAL_SUPPLIER_SERVICE")

    if data.supplier.single_source:
        triggers.append(ReassessmentTrigger.SINGLE_SOURCE)
        reason_codes.append("SINGLE_SOURCE_DEPENDENCY")

    if data.supplier_incident_open:
        triggers.append(ReassessmentTrigger.SUPPLIER_INCIDENT)
        reason_codes.append("SUPPLIER_INCIDENT_OPEN")

    if data.material_change:
        triggers.append(ReassessmentTrigger.MATERIAL_CHANGE)
        reason_codes.append("SUPPLIER_MATERIAL_CHANGE")

    expired = sum(status.state is EvidenceState.EXPIRED for status in statuses)
    expiring = sum(status.state is EvidenceState.EXPIRING for status in statuses)
    if data.supplier.service_criticality is Level.CRITICAL or expired >= 2:
        assurance_level = Level.CRITICAL
    elif data.supplier.service_criticality is Level.HIGH or expired == 1:
        assurance_level = Level.HIGH
    elif expiring:
        assurance_level = Level.MEDIUM
    else:
        assurance_level = Level.LOW

    remediation_triggers = {
        ReassessmentTrigger.EVIDENCE_EXPIRED,
        ReassessmentTrigger.SUPPLIER_INCIDENT,
        ReassessmentTrigger.MATERIAL_CHANGE,
        ReassessmentTrigger.SINGLE_SOURCE,
    }
    remediation_required = any(trigger in remediation_triggers for trigger in triggers)

    return SupplierAssuranceResult(
        supplier_id=data.supplier.supplier_id,
        assurance_level=assurance_level,
        evidence_status=statuses,
        triggers=triggers,
        reason_codes=reason_codes,
        reassessment_required=bool(triggers),
        remediation_required=remediation_required,
        closure_evidence_required=remediation_required,
    )
