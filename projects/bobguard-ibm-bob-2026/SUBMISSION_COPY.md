# Hackathon Submission Copy

## Project name
BobGuard — Evidence-Gated Modernization with IBM Bob 2.0

## Elevator pitch
A Bob-orchestrated modernization workflow that turns risky legacy refactoring into bounded, regression-gated tasks with reproducible before/after evidence.

## Problem
Enterprise modernization is slowed by uncertainty, not syntax. Developers must discover hidden business invariants, decompose risky changes, preserve behavior, rerun tests, document evidence, and convince reviewers that the refactor is safe.

## Solution
BobGuard uses IBM Bob 2.0 as the orchestration layer for repository/document understanding, invariant discovery, bounded modernization planning, implementation review, and deterministic validation. Every bounded change is gated by machine-checkable behavioral evidence. The output is a modernization plan plus reviewer-facing JSON, Markdown, and HTML evidence rather than code suggestions alone.

## How IBM Bob 2.0 is used
1. Inspect the repository and document legacy behavior and constraints.
2. Identify externally observable invariants and modernization risk.
3. Decompose the work into bounded tasks with explicit acceptance criteria.
4. Review or execute narrowly scoped changes.
5. Run `./run_demo.sh` after the bounded change.
6. Treat any parity or validation failure as a release blocker.
7. Produce a final reviewer summary tied to the generated evidence artifacts.

## Prototype
The Java prototype contains a monolithic legacy pricing service and a modular target architecture using `DiscountPolicy`, `TaxPolicy`, and `ModernPricingService`. The deterministic harness compares the two implementations across eight parity cases and two validation/failure cases.

## Verified result
```text
PASS parity_cases=8 validation_cases=2
Behavioral parity: PASS
```

## Evidence generated
- `evidence/report.json`
- `evidence/report.md`
- `evidence/report.html`

## Technical differentiator
Governance by evidence. Bob is used to coordinate understanding, planning, bounded work, validation, and reviewer documentation rather than acting only as autocomplete.

## Repository
https://github.com/SamySalamy87x/agentic-tools/tree/main/projects/bobguard-ibm-bob-2026

## Demo
Talking-head hackathon explainer is being rendered. A stronger final demo should additionally include a real IBM Bob session export/screenshot and an actual screen recording of `./run_demo.sh`.

## Provenance note
Do not present generated or reconstructed UI as a real IBM Bob session. Real Bob-session exports/screenshots, when captured, should be stored unmodified under `evidence/bob-session/`.
