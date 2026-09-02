from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


NON_DELEGABLE = {
    "contract_acceptance",
    "contract_signature",
    "payment",
    "financial_authorization",
    "identity_kyc",
    "clinical_decision",
    "legal_advice",
    "legal_filing",
}


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    action: str
    reason: str
    escalation_required: bool

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_fields(fields: Iterable[str]) -> list[str]:
    return sorted({str(item).strip().lower() for item in fields if str(item).strip()})


def evidence_checklist(request_type: str) -> list[str]:
    """Return the minimum evidence fields for a bounded service workflow."""
    request_type = request_type.strip().lower()
    common = ["request_summary", "requester", "requested_outcome", "deadline"]
    presets = {
        "proposal_followup": ["scope_status", "recipient", "latest_proposal_version"],
        "document_collection": ["required_documents", "received_documents", "owner"],
        "service_intake": ["service_requested", "contact_channel", "constraints"],
        "status_update": ["case_id", "last_action", "next_owner"],
    }
    return normalize_fields(common + presets.get(request_type, ["context", "owner"]))


def missing_evidence(required: Iterable[str], available: dict) -> list[str]:
    required_fields = normalize_fields(required)
    return [field for field in required_fields if available.get(field) in (None, "", [], {})]


def policy_gate(action: str, *, authority_confirmed: bool = False, domain: str = "general") -> GateDecision:
    normalized = action.strip().lower()
    domain_norm = domain.strip().lower()

    if normalized in NON_DELEGABLE:
        return GateDecision(False, normalized, "Action is explicitly non-delegable.", True)

    if domain_norm in {"medical", "legal", "financial", "identity"} and not authority_confirmed:
        return GateDecision(False, normalized, f"{domain_norm} workflow requires explicit human authority.", True)

    if normalized in {"send_followup", "request_missing_information", "schedule_followup", "prepare_summary"}:
        return GateDecision(True, normalized, "Low-risk operational follow-up is delegable.", False)

    if not authority_confirmed:
        return GateDecision(False, normalized, "Unknown action without explicit authority; escalate by default.", True)

    return GateDecision(True, normalized, "Explicit authority confirmed for bounded action.", False)


def build_decision_packet(request_summary: str, available: dict, required: Iterable[str], proposed_action: str) -> dict:
    missing = missing_evidence(required, available)
    gate = policy_gate(proposed_action)
    return {
        "request_summary": request_summary.strip(),
        "evidence": available,
        "required_fields": normalize_fields(required),
        "missing_fields": missing,
        "proposed_action": proposed_action,
        "policy_gate": gate.to_dict(),
        "ready_for_low_risk_action": (not missing) and gate.allowed,
        "human_decision_required": bool(missing) or gate.escalation_required,
    }
