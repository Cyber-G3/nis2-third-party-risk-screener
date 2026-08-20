# NIS2 Third-Party Risk Screener

Open-source, deterministic third-party cyber risk screening and assurance toolkit for supplier intake, inherent/residual risk, decision support, evidence expectations and NIS2-oriented supply-chain traceability.

> Status: **v0.1.0 Release Candidate**

## Product goal

Help security, GRC and procurement teams answer:

- Which suppliers are critical?
- What is the supplier's inherent cyber risk?
- Which controls and evidence reduce that risk?
- What residual risk remains?
- Should the supplier be approved, approved with conditions, escalated or reassessed?
- Which NIS2 / EU 2024/2690 supporting references are relevant to the assessment?
- Which supplier evidence is missing, expiring or expired?
- What event should trigger reassessment?
- Is remediation or closure evidence required before assurance can be improved?

The tool supports decision-making. It does **not** determine legal applicability, regulatory compliance, certification status or contractual sufficiency.

## Architecture

```text
Supplier Intake
      ↓
Inherent Risk Engine
      ↓
Control / Evidence Inputs
      ↓
Residual Risk Engine
      ↓
Supplier Assurance Layer
      ↓
Evidence Freshness + Reassessment Triggers
      ↓
Decision Engine
      ↓
NIS2 / 2024/2690 Supporting References
      ↓
Remediation + Closure Evidence
```

## Supplier risk dimensions

- service criticality
- data sensitivity
- access level
- operational dependency
- Internet dependency
- single-source dependency
- subcontractor / fourth-party visibility
- geographic exposure
- incident-notification capability
- vulnerability management
- MFA / privileged access
- encryption
- backup / recovery
- business continuity
- security testing
- supplier monitoring
- certification / assurance evidence
- exit / portability readiness

## v0.1.0 release scope

- versioned supplier schema
- deterministic inherent and residual risk engines
- supplier decision engine
- supplier evidence inventory
- evidence freshness states
- reassessment triggers
- critical-service and single-source reason codes
- supplier incident and material-change triggers
- stable Supplier Assurance output contract (`schema_version=1.0`)
- published JSON Schema
- explicit remediation and closure-evidence outputs
- NIS2 / EU 2024/2690 supporting mapping dataset
- typed/tests/security quality gates

## Post-v0.1 roadmap

### v0.2
- adaptive questionnaire
- deeper evidence quality
- contract security checker
- remediation planner
- supplier tiering refinements

### v0.3
- concentration metrics
- fourth-party context
- continuous supplier reassessment signals

### Platform layer
- supplier register across multiple customers
- portfolio dashboard
- white-label workflows
- automated supplier chasing
- multi-tenant persistence

These platform capabilities are intentionally out of scope for the standalone engine.

## Principles

- deterministic and explainable scoring
- explicit reason codes
- versioned schemas and mappings
- risk separated from compliance conclusions
- local-first processing
- no telemetry
- no LLM dependency required at runtime

## Security

Do not commit real supplier-confidential evidence, credentials, personal data, contracts or customer-specific assurance records to this public repository. See `SECURITY.md`.

## License

Apache-2.0. See `LICENSE`.
