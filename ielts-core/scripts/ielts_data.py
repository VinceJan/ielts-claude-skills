#!/usr/bin/env python3
"""Small deterministic helper for the IELTS skills local data store."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
from pathlib import Path
from typing import Any


MODULES = {"diagnose", "writing", "reading", "listening", "speaking", "vocab", "dashboard"}


def root() -> Path:
    return Path(os.environ.get("IELTS_HOME", Path.home() / ".ielts")).expanduser()


def today() -> str:
    return dt.date.today().isoformat()


def ensure_layout(base: Path) -> None:
    for name in ["writing", "reading", "listening", "speaking", "vocab", "dashboard"]:
        (base / name).mkdir(parents=True, exist_ok=True)
    events = base / "events.jsonl"
    events.touch(exist_ok=True)
    wordbank = base / "vocab" / "wordbank.md"
    if not wordbank.exists():
        wordbank.write_text(
            "# 生词库\n\n"
            "| 词 | 词性 | 中文 | 语境例句 | 来源 | 状态 | 下次复习 |\n"
            "|----|------|------|----------|------|------|----------|\n",
            encoding="utf-8",
        )
    synonyms = base / "vocab" / "synonyms.md"
    if not synonyms.exists():
        synonyms.write_text(
            "# 同义替换库\n\n"
            "| 题目用词 | 原文用词 | 出处 | 状态 |\n"
            "|----------|----------|------|------|\n",
            encoding="utf-8",
        )


def parse_metrics(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--metrics must be valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("--metrics must decode to a JSON object")
    return value


def cmd_init(_: argparse.Namespace) -> None:
    base = root()
    ensure_layout(base)
    print(base)


def cmd_record(args: argparse.Namespace) -> None:
    if args.module not in MODULES:
        raise SystemExit(f"--module must be one of: {', '.join(sorted(MODULES))}")
    base = root()
    ensure_layout(base)
    event = {
        "date": args.date or today(),
        "module": args.module,
        "kind": args.kind,
        "source": args.source or "",
        "metrics": parse_metrics(args.metrics),
        "notes": args.notes or "",
    }
    with (base / "events.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps(event, ensure_ascii=False, sort_keys=True))


def table_has_word(path: Path, word: str, source: str) -> bool:
    if not path.exists():
        return False
    target = word.strip().lower()
    src = source.strip().lower()
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = [p.strip().lower() for p in line.strip("|").split("|")]
        if len(parts) >= 5 and parts[0] == target and (not src or parts[4] == src):
            return True
    return False


def cmd_vocab_add(args: argparse.Namespace) -> None:
    base = root()
    ensure_layout(base)
    path = base / "vocab" / "wordbank.md"
    if table_has_word(path, args.word, args.source or ""):
        print("exists")
        return
    next_review = args.next_review or (dt.date.today() + dt.timedelta(days=1)).isoformat()
    row = (
        f"| {args.word} | {args.pos or ''} | {args.meaning or ''} | "
        f"{args.example or ''} | {args.source or ''} | learning | {next_review} |\n"
    )
    with path.open("a", encoding="utf-8") as fh:
        fh.write(row)
    print("added")


def load_events(base: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    path = base / "events.jsonl"
    if not path.exists():
        return events
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def count_wordbank(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    total = mastered = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|----") or "词 |" in line:
            continue
        total += 1
        if "| mastered |" in line or "| ✅ |" in line:
            mastered += 1
    return total, mastered


def latest_metric(events: list[dict[str, Any]], module: str, key: str) -> Any:
    for event in reversed(events):
        if event.get("module") == module:
            metrics = event.get("metrics") or {}
            if key in metrics:
                return metrics[key]
    return "—"


def cmd_build_dashboard(_: argparse.Namespace) -> None:
    base = root()
    ensure_layout(base)
    events = load_events(base)
    vocab_total, vocab_mastered = count_wordbank(base / "vocab" / "wordbank.md")
    rows = []
    for event in events[-20:]:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(event.get('date', '')))}</td>"
            f"<td>{html.escape(str(event.get('module', '')))}</td>"
            f"<td>{html.escape(str(event.get('kind', '')))}</td>"
            f"<td>{html.escape(json.dumps(event.get('metrics', {}), ensure_ascii=False))}</td>"
            f"<td>{html.escape(str(event.get('notes', '')))}</td>"
            "</tr>"
        )
    content = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IELTS Dashboard</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:0;background:#f8fafc;color:#0f172a}}
main{{max-width:1080px;margin:0 auto;padding:24px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}
.card{{background:white;border:1px solid #e2e8f0;border-radius:8px;padding:16px}}
.num{{font-size:32px;font-weight:700}}
table{{width:100%;border-collapse:collapse;background:white;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden}}
th,td{{padding:10px;border-bottom:1px solid #e2e8f0;text-align:left;font-size:14px;vertical-align:top}}
th{{background:#e0f2fe}}
</style>
</head>
<body><main>
<h1>IELTS Dashboard</h1>
<p>Generated {today()} from {html.escape(str(base))}</p>
<section class="grid">
<div class="card"><div>Writing</div><div class="num">{latest_metric(events, 'writing', 'overall')}</div></div>
<div class="card"><div>Reading</div><div class="num">{latest_metric(events, 'reading', 'accuracy')}</div></div>
<div class="card"><div>Listening</div><div class="num">{latest_metric(events, 'listening', 'accuracy')}</div></div>
<div class="card"><div>Vocab</div><div class="num">{vocab_mastered}/{vocab_total}</div></div>
</section>
<h2>Recent Events</h2>
<table><thead><tr><th>Date</th><th>Module</th><th>Kind</th><th>Metrics</th><th>Notes</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
</main></body></html>"""
    output = base / "dashboard" / "index.html"
    output.write_text(content, encoding="utf-8")
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="IELTS local data helper")
    sub = parser.add_subparsers(required=True)

    init_p = sub.add_parser("init")
    init_p.set_defaults(func=cmd_init)

    rec_p = sub.add_parser("record")
    rec_p.add_argument("--module", required=True)
    rec_p.add_argument("--kind", required=True)
    rec_p.add_argument("--source")
    rec_p.add_argument("--metrics")
    rec_p.add_argument("--notes")
    rec_p.add_argument("--date")
    rec_p.set_defaults(func=cmd_record)

    vocab_p = sub.add_parser("vocab-add")
    vocab_p.add_argument("--word", required=True)
    vocab_p.add_argument("--pos")
    vocab_p.add_argument("--meaning")
    vocab_p.add_argument("--example")
    vocab_p.add_argument("--source")
    vocab_p.add_argument("--next-review")
    vocab_p.set_defaults(func=cmd_vocab_add)

    dash_p = sub.add_parser("build-dashboard")
    dash_p.set_defaults(func=cmd_build_dashboard)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
