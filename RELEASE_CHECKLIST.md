# v0.1.0 Release Checklist

Scope is frozen for the first stable Supplier Assurance Engine release. Do not add new product features until these gates are closed.

## Functional gates

- [x] Deterministic supplier risk screening
- [x] Supplier evidence inventory
- [x] Evidence freshness states
- [x] Reassessment triggers
- [x] Critical-service and single-source reason codes
- [x] Supplier incident and material-change triggers
- [x] Stable Supplier Assurance output contract (`schema_version=1.0`)
- [x] Published JSON Schema
- [x] Explicit remediation and closure-evidence outputs

## Quality gates

- [x] Ruff configured
- [x] Strict Mypy configured
- [x] pytest configured
- [x] Python 3.12 / 3.13 CI matrix configured
- [x] Minimum 80% coverage gate configured
- [x] Bandit configured
- [x] pip-audit configured
- [ ] Final CI green on release commit

## Security / governance

- [x] `SECURITY.md` present
- [x] No runtime LLM dependency for core scoring
- [x] Deterministic reason codes documented
- [x] Public repository data-handling warning documented
- [ ] Confirm no credentials, secrets or customer evidence in repository history/assets

## Documentation / packaging

- [x] README present
- [x] Supplier Assurance documentation present
- [x] JSON Schema published
- [x] `CHANGELOG.md` present
- [x] Package version set to `0.1.0`
- [ ] LICENSE file present
- [ ] Build wheel and sdist successfully from release commit

## Release

- [ ] Merge release-readiness PR
- [ ] Tag `v0.1.0`
- [ ] Publish GitHub Release `v0.1.0`

## Out of scope for v0.1.0

Do not block this release on multi-tenant portfolio management, dashboards, white-label functionality, fourth-party graphing, concentration dashboards, automated supplier chasing or SaaS persistence.
