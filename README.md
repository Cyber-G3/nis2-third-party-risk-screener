# NIS2 Third-Party Risk Screener

Open-source, deterministic third-party cyber risk screening and assurance toolkit for supplier intake, inherent/residual risk, decision support, evidence expectations and NIS2-oriented supply-chain traceability.

> Status: **Alpha / v0.1-dev**

## Product goal

Help security, GRC and procurement teams answer:

- Which suppliers are critical?
- What is the supplier's inherent cyber risk?
- Which controls and evidence reduce that risk?
- What residual risk remains?
- Should the supplier be approved, approved with conditions, escalated or reassessed?
- Which NIS2 / EU 2024/2690 supporting references are relevant to the assessment?

The tool supports decision-making. It does **not** determine legal applicability, regulatory compliance, certification status or contractual sufficiency.

## Initial architecture

```text
Supplier Intake
      ↓
Inherent Risk Engine
      ↓
Control / Evidence Inputs
      ↓
Residual Risk Engine
      ↓
Decision Engine
      ↓
NIS2 / 2024/2690 Supporting References
      ↓
Remediation + Supplier Tier
```

## Initial supplier risk dimensions

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

## Planned phases

### v0.1
- versioned supplier schema
- deterministic inherent risk engine
- residual risk engine
- decision engine
- NIS2 / 2024/2690 supporting mapping dataset
- tests
- CLI for one supplier

### v0.2
- adaptive questionnaire
- evidence quality
- contract security checker
- remediation planner
- supplier tiering

### v0.3
- supplier register
- portfolio dashboard
- concentration risk
- fourth-party map
- reassessment / continuous monitoring

### v0.4
- incident-impact mode
- keep / mitigate / replace simulator
- import/export integrations

## Principles

- deterministic and explainable scoring
- explicit reason codes
- versioned schemas and mappings
- risk separated from compliance conclusions
- local-first processing
- no telemetry
- no LLM dependency required at runtime

## License

Apache-2.0 planned for the first release.
