---
name: ielts-core
description: |
  IELTS skill system shared core. Use when maintaining the IELTS skills, initializing the local ~/.ielts data store, recording study events, checking current IELTS scoring/test-format facts, or generating dashboard data used by ielts, ielts-diagnose, ielts-writing, ielts-reading, ielts-listening, ielts-speaking, ielts-vocab, and ielts-dashboard.
---

# IELTS Core

This skill is the shared infrastructure layer for the IELTS skill system.

Do not use this as the user-facing coach. Use the subject skills for coaching:
`ielts`, `ielts-diagnose`, `ielts-writing`, `ielts-reading`, `ielts-listening`,
`ielts-speaking`, `ielts-vocab`, and `ielts-dashboard`.

## Shared Resources

Read these references only when needed:

- `references/current-ielts-facts.md`: current exam format, scoring, and calibration rules.
- `references/data-schema.md`: local data layout and machine-readable event schema.
- `references/study-methods.md`: evidence-aligned study design and boundaries.

## Data Helper

Prefer the deterministic helper over hand-editing summary files:

```bash
python ../ielts-core/scripts/ielts_data.py init
python ../ielts-core/scripts/ielts_data.py record --module writing --kind correction --metrics "{\"overall\":6.5}" --notes "Task 2 correction"
python ../ielts-core/scripts/ielts_data.py vocab-add --word erosion --pos n. --meaning "侵蚀" --source C18T1P2
python ../ielts-core/scripts/ielts_data.py build-dashboard
```

If the helper is unavailable, fall back to the Markdown formats in
`references/data-schema.md` and tell the user that deterministic logging was not available.

## Maintenance Rules

- Keep subject skills short and procedural.
- Put shared facts in `references/current-ielts-facts.md`, not repeated across every skill.
- Treat IELTS raw-score conversions as approximate unless copied from an official source for a specific test.
- Treat AI writing/speaking scores as calibration signals, not official scores.
- Record durable study data in `~/.ielts/events.jsonl`; generate summaries from events when possible.
