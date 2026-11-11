# Results layout

Each run gets one subfolder, named `<date>_v<version>`, for example
`2026-08-28_v0.1`.

Each run folder holds:

- `questions.jsonl` — the prompts sent for that run, one JSON object per line.
- `judgments.jsonl` — judge-model scores for each response.
- `clusters.jsonl` — cluster assignments from the cluster task.
- `summary.csv` — per-model aggregate scores for the run.
- `manifest.json` — run metadata: date, notebook version, models tested,
  OpenRouter settings, git commit of the notebook used.

`calls.jsonl` (raw API call logs) is written locally by the notebook but
is not committed to this repo. It can contain full prompt and response
text at a volume that does not belong in git history. See `.gitignore`.

Only `README.md` and `.gitkeep` in this `results/` folder are tracked
before a run exists. Everything under `results/<date>_v<version>/` is
produced by running the notebook yourself.
