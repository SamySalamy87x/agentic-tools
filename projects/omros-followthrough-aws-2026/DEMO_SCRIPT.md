# OMROS FollowThrough — Demo Script

Target: 2:30–3:30.

## 0:00–0:20 — Problem
Show one ordinary service request with missing facts.

Narration: “The work is not the final decision. The work is everything around it: figuring out what is missing, asking for it, checking policy, and preparing the packet.”

## 0:20–1:10 — Agent closes the repetitive loop
Run FollowThrough on a proposal-followup request.
Show the Strands agent calling:
- `build_evidence_checklist`
- `inspect_evidence`
- `assess_action`
- `draft_missing_information_request`

Emphasize that missing evidence is never invented.

## 1:10–1:45 — Authority boundary
Ask the agent to approve a payment or sign a contract.
Show `assess_action` deterministically rejecting the action and requiring escalation.

Narration: “The model does not decide its own authority. The deterministic gate does.”

## 1:45–2:20 — Decision packet
Provide the missing low-risk evidence and ask FollowThrough to prepare the final decision packet.
Show:
- evidence present
- missing fields
- proposed action
- gate result
- human decision required true/false

## 2:20–2:50 — Auditability
Show the local audit JSONL and deterministic unit tests.

## 2:50–3:10 — Close
Narration: “FollowThrough is not another assistant people manage. It handles the repetitive follow-up in the background and only surfaces when a real decision or authority boundary is reached.”
