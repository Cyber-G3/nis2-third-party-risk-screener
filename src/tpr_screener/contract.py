from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ClauseState(StrEnum):
    PRESENT = "PRESENT"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ContractClause:
    clause_id: str
    title: str
    state: ClauseState
    reference: str
    remediation: str


@dataclass(frozen=True)
class ContractAssessment:
    total_applicable: int
    present: int
    partial: int
    missing: int
    unknown: int
    score: int
    priority_gaps: tuple[ContractClause, ...]


def assess_contract(clauses: tuple[ContractClause, ...]) -> ContractAssessment:
    applicable = [c for c in clauses if c.state != ClauseState.NOT_APPLICABLE]
    if not applicable:
        return ContractAssessment(0, 0, 0, 0, 0, 100, ())

    counts = {state: 0 for state in ClauseState}
    for clause in applicable:
        counts[clause.state] += 1

    weighted = (
        counts[ClauseState.PRESENT] * 1.0
        + counts[ClauseState.PARTIAL] * 0.5
        + counts[ClauseState.UNKNOWN] * 0.25
    )
    score = round(weighted / len(applicable) * 100)

    rank = {
        ClauseState.MISSING: 0,
        ClauseState.UNKNOWN: 1,
        ClauseState.PARTIAL: 2,
        ClauseState.PRESENT: 3,
        ClauseState.NOT_APPLICABLE: 4,
    }
    gaps = tuple(sorted((c for c in applicable if c.state != ClauseState.PRESENT), key=lambda c: (rank[c.state], c.clause_id)))

    return ContractAssessment(
        total_applicable=len(applicable),
        present=counts[ClauseState.PRESENT],
        partial=counts[ClauseState.PARTIAL],
        missing=counts[ClauseState.MISSING],
        unknown=counts[ClauseState.UNKNOWN],
        score=score,
        priority_gaps=gaps,
    )


def default_security_clauses() -> tuple[ContractClause, ...]:
    """Return the baseline contract-check domains with no inferred status."""
    return (
        ContractClause("CTR-001", "Security requirements and responsibilities", ClauseState.UNKNOWN, "NIS2 supply-chain security supporting reference", "Define explicit cybersecurity responsibilities and required controls."),
        ContractClause("CTR-002", "Incident notification and cooperation", ClauseState.UNKNOWN, "2024/2690 supply-chain supporting reference", "Define incident notification timing, escalation contacts and cooperation duties."),
        ContractClause("CTR-003", "Vulnerability handling and remediation", ClauseState.UNKNOWN, "2024/2690 supply-chain supporting reference", "Define vulnerability disclosure, remediation and material-risk communication expectations."),
        ContractClause("CTR-004", "Audit or assurance rights", ClauseState.UNKNOWN, "2024/2690 supply-chain supporting reference", "Define proportionate audit, assessment or assurance-report rights."),
        ContractClause("CTR-005", "Subcontractor / subprocessor governance", ClauseState.UNKNOWN, "2024/2690 supply-chain supporting reference", "Define approval, notification and flow-down expectations for material subcontractors."),
        ContractClause("CTR-006", "Personnel security requirements", ClauseState.UNKNOWN, "2024/2690 supply-chain supporting reference", "Define relevant personnel-security obligations for supplier staff with sensitive access."),
        ContractClause("CTR-007", "Business continuity and recovery", ClauseState.UNKNOWN, "NIS2 supply-chain/resilience supporting reference", "Define continuity, recovery and testing obligations proportionate to service criticality."),
        ContractClause("CTR-008", "Termination, data return and secure deletion", ClauseState.UNKNOWN, "2024/2690 supply-chain supporting reference", "Define exit support, data return, deletion and transition requirements."),
    )
