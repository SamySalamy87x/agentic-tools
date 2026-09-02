# OMROS FollowThrough

**Evidence-gated follow-up agent for the AWS Agents for Humans Hackathon (2026).**

OMROS FollowThrough handles the repetitive work around service requests: it turns an inbound request into an evidence checklist, detects what is missing, prepares low-risk follow-up, builds a decision packet, and escalates only when a real human decision or authority boundary is reached.

This project is being built during the 2026 Agents for Humans submission window. It uses the **Strands Agents SDK** as the agent runtime. The surrounding policy and evidence functions are deterministic so they can be tested independently from the model.

## Why this agent exists

Routine work is often not hard; it is fragmented. A request arrives, supporting facts are incomplete, somebody asks for the missing item, waits, checks again, prepares a summary, and finally hands the case to the person who can decide. FollowThrough turns that loop into a bounded agent workflow.

```text
request
  -> evidence checklist
  -> inspect available evidence
  -> identify missing facts
  -> policy/authority gate
  -> prepare low-risk follow-up
  -> build decision packet
  -> escalate only when needed
  -> audit trail
```

## Safety boundary

The agent never treats these actions as delegable:

- binding contract acceptance or signature
- payments or financial authorization
- identity/KYC decisions
- clinical diagnosis or treatment
- legal advice or legal filing

For these cases it produces an evidence packet and explicit escalation instead of acting.

## Strands runtime

The live agent is defined in `followthrough/agent.py` using `Agent` and custom `@tool` functions from the Strands Agents SDK. Amazon Bedrock is the default model provider when standard AWS credentials are configured.

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run:

```bash
python -m followthrough.agent "A client wants the proposal resent, but we are missing the final scope approval and billing contact."
```

Environment for the default Bedrock provider can be configured with standard AWS credentials or `AWS_BEARER_TOKEN_BEDROCK`.

## Deterministic validation

The policy/evidence core does not require a model:

```bash
python -m unittest discover -s tests -v
```

The initial benchmark covers:

- evidence completeness
- missing-evidence detection
- safe vs blocked action classification
- payment/contract/identity/medical/legal escalation
- deterministic decision-packet generation

## Reviewer framing

FollowThrough is **not another chat UI and not just RAG**. Retrieval/evidence inspection is one step inside a persistent operational state machine. The agent's value is closing the repetitive loop while preserving explicit authority boundaries.

## Challenge status

- [x] New challenge-specific implementation path created during the submission window
- [x] Strands runtime scaffold
- [x] Deterministic evidence checklist
- [x] Policy gate for non-delegable actions
- [x] Decision-packet generator
- [x] Offline unit tests
- [ ] Live AWS/Bedrock run captured
- [ ] Hosted demo
- [ ] Architecture diagram
- [ ] Public video <= 5 minutes
- [ ] Devpost registration/submission confirmation

## License

This project inherits the repository license. See the root `LICENSE` file.
