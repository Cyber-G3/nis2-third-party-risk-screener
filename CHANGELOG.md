# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-08-20

### Added

- deterministic supplier risk screening;
- supplier evidence inventory and freshness states;
- assurance-level output;
- reassessment triggers for evidence expiry, supplier incidents and material changes;
- critical-service and single-source reason codes;
- explicit remediation and closure-evidence requirements;
- stable output contract with `schema_version=1.0`;
- published JSON Schema for Supplier Assurance v1;
- documentation for the supplier-assurance lifecycle;
- Python 3.12 and 3.13 CI matrix;
- Ruff, strict Mypy, test coverage gate, Bandit and dependency audit.

### Changed

- project packaging is explicitly configured for the `src/tpr_screener` package;
- package version promoted from `0.1.0.dev0` to `0.1.0` release candidate scope.

### Security

- added public security policy and release security gates.

### Scope boundary

This release does not include multi-tenant portfolio management, dashboards, white-label functionality, automated supplier chasing or fourth-party graphing. Those belong to later platform or engine versions.
