from __future__ import annotations

from dataclasses import dataclass

from .contract import ContractAssessment, ContractClause, assess_contract
from .decision import DecisionResult, decide_supplier
from .models import SupplierAssessmentInput
from .questionnaire import Question, build_questionnaire
from .risk import RiskAssessment, assess_inherent_risk, assess_residual_risk
from .tiering import TieringResult, classify_supplier


@dataclass(frozen=True)
class SupplierAssessment:
    tiering: TieringResult
    inherent_risk: RiskAssessment
    residual_risk: RiskAssessment
    decision: DecisionResult
    questionnaire: tuple[Question, ...]
    contract: ContractAssessment | None


def assess_supplier(
    assessment_input: SupplierAssessmentInput,
    *,
    contract_clauses: tuple[ContractClause, ...] | None = None,
) -> SupplierAssessment:
    """Run the deterministic supplier assessment pipeline."""
    tiering = classify_supplier(assessment_input.profile)
    inherent = assess_inherent_risk(assessment_input.profile)
    residual = assess_residual_risk(inherent, assessment_input.controls)
    decision = decide_supplier(assessment_input.profile, assessment_input.controls, residual)
    questionnaire = build_questionnaire(assessment_input.profile)
    contract = assess_contract(contract_clauses) if contract_clauses is not None else None

    return SupplierAssessment(
        tiering=tiering,
        inherent_risk=inherent,
        residual_risk=residual,
        decision=decision,
        questionnaire=questionnaire,
        contract=contract,
    )
