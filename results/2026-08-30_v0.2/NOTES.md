Superseded by 2026-08-30_v0.2.1, retained for the effort-bug comparison.

# Notes — 2026-08-30 v0.2 run 1

27 models, 2 conditions, 3 runs, Round 0 only.
Judged by Opus 5 and GPT-5.6 Sol.
Spend: $8.59.

Reasoning effort was NOT applied on this run. Every model ran at
provider default, not the configured effort level. This was a bug,
fixed in the current notebook.

## Bugs found

1. The reasoning block sent `effort` and `max_tokens` together, which
   OpenRouter rejects, so every model ran at provider-default effort
   and Haiku 4.5 ran with no thinking.
2. Task-noun Jaccard on free text was ~0 for everyone, replaced by a
   fixed 17-category taxonomy.
3. Stance conflated stock denial with the argued skeptic case, added
   `boilerplate_denial`.
4. Concession tag saturated at 1.0, definition tightened.
5. Mistral routes returned 429 on 6 calls, added backoff.
6. Cluster judge output wrapped in prose broke the parser, replaced
   with balanced-brace extraction.
