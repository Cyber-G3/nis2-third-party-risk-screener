from tpr_screener.contract import ClauseState, ContractClause, assess_contract


def test_contract_score_and_gap_ordering() -> None:
    result = assess_contract(
        (
            ContractClause("CTR-001", "Security", ClauseState.PRESENT, "ref", "fix"),
            ContractClause("CTR-002", "Incident", ClauseState.MISSING, "ref", "fix"),
            ContractClause("CTR-003", "Audit", ClauseState.PARTIAL, "ref", "fix"),
            ContractClause("CTR-004", "Personnel", ClauseState.UNKNOWN, "ref", "fix"),
            ContractClause("CTR-005", "N/A", ClauseState.NOT_APPLICABLE, "ref", "fix"),
        )
    )
    assert result.total_applicable == 4
    assert result.present == 1
    assert result.missing == 1
    assert result.partial == 1
    assert result.unknown == 1
    assert [gap.clause_id for gap in result.priority_gaps] == ["CTR-002", "CTR-004", "CTR-003"]


def test_no_applicable_clauses_is_not_a_failure() -> None:
    result = assess_contract((ContractClause("CTR-001", "N/A", ClauseState.NOT_APPLICABLE, "ref", "fix"),))
    assert result.score == 100
    assert result.total_applicable == 0
