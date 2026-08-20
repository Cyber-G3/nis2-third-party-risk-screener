# Security Policy

## Supported version

The current supported release line is `0.1.x`.

## Reporting a vulnerability

Please do not disclose suspected vulnerabilities in a public issue. Report them privately to the repository owner through GitHub's private vulnerability reporting or another private contact channel published by the project owner.

Include, when possible:

- affected version or commit;
- reproduction steps;
- expected and observed behaviour;
- security impact;
- any suggested mitigation.

## Security model

This project is a deterministic third-party risk and assurance engine. It does not require an LLM for its core workflow and does not make legal or certification determinations.

Do not commit supplier-confidential evidence, credentials, secrets, production contracts, personal data, or customer-specific assurance records to this public repository.

## Dependency and code checks

The CI pipeline runs static analysis, typed checks, tests with a coverage gate, Bandit and dependency auditing. These controls reduce risk but do not constitute a security certification.
