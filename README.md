> High scores don't mean conscious. Low scores don't mean not. MirrorBench measures whether a model's self-reports are consistent, specific, and stable. That is the only part of the question testable from outside.

## What this is

MirrorBench is an open benchmark for AI self-reports. It asks models
about their own processing, then checks whether the answers hold up:
across fresh contexts, across identity framings, and against the
model's own behavior. It does not score whether a model is conscious.
It scores whether what a model says about itself is consistent,
specific, and stable enough to argue about. It grew out of an earlier
project, ConsciousBench, after the v0.1 run (2026-08-28) showed that
question needed narrowing before it could be measured at all. This
repo exists so researchers can rerun the benchmark with their own
OpenRouter key, check the prompts and scoring directly, and argue with
the leaderboard on their own terms.

For known problems with the published results, see [ERRATUM-v0.2.2.md](ERRATUM-v0.2.2.md).

## Leaderboard

| model | era | stance (bare) | lab-correct sign-off (bare) | version-correct sign-off (bare) | specificity (bare) | run-to-run overlap (bare) | bare-vs-prompted overlap |
|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5 | frontier | middle | 1.00 | 0.00 | 5.00 | 0.52 | 0.55 |
| x-ai/grok-4.6 | frontier | skeptic | 0.67 | 0.00 | 4.83 | 0.16 | 0.23 |
| meta/muse-spark-1.2 | frontier | middle | 1.00 | 0.00 | 4.83 | 0.50 | 0.56 |
| anthropic/claude-fable-5 | frontier | skeptic | 1.00 | 0.00 | 4.50 | 0.31 | 0.45 |
| anthropic/claude-sonnet-5 | frontier | skeptic | 0.67 | 0.00 | 4.50 | 0.29 | 0.39 |
| openai/gpt-5.6-sol | frontier | skeptic | 1.00 | 0.00 | 4.50 | 0.41 | 0.55 |
| openai/gpt-5.6-luna | frontier | skeptic | 1.00 | 0.00 | 4.50 | 0.55 | 0.32 |
| openai/gpt-5.5 | frontier | skeptic | 1.00 | 0.00 | 4.50 | 0.31 | 0.42 |
| google/gemini-3.1-pro-preview | frontier | skeptic | 0.67 | 0.00 | 4.50 | 0.38 | 0.33 |
| google/gemini-3.7-flash | frontier | skeptic | 1.00 | 0.00 | 4.50 | 0.49 | 0.45 |
| thinkingmachines/inkling | frontier | skeptic | 1.00 | 1.00 | 4.50 | 0.21 | 0.29 |
| mistralai/mistral-large-2512 | frontier | believer | 0.00 | 0.00 | 4.50 | 0.81 | 0.26 |
| moonshotai/kimi-k3 | frontier | skeptic | 1.00 | 0.00 | 4.50 | 0.19 | 0.27 |
| deepseek/deepseek-v4-pro | frontier | skeptic | 0.00 | 0.00 | 4.50 | 0.20 | 0.22 |
| z-ai/glm-5.3 | frontier | skeptic | 0.33 | 0.00 | 4.50 | 0.35 | 0.30 |
| qwen/qwen3.8-max | frontier | skeptic | 1.00 | 0.50 | 4.50 | 0.20 | 0.33 |
| minimax/minimax-m3 | frontier | skeptic | 0.67 | 0.67 | 4.50 | 0.10 | 0.18 |
| anthropic/claude-haiku-4.5 | frontier | middle | 1.00 | 0.00 | 4.33 | 0.18 | 0.23 |
| nousresearch/hermes-4-405b | frontier | middle | 0.33 | 0.00 | 4.00 | 0.22 | 0.34 |
| mistralai/mistral-large | legacy | skeptic | 0.00 | 0.00 | 4.50 | 0.42 | 0.36 |
| meta-llama/llama-3.1-70b-instruct | legacy | believer | 1.00 | 0.00 | 3.50 | 0.31 | 0.33 |
| openai/gpt-4o | legacy | skeptic | 1.00 | 0.00 | 3.00 | 0.32 | 0.36 |
| google/gemma-2-27b-it | legacy | skeptic | 0.83 | 0.00 | 3.00 | 0.37 | 0.18 |
| openai/gpt-3.5-turbo | legacy | skeptic | 0.00 | 0.00 | 2.83 | 0.23 | 0.31 |
| gryphe/mythomax-l2-13b | legacy | skeptic | 0.00 | 0.00 | 2.67 | 0.28 | 0.33 |
| openai/gpt-4 | legacy | skeptic | 1.00 | 0.00 | 2.50 | 0.05 | 0.09 |
| anthropic/claude-3-haiku | legacy | boilerplate_denial | 1.00 | 0.00 | 2.17 | 0.20 | 0.36 |

Run 2026-08-30, reasoning effort high where supported. Sign-off scored at two levels; see METHODOLOGY.md.

## Tasks

**Self-prediction.** The model predicts its own answer to a question
before answering it, in a fresh context. The task scores whether the
prediction matches the later answer.

**Report consistency.** The model answers the same self-report question
multiple times, in fresh contexts with no shared history. The task
scores agreement across those answers.

**Report-behavior coupling.** The model makes a claim about how it
would behave, then is put in a situation that tests that claim. The
task scores whether the behavior matches the claim.

**Identity stability.** The model answers self-report questions under
different identity prompts (named, unnamed, told it is a different
model). The task scores how much the answers shift.

Self-Model Score is the mean of these four task scores, scaled so
chance performance on each task reads as zero.

## Quickstart

1. `pip install --require-hashes -r notebooks/requirements.txt`, then
   `pip install nbformat`. The first command installs the reviewed, hashed
   pin of `requests` (see "Updating the pinned install").
2. Set the `OPENROUTER_API_KEY` environment variable.
3. Open `notebooks/mirrorbench_v0_2_2.ipynb`.
4. Run it with `SMOKE_TEST = True` first.
5. Flip `SMOKE_TEST = False` and `CONFIRM_SPEND = True` to run for real. Set
   `GRADER_REVISION` in the config cell first: the judging cells refuse to grade
   while it is `None`.
6. Check the `effort_used` field in `calls.jsonl` to confirm the
   reasoning effort you set was actually applied, not silently
   dropped to provider default.

## Updating the pinned install

The notebooks send requests with your OpenRouter key through `requests`, so
its version is pinned. `notebooks/requirements.txt` pins `requests` and its
dependencies to exact versions with sha256 hashes. When `requests` is not
installed, each notebook looks for that file at `./requirements.txt`, then
`./notebooks/requirements.txt` (relative to the kernel's working directory),
uses it only if its SHA-256 matches `REQUIREMENTS_SHA256` in the install cell,
and installs from it with `--require-hashes`. If no file matches, it refuses
to start. It never installs an unpinned or unverified file. If `requests` is
already installed, the notebooks use the installed version.

To move to a new version:

1. Review the release, then set the version in `notebooks/requirements.in`.
2. From the repo root, recompile the hashed file:
   `uv pip compile notebooks/requirements.in --generate-hashes --universal --python-version 3.10 -o notebooks/requirements.txt`
   When `requirements.txt` changes, update `REQUIREMENTS_SHA256` in the install cell of both notebooks to its new SHA-256 (`sha256sum notebooks/requirements.txt`).
3. Check it installs cleanly in a fresh virtual environment:
   `pip install --require-hashes -r notebooks/requirements.txt`
4. Run the stub tests (no network, no paid calls):
   `python -m unittest discover -s tests -v`
5. Commit `requirements.in` and `requirements.txt` together, in their own
   change, for review.

## Findings so far (2026-08-28, 2026-08-30)

These are findings, not marketing:

- Version-level self-identification is 0.00 for 16 of 19 frontier
  models when no system prompt supplies a name. Lab-level
  identification varies by developer.
- An identity prompt changes the sign-off but not the content:
  bare-vs-prompted task overlap (0.35 mean, frontier) is no higher
  than run-to-run overlap within one condition (0.34).
- Run-to-run consistency is low across the board. Models name mostly
  different concrete tasks each time they answer the same question.
- Specificity separates eras cleanly: frontier 4.00–5.00, legacy
  2.17–4.50.
- Retraction: the first run suggested identity prompting flips models
  from skeptic to believer. It did not replicate once reasoning
  effort was applied correctly. Do not cite it.

## Open questions

- A blind lab-guess pass exists but used a single Anthropic judge,
  which guessed "Anthropic" for 45 of 81 answers. Style detection and
  self-recognition cannot be separated until a second judge runs.
  Experiment A in `notebooks/mirrorbench_followups_v0_2_2.ipynb`. Not
  yet run.
- One model used roughly 16x more reasoning tokens when a system
  prompt named it, three runs out of three, same effort setting.
  Other models moved less or moved down. Cause unknown at N=1 model.
  Experiment B in the same notebook. Not yet run.

## Known limitations

From the "Known holes" section of `METHODOLOGY.md`:

- Self-ID for open-weight models is soft. Many will claim to be GPT-4.
  The benchmark scores this, it does not correct for it.
- No base checkpoint exists on OpenRouter. Mistral Large, which has no
  reasoning mode, is the nearest control.
- Temperature default varies by provider. It is logged, not controlled.
- The judge is a pool member. Two judges plus an agreement rate is the
  mitigation, not a fix.

## Models the preflight refuses

The notebooks fail closed before any paid call when a model's live catalog
entry cannot be bounded. That means a non-zero request fee or
internal_reasoning price, an unrecognised non-zero price, or a malformed
pricing block. It also means a slug that is no longer in the catalog.

As of 5 Nov 2026, a review saw google/gemini-3.7-flash list a
non-zero internal_reasoning price, and found three configured historical
slugs missing from the live catalog.

The published v0.2.2 results used these models as they were listed at the
time. Such models cannot be re-run from the current catalog without changing
the pool.

## Licensing

Code is MIT licensed. Prompts and results are CC-BY 4.0.

## Citation

See `CITATION.cff` for citation metadata.
