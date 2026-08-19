from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class SupplierType(StrEnum):
    CLOUD = "CLOUD"
    SAAS = "SAAS"
    MSP = "MSP"
    MSSP = "MSSP"
    SOFTWARE = "SOFTWARE"
    DATA_PROCESSOR = "DATA_PROCESSOR"
    HARDWARE = "HARDWARE"
    PROFESSIONAL_SERVICE = "PROFESSIONAL_SERVICE"
    OTHER = "OTHER"


class Level(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DataSensitivity(StrEnum):
    NONE = "NONE"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class AccessLevel(StrEnum):
    NONE = "NONE"
    USER = "USER"
    PRIVILEGED = "PRIVILEGED"
    ADMINISTRATIVE = "ADMINISTRATIVE"


class Geography(StrEnum):
    EU_EEA = "EU_EEA"
    THIRD_COUNTRY = "THIRD_COUNTRY"
    UNKNOWN = "UNKNOWN"


class ControlState(StrEnum):
    YES = "YES"
    PARTIAL = "PARTIAL"
    NO = "NO"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SupplierProfile(BaseModel):
    schema_version: Literal["0.1"] = "0.1"
    supplier_id: str = Field(min_length=1, max_length=120)
    supplier_name: str = Field(min_length=1, max_length=200)
    supplier_type: SupplierType
    service_description: str = Field(min_length=1, max_length=1000)
    service_criticality: Level
    data_sensitivity: DataSensitivity = DataSensitivity.NONE
    access_level: AccessLevel = AccessLevel.NONE
    operational_dependency: Level = Level.MEDIUM
    internet_dependency: bool = False
    single_source: bool = False
    subcontractors_used: bool | None = None
    fourth_party_visibility: ControlState = ControlState.UNKNOWN
    geography: Geography = Geography.UNKNOWN


class ControlProfile(BaseModel):
    mfa: ControlState = ControlState.UNKNOWN
    privileged_access_management: ControlState = ControlState.UNKNOWN
    incident_notification_commitment: ControlState = ControlState.UNKNOWN
    vulnerability_management: ControlState = ControlState.UNKNOWN
    security_testing: ControlState = ControlState.UNKNOWN
    encryption: ControlState = ControlState.UNKNOWN
    backup_recovery: ControlState = ControlState.UNKNOWN
    business_continuity: ControlState = ControlState.UNKNOWN
    supplier_monitoring: ControlState = ControlState.UNKNOWN
    assurance_evidence: ControlState = ControlState.UNKNOWN
    exit_portability: ControlState = ControlState.UNKNOWN
    subcontractor_governance: ControlState = ControlState.UNKNOWN


class SupplierAssessmentInput(BaseModel):
    profile: SupplierProfile
    controls: ControlProfile = Field(default_factory=ControlProfile)
