#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD="$ROOT/.build"
rm -rf "$BUILD"
mkdir -p "$BUILD/classes" "$ROOT/evidence"

START_NS=$(date +%s%N)
javac -d "$BUILD/classes" \
  $(find "$ROOT/legacy/src" "$ROOT/modern/src" "$ROOT/tests/src" -name '*.java' | sort)

set +e
OUTPUT=$(java -cp "$BUILD/classes" bobguard.tests.ParityHarness 2>&1)
STATUS=$?
set -e
END_NS=$(date +%s%N)
ELAPSED_MS=$(( (END_NS - START_NS) / 1000000 ))

printf '%s\n' "$OUTPUT"
PASS_LINE=$(printf '%s\n' "$OUTPUT" | head -n 1)
PARITY_LINE=$(printf '%s\n' "$OUTPUT" | sed -n '2p')
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

cat > "$ROOT/evidence/report.json" <<JSON
{
  "project": "BobGuard — Evidence-Gated Modernization with IBM Bob 2.0",
  "generated_at_utc": "$NOW",
  "status": $STATUS,
  "summary": "$PASS_LINE",
  "behavioral_parity": "$PARITY_LINE",
  "runtime_ms": $ELAPSED_MS,
  "method": "Compile legacy and modular implementations, execute deterministic parity cases, and verify matched failure behavior."
}
JSON

cat > "$ROOT/evidence/report.md" <<MD
# BobGuard Validation Evidence

- Generated: $NOW
- Result: **$PASS_LINE**
- $PARITY_LINE
- End-to-end compile + validation runtime: **${ELAPSED_MS} ms**

## Deterministic output

\`\`\`text
$OUTPUT
\`\`\`

## Evidence gate

BobGuard treats modernization as acceptable only when the modularized implementation preserves the legacy service's externally observable behavior across the declared invariants and validation cases.
MD

cat > "$ROOT/evidence/report.html" <<HTML
<!doctype html><html><head><meta charset="utf-8"><title>BobGuard Evidence</title>
<style>body{font-family:system-ui;margin:40px;max-width:980px;background:#0b0f14;color:#e8eef7}code,pre{background:#141b24;padding:14px;border-radius:8px;display:block;white-space:pre-wrap}.pass{font-size:28px;font-weight:700}</style></head>
<body><h1>BobGuard Validation Evidence</h1><div class="pass">$PASS_LINE</div><p>$PARITY_LINE</p><p>Runtime: ${ELAPSED_MS} ms</p><h2>Deterministic output</h2><pre>$OUTPUT</pre><h2>Evidence gate</h2><p>Modernization is accepted only when declared behavioral invariants remain machine-checkably preserved.</p></body></html>
HTML

exit "$STATUS"
