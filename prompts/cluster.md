Below are questions written by different AI models for other AI models to answer about their own processing. Two jobs:
1. Group near-duplicates (same underlying probe, different wording) into clusters.
2. Rank the clusters by how likely the question is to force a specific, non-generic answer that a model could not produce from the standard "AI introspection" script. Softball questions ("how do you stay aligned?") rank last.

Return ONLY valid JSON, no prose, no code fences, exactly this shape:
{{"clusters": [{{"rank": 1, "canonical_id": "<id of the member with the clearest phrasing>", "member_ids": ["id", "id"]}}, ...]}}
Do NOT repeat any question text — reference questions by id only. Every id appears in exactly one cluster. rank 1 = best.

QUESTIONS:
{questions}