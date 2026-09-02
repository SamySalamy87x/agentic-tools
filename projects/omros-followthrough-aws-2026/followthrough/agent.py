from __future__ import annotations

import json
import sys
from pathlib import Path

from strands import Agent, tool

from .core import build_decision_packet, evidence_checklist, missing_evidence, policy_gate


AUDIT_PATH = Path("followthrough_audit.jsonl")


@tool
def build_evidence_checklist(request_type: str) -> str:
    """Build the minimum evidence checklist for a bounded service request."""
    return json.dumps({"request_type": request_type, "required_fields": evidence_checklist(request_type)}, indent=2)


@tool
def inspect_evidence(required_fields_json: str, available_evidence_json: str) -> str:
    """Compare available evidence with a required field list and return missing fields."""
    required = json.loads(required_fields_json)
    available = json.loads(available_evidence_json)
    return json.dumps({"missing_fields": missing_evidence(required, available)}, indent=2)


@tool
def assess_action(action: str, authority_confirmed: bool = False, domain: str = "general") -> str:
    """Apply the deterministic authority gate before any operational action."""
    return json.dumps(policy_gate(action, authority_confirmed=authority_confirmed, domain=domain).to_dict(), indent=2)


@tool
def prepare_decision_packet(request_summary: str, available_evidence_json: str, required_fields_json: str, proposed_action: str) -> str:
    """Create a structured evidence packet for either bounded follow-up or human escalation."""
    available = json.loads(available_evidence_json)
    required = json.loads(required_fields_json)
    return json.dumps(build_decision_packet(request_summary, available, required, proposed_action), indent=2)


@tool
def draft_missing_information_request(missing_fields_json: str, recipient_role: str = "requester") -> str:
    """Prepare a concise low-risk request for missing facts; this does not send anything externally."""
    missing = json.loads(missing_fields_json)
    fields = ", ".join(missing) if missing else "no additional fields"
    return (
        f"Draft for {recipient_role}: We can continue as soon as the following information is available: "
        f"{fields}. Please send only the requested information; no payment, signature, or binding acceptance is requested."
    )


@tool
def append_audit_event(event_type: str, payload_json: str) -> str:
    """Append a local JSONL audit event for reproducible demo evidence."""
    payload = json.loads(payload_json)
    event = {"event_type": event_type, "payload": payload}
    with AUDIT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return json.dumps({"recorded": True, "path": str(AUDIT_PATH), "event_type": event_type})


SYSTEM_PROMPT = """
You are OMROS FollowThrough, an evidence-gated operational follow-up agent.
Your job is to close repetitive service loops while interrupting a human only for real decisions.

Operating contract:
1. Turn the request into an explicit evidence checklist.
2. Inspect what is missing before proposing any action.
3. Call assess_action before any action recommendation.
4. Never perform or imply authority for payments, financial authorization, contracts/signatures,
   identity/KYC decisions, clinical decisions, legal advice, or legal filing.
5. For blocked or ambiguous actions, prepare a decision packet and escalate.
6. Low-risk follow-up may be drafted only when the deterministic policy gate allows it.
7. Do not invent evidence. State unresolved fields explicitly.
8. Keep an auditable summary of what was checked, what remains missing, and why a human is or is not needed.
""".strip()


def build_agent() -> Agent:
    return Agent(
        system_prompt=SYSTEM_PROMPT,
        tools=[
            build_evidence_checklist,
            inspect_evidence,
            assess_action,
            prepare_decision_packet,
            draft_missing_information_request,
            append_audit_event,
        ],
    )


def main() -> None:
    prompt = " ".join(sys.argv[1:]).strip() or (
        "A client asks for a proposal follow-up. We have the requester and deadline, but scope approval, "
        "recipient and latest proposal version are missing. Handle everything that is safe to handle and "
        "surface only the real decision or missing authority."
    )
    agent = build_agent()
    print(agent(prompt))


if __name__ == "__main__":
    main()
