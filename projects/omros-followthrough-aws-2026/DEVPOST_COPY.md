# OMROS FollowThrough — Devpost Copy

## Project title
OMROS FollowThrough

## Tagline
The agent that closes the repetitive loop and surfaces only real decisions.

## Short description
OMROS FollowThrough is an evidence-gated operational agent built with the Strands Agents SDK. It turns inbound service work into an explicit evidence checklist, detects missing facts, prepares low-risk follow-up, builds a decision packet, and escalates only when a real human decision or authority boundary is reached.

## Inspiration
People lose time not only on difficult decisions, but on everything around them: checking what is missing, requesting it, following up, retrying failed steps, summarizing context and handing the case to the right person. Those loops are ideal agent work—if authority is bounded explicitly.

## What it does
FollowThrough receives a routine service request and creates a structured operational workflow. The Strands agent uses deterministic tools to build the evidence checklist, inspect missing facts, apply an authority policy gate, prepare safe follow-up, produce an evidence packet, and maintain an audit trail. Payments, contracts/signatures, identity/KYC decisions, clinical decisions and legal actions are never delegated.

## How we built it
- Strands Agents SDK for the agent runtime and tool orchestration
- deterministic Python evidence/policy core
- explicit non-delegable action boundary
- structured decision packets
- JSONL audit events for reproducible evidence
- deterministic unit tests independent of the model

The model proposes and orchestrates; deterministic code defines authority.

## Why an agent instead of another app
FollowThrough is designed to run the repetitive state machine in the background. The user should not need to manage a chat session for every step. The agent performs evidence checks and low-risk follow-up, then surfaces only when something is missing or human authority is actually required.

## Safety and authority
FollowThrough hard-blocks:
- binding contract acceptance/signature
- payments and financial authorization
- identity/KYC decisions
- clinical diagnosis/treatment decisions
- legal advice/filing

Unknown actions without explicit authority escalate by default.

## Validation
The deterministic core is tested independently from the model for evidence completeness, missing-field detection, low-risk follow-up, payment blocking, unknown-action escalation and decision-packet generation.

## What is next
Complete a live Bedrock/Strands run, host the demo, record the final video, and measure manual-intervention count across a fixed 20-case benchmark.

## Repository path
https://github.com/SamySalamy87x/agentic-tools/tree/main/projects/omros-followthrough-aws-2026

## License
Repository root license applies.
