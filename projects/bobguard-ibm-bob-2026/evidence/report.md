# BobGuard Validation Evidence

- Generated: 2026-08-30T09:46:14Z
- Result: **PASS parity_cases=8 validation_cases=2**
- Behavioral parity: PASS
- End-to-end compile + validation runtime: **601 ms**

## Deterministic output

```text
PASS parity_cases=8 validation_cases=2
Behavioral parity: PASS
parity_1=PASS legacy=116.0 modern=116.0
parity_2=PASS legacy=110.2 modern=110.2
parity_3=PASS legacy=104.4 modern=104.4
parity_4=PASS legacy=525.01 modern=525.01
parity_5=PASS legacy=492.54 modern=492.54
parity_6=PASS legacy=528.0 modern=528.0
parity_7=PASS legacy=443.15 modern=443.15
parity_8=PASS legacy=36.26 modern=36.26
validation_quantity=PASS
validation_coupon=PASS
```

## Evidence gate

BobGuard treats modernization as acceptable only when the modularized implementation preserves the legacy service's externally observable behavior across the declared invariants and validation cases.
