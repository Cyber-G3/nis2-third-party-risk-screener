# Portfolio Case — NIS2 Third-Party Risk Screener

## Problem
Supplier onboarding often records questionnaire answers without connecting criticality, evidence, residual risk, remediation and an explicit business decision.

## Decision architecture
```text
Supplier intake
    ↓
Inherent risk
    ↓
Controls + evidence
    ↓
Residual risk
    ↓
Assurance state
    ↓
Decision / remediation
    ↓
Reassessment triggers
```

## What this demonstrates
- Deterministic and explainable supplier-risk scoring
- Evidence freshness and traceability
- Residual-risk decision support
- Remediation and closure evidence
- Versioned schemas and mappings
- NIS2-oriented supply-chain context without claiming compliance

## Commercial direction
The standalone engine can act as the diagnostic layer before a managed TPRM engagement or an appropriate continuous-monitoring technology. Vendor selection should remain needs-based and any commercial relationship should be disclosed.

## Next milestone
Adaptive questionnaires, deeper evidence quality, contract-security checks and portfolio-level concentration metrics.
