from tpr_screener.models import AccessLevel, DataSensitivity, Level, SupplierProfile, SupplierType
from tpr_screener.tiering import SupplierTier, classify_supplier


def test_critical_supplier_is_tier_one() -> None:
    result = classify_supplier(
        SupplierProfile(
            supplier_id="sup-1",
            supplier_name="Critical SaaS",
            supplier_type=SupplierType.SAAS,
            service_description="Critical production service",
            service_criticality=Level.CRITICAL,
            operational_dependency=Level.CRITICAL,
            access_level=AccessLevel.ADMINISTRATIVE,
            data_sensitivity=DataSensitivity.RESTRICTED,
            single_source=True,
            internet_dependency=True,
            subcontractors_used=True,
        )
    )
    assert result.tier == SupplierTier.TIER_1_CRITICAL
    assert result.score >= 70


def test_low_supplier_is_tier_four() -> None:
    result = classify_supplier(
        SupplierProfile(
            supplier_id="sup-2",
            supplier_name="Low Risk",
            supplier_type=SupplierType.PROFESSIONAL_SERVICE,
            service_description="Non-critical advisory service",
            service_criticality=Level.LOW,
            operational_dependency=Level.LOW,
        )
    )
    assert result.tier == SupplierTier.TIER_4_LOW
