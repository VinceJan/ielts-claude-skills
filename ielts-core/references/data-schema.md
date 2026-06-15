# IELTS Local Data Schema

All skills share `~/.ielts/`.

## Directory Layout

```text
~/.ielts/
├── profile.md
├── plan.md
├── events.jsonl
├── writing/
├── reading/
├── listening/
├── speaking/
├── vocab/
│   ├── wordbank.md
│   ├── synonyms.md
│   └── review-log.md
└── dashboard/
    └── index.html
```

## Source Of Truth

Use `events.jsonl` as the machine-readable source of truth.

Each line is one JSON object:

```json
{
  "date": "2026-06-12",
  "module": "writing",
  "kind": "correction",
  "source": "Task 2 education essay",
  "metrics": {"overall": 6.5, "tr": 6.5, "cc": 6.0, "lr": 7.0, "gra": 6.5},
  "notes": "Main weakness: CC paragraph progression"
}
```

Allowed `module` values: `diagnose`, `writing`, `reading`, `listening`, `speaking`, `vocab`, `dashboard`.

## Human-Readable Reports

Subject skills may still write detailed Markdown reports:

- `writing/YYYY-MM-DD-task-2-001.md`
- `reading/YYYY-MM-DD-c18t1p2.md`
- `listening/YYYY-MM-DD-c18t1s3.md`
- `speaking/stories.md`

Reports are for review. `events.jsonl` is for dashboard aggregation.

## Vocab Wordbank

`vocab/wordbank.md` table:

```markdown
| 词 | 词性 | 中文 | 语境例句 | 来源 | 状态 | 下次复习 |
|----|------|------|----------|------|------|----------|
| erosion | n. | 侵蚀 | The erosion of the coastline... | C18T1P2 | learning | 2026-06-14 |
```

Status values: `new`, `learning`, `mastered`, `suspended`.

## Logging Rule

When a training interaction produces durable data:

1. Create/update the detailed Markdown report if useful.
2. Record one compact event in `events.jsonl`.
3. Add vocabulary/synonyms through the helper script where possible.
4. Rebuild the dashboard only when the user asks for it, or after a milestone review.
