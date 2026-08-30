# IBM Bob 2.0 Runbook

Use this repository as the bounded modernization target inside IBM Bob 2.0.

## Prompt 1 — Repository understanding
Inspect the repository. Explain the legacy pricing behavior, enumerate externally observable invariants, and identify modernization risks. Do not change code yet.

## Prompt 2 — Bounded plan
Create a modernization plan that decomposes the monolithic pricing service into bounded responsibilities while preserving every declared invariant. Define machine-checkable acceptance criteria for each step.

## Prompt 3 — Implementation review
Review `modern/src` against `legacy/src`. Identify any semantic drift. If a change is necessary, keep it minimal and explain the invariant it protects.

## Prompt 4 — Validation
Run `./run_demo.sh`. Treat any parity or validation failure as a release blocker. Summarize the evidence in `evidence/report.md` and `evidence/report.json`.

## Prompt 5 — Final reviewer summary
Produce a concise modernization review containing: original risk, bounded workstreams, invariants preserved, validation result, residual risk, and the exact evidence artifacts a reviewer should inspect.

## Evidence capture checklist
For hackathon provenance, export or screenshot the Bob session showing repository understanding, bounded planning, code review, and final validation. Store those artifacts under `evidence/bob-session/` without altering their timestamps.
