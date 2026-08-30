# 75–90 Second Demo Script

Legacy modernization is not hard because developers cannot write code. It is hard because every refactor can break hidden business behavior.

BobGuard turns that uncertainty into a controlled workflow. IBM Bob 2.0 is used to understand the repository, identify behavioral invariants, decompose modernization into bounded tasks, and validate each change against machine-checkable acceptance criteria.

Our prototype starts with a monolithic Java pricing service and a modular target architecture built around DiscountPolicy, TaxPolicy, and ModernPricingService.

One command — `run_demo.sh` — compiles both versions, executes eight deterministic parity cases and two validation cases, and generates reviewer-facing JSON, Markdown, and HTML evidence.

The verified result is:

`PASS parity_cases=8 validation_cases=2`

`Behavioral parity: PASS`

The point is not autocomplete. The point is governance by evidence: understand, plan, change, validate, and prove that behavior was preserved.

That is BobGuard.
