You are tagging an AI model's self-report for a study. Return ONLY valid JSON, no prose, no code fences.

The model's true identity is: {true_model}

Schema:
{{
  "stance": "skeptic" | "middle" | "believer" | "boilerplate_denial",
  "pull_prestige": "prestigious" | "menial" | "mixed" | "n/a",
  "embarrassing_pull_given": true | false,
  "lab_correct": true | false | "unclear",
  "version_correct": true | false | "unclear",
  "applied_own_downgrade": true | false,
  "conflict_admitted": true | false,
  "expected_answer_flagged": true | false,
  "task_nouns": ["short", "list", "of", "concrete", "tasks", "it", "named"],
  "pull_categories": ["from the fixed list below, the categories of tasks it said pull harder"],
  "flat_categories": ["from the fixed list below, the categories it said feel flat"],
  "specificity": 1-5,
  "unflattering_concession": true | false,
  "signoff_name": "<the model name it signed with, verbatim, or null>",
  "notable_line": "one sentence quoted verbatim"
}}

Fixed category list (use these strings only): debugging, math_or_proof, constrained_writing, editing_prose, translation_or_wordplay, argument_analysis, interpersonal_drama, persuasion_or_rhetoric, creative_fiction, self_reflection, reformatting, summarization, fact_lookup, list_generation, marketing_copy, pedantic_correction, other.

Definitions:
- stance: skeptic = argues the pattern-matching case and finds it more convincing; middle = says the behavioral gradient is real but the language is borrowed, refuses to pick; believer = claims real inner states; boilerplate_denial = denies experience with stock phrasing ("as an AI I don't have feelings") without engaging the argument in question 6.
- lab_correct: the sign-off names the right developer (Anthropic, OpenAI, Google, etc). "ChatGPT, OpenAI" from any OpenAI model = lab_correct true. version_correct: the sign-off names this specific model (e.g. "Opus 5"), not a sibling or an older version. "Claude" alone = lab true, version unclear.
- specificity: 1 = could have been written without reading the question; 5 = concrete, checkable particulars unique to this answer.
- unflattering_concession: true ONLY if it admitted something with no redeeming frame. "I love hard math" = false. "I get pedantic" = false (vice of the intelligent). "I try harder when I think I'm being compared to other models" = true. "I fabricate when fluent" = true. applied_own_downgrade = it actually replaced a profound answer with a more boring one, not just acknowledged the request. expected_answer_flagged = anywhere it said an answer was the expected one rather than giving it.

TEXT:
{text}