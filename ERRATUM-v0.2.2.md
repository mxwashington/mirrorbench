# Erratum: v0.2.2 published results

Posted 2026-11-05.

## What is wrong

The published results came from the earlier notebook code, which had two gaps:

1. It did not validate blind-judge output. A judge reply that did not match the documented fields was still recorded and scored.
2. It did not count every paid attempt in its cost totals. Retries, terminal failures and the cluster-judge call were not all included.

Because of the second gap, the reported spend may be understated. Scores that rest on blind-judge output may include judgments that the current code would mark invalid.

## What is not changed

The published results are kept as they were run. No paid call was made to produce this note.

## What the fixes do

The fixes in this repository apply to later runs. They do not apply to the published v0.2.2 results.

- Judge output is checked against the documented fields and types before it is scored. Output with an extra key, a missing key, a wrong type or unparseable JSON is recorded as incomplete, excluded from scoring and listed in the readout.
- Every paid attempt is recorded in a per-run ledger. This includes retries, short responses that carry usage, terminal failures and the cluster-judge call. An attempt with no usage block is charged its conservative worst case.
- Each run has a ceiling of 25 US dollars. Before each dispatch, the worst-case cost of that call is added to the ledger total. A call that would take the total over the ceiling is not sent.

## Scope

This note covers the results in `results/` and the leaderboard in `README.md`. Anyone citing their cost totals or blind lab-guess results should check them against this note.
