# Supplier Assurance Lifecycle

This module extends the one-time supplier screening model into a deterministic assurance lifecycle suitable for downstream NIS2 operations.

```text
Supplier profile
      ↓
Evidence inventory
      ↓
Freshness / expiry
      ↓
Reassessment triggers
      ↓
Assurance level
      ↓
Remediation / monitoring in downstream platform
```

## Initial capabilities

- evidence freshness: `CURRENT`, `EXPIRING`, `EXPIRED`, `UNKNOWN`
- scheduled reassessment trigger
- critical-service trigger
- supplier incident trigger
- material-change trigger
- single-source dependency trigger
- stable reason codes for platform automation

## Public API

```python
from tpr_screener.assurance import SupplierAssuranceInput, assess_supplier_assurance

result = assess_supplier_assurance(data)
```

## Boundary

The module does not provide portfolio multi-tenancy, fourth-party graphing, partner dashboards or automated supplier chasing. Those belong to the future NIS2 Operations Platform.

The engine's responsibility is to produce a reusable supplier-assurance result that downstream systems can consume.
