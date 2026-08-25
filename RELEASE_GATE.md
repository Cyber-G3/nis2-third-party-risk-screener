# v0.1.0 Release Gate

The functional scope is frozen. Do not add new product features before v0.1.0 is published.

## Verified on main

- Supplier Assurance output contract is versioned as schema_version 1.0.
- JSON Schema, remediation outputs and closure-evidence requirements are present.
- Python 3.12/3.13 CI matrix, Ruff, strict Mypy, pytest coverage >=80%, Bandit, pip-audit and package build checks are configured.
- CHANGELOG, SECURITY.md and Apache-2.0 LICENSE are present.
- Package version is 0.1.0.

## Final gates

- [ ] Fresh CI succeeds on current main.
- [ ] Confirm repository contains no credentials, secrets or customer evidence in tracked release assets.
- [ ] Create tag v0.1.0 from validated main.
- [ ] Publish GitHub Release v0.1.0.
- [ ] Update README from Release Candidate to released status.

## Deferred to post-v0.1

Multi-tenant portfolio management, dashboards, white-label functionality, fourth-party graphing, concentration dashboards, automated supplier chasing and SaaS persistence.
