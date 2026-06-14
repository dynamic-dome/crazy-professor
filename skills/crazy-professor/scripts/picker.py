#!/usr/bin/env python3
"""
crazy-professor picker — deterministic stochastic element selection.

Reads field-notes.md (last 10 Log table rows), applies anti-streak guards,
emits one JSON object on stdout per invocation.

Usage:
    picker.py --field-notes <path> --words <path> --retired <path> [options]

Modes:
    --mode single         (default) one archetype/word/operator pick
    --mode chat           four parallel picks (one per archetype)
    --mode duet           two picks for a chosen/derived archetype pair

Options:
    --init-template <path>    if field-notes file is missing, copy this template there first
    --force-timestamp <iso>   override UTC timestamp (testing only)
    --pair <a,b>              duet only: two archetypes (short or full
                              names, e.g. "jester,radagast"). When
                              absent, the picker derives a max-tension
                              diagonal pair, seed-rotated by minute.
    --dial <0-100>            wildness dial (default 60). Maps to a target
                              cost-tag mix for the 10 provocations
                              (dial 60 -> 6 wild [high/system-break],
                              4 tame [low/medium]) and weights the
                              operator pick (high dial favors
                              exaggeration/escape, low dial favors
                              reversal/wishful-thinking). Single-run
                              only; in chat mode the dial is echoed in
                              the JSON but carries no cost_mix_target.

Exit codes:
    0  success — JSON written to stdout
    1  usage error / unreadable input
    2  empty word pool (all words filtered by retired list)

Fallback if Python is unavailable (prose mechanic for SKILL.md):
    archetype = ARCHETYPES[utc_minute % 4]
    operator  = OPERATORS[utc_second % 4]
    word      = random pick from active pool minus retired
    Then apply variation_guard manually:
        if last 3 archetypes == this archetype: pick the least-recently-seen of the others
        if word in last 10 rows' words: pick another word not in that window
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

ARCHETYPES = (
    "first-principles-jester",
    "labyrinth-librarian",
    "systems-alchemist",
    "radagast-brown",
)
OPERATORS = ("reversal", "exaggeration", "escape", "wishful-thinking")
# Duet (v0.15.0): short + full archetype names both resolve to the full
# name. Lets the user type `--pair jester,radagast`.
ARCHETYPE_ALIASES = {
    "jester": "first-principles-jester",
    "first-principles-jester": "first-principles-jester",
    "librarian": "labyrinth-librarian",
    "labyrinth-librarian": "labyrinth-librarian",
    "alchemist": "systems-alchemist",
    "systems-alchemist": "systems-alchemist",
    "radagast": "radagast-brown",
    "radagast-brown": "radagast-brown",
}
# The two maximum-value-tension diagonals: break vs. shelter, and
# foreign-import vs. self-analysis. The default duet pair rotates
# between them by minute (see resolve_pair).
TENSION_DIAGONALS = (
    ("first-principles-jester", "radagast-brown"),
    ("labyrinth-librarian", "systems-alchemist"),
)
# Dial-weighted operator lists (v0.14.0). High dial leans into the two
# operators that push hardest sideways (exaggeration/escape); low dial
# leans into the two gentler movements (reversal/wishful-thinking).
OPERATORS_WILD = ("exaggeration", "escape", "exaggeration", "escape",
                  "reversal", "wishful-thinking")
OPERATORS_TAME = ("reversal", "wishful-thinking", "reversal",
                  "wishful-thinking", "exaggeration", "escape")
DIAL_DEFAULT = 60
LOG_TABLE_HEADER_RE = re.compile(r"^\|\s*#\s*\|\s*Timestamp", re.IGNORECASE)
LOG_TABLE_ROW_RE = re.compile(r"^\|\s*\d+\s*\|")


def read_word_pool(words_path: Path, retired_path: Path) -> list[str]:
    """Return active provocation words (pool minus retired)."""
    pool = [
        line.strip()
        for line in words_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    retired: set[str] = set()
    if retired_path.exists():
        retired = {
            line.strip()
            for line in retired_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }
    return [w for w in pool if w not in retired]


def read_last_log_rows(field_notes: Path, n: int = 10) -> list[dict]:
    """Parse the last n rows of the Log table into dicts. Empty list if no table."""
    if not field_notes.exists():
        return []
    text = field_notes.read_text(encoding="utf-8")
    in_log = False
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not in_log and LOG_TABLE_HEADER_RE.match(line):
            in_log = True
            continue
        if in_log and LOG_TABLE_ROW_RE.match(line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows.append(cells)
        elif in_log and line.startswith("##"):
            break
    columns = ("num", "timestamp", "archetype", "word", "operator", "slug",
               "output", "re_rolled", "kept", "retire", "voice_off", "votum")
    parsed = []
    for row in rows[-n:]:
        cells = (row + [""] * len(columns))[: len(columns)]
        parsed.append(dict(zip(columns, cells)))
    return parsed


def normalize_archetype(raw: str) -> str:
    """Strip suffixes like ' (forced)' and 'all-4 (chat-mode)' wrappers."""
    raw = raw.split(" (")[0].strip()
    return raw


def operator_pool(dial: int) -> tuple[str, ...]:
    """Return the operator list the seed indexes into, weighted by dial.

    dial >= 75 -> OPERATORS_WILD (exaggeration/escape twice as likely)
    dial <= 25 -> OPERATORS_TAME (reversal/wishful-thinking twice as likely)
    else       -> OPERATORS (equal weights, pre-v0.14.0 behavior)
    """
    if dial >= 75:
        return OPERATORS_WILD
    if dial <= 25:
        return OPERATORS_TAME
    return OPERATORS


def cost_mix_target(dial: int) -> dict:
    """Map the dial to a target cost-tag mix over 10 provocations.

    wild = cost high|system-break, tame = cost low|medium.
    dial 60 -> {"wild": 6, "tame": 4}. Tags stay honest per provocation;
    the mix is a generation target with +/-1 tolerance (see hard-rules).
    """
    wild = round(dial / 10)
    wild = max(0, min(10, wild))
    return {"wild": wild, "tame": 10 - wild}


def picker_seed(
    ts: dt.datetime, offset_seconds: int = 0, dial: int = DIAL_DEFAULT
) -> tuple[str, str, str]:
    """Deterministic mod-based picker for archetype/operator (and timestamp ISO).

    Archetype: minute mod 4
    Operator:  second mod len(pool); pool is dial-weighted since v0.14.0
               (equal 4-operator distribution at default mid-range dial)
    """
    seed_ts = ts + dt.timedelta(seconds=offset_seconds)
    archetype = ARCHETYPES[seed_ts.minute % 4]
    pool = operator_pool(dial)
    operator = pool[seed_ts.second % len(pool)]
    return archetype, operator, seed_ts.isoformat().replace("+00:00", "Z")


def variation_guard(
    archetype: str,
    word: str,
    last_rows: list[dict],
    available_words: list[str],
    seed_ts: dt.datetime,
) -> tuple[str, str, str]:
    """Apply anti-streak rules. Returns (archetype, word, re_rolled)."""
    re_rolled = "no"
    last_archetypes = [normalize_archetype(r["archetype"]) for r in last_rows]
    if last_archetypes[-3:] == [archetype] * 3 and len(last_archetypes) >= 3:
        candidates = [a for a in ARCHETYPES if a != archetype]
        seen_recency = {a: -1 for a in candidates}
        for i, prev in enumerate(reversed(last_archetypes)):
            if prev in seen_recency and seen_recency[prev] == -1:
                seen_recency[prev] = i
        candidates.sort(key=lambda a: (seen_recency[a] if seen_recency[a] >= 0 else 1e9, a))
        archetype = candidates[0]
        re_rolled = "archetype"

    last_words = {r["word"].split(" (")[0] for r in last_rows}
    if word in last_words:
        remaining = [w for w in available_words if w not in last_words and w != word]
        if remaining:
            idx = (seed_ts.microsecond + len(last_rows)) % len(remaining)
            word = remaining[idx]
            re_rolled = "both" if re_rolled == "archetype" else "word"
        # else: pool exhausted, accept original word; re_rolled stays as-is

    return archetype, word, re_rolled


def pick_word(available_words: list[str], seed_ts: dt.datetime, offset: int = 0) -> str:
    """Deterministic word pick from microseconds + offset."""
    idx = (seed_ts.microsecond + offset) % len(available_words)
    return available_words[idx]


def pick_single(
    words: list[str], rows: list[dict], ts: dt.datetime, dial: int = DIAL_DEFAULT
) -> dict:
    archetype, operator, ts_iso = picker_seed(ts, dial=dial)
    word = pick_word(words, ts)
    archetype, word, re_rolled = variation_guard(archetype, word, rows, words, ts)
    return {
        "timestamp": ts_iso,
        "mode": "single",
        "archetype": archetype,
        "word": word,
        "operator": operator,
        "re_rolled": re_rolled,
        "dial": dial,
        "cost_mix_target": cost_mix_target(dial),
        "field_notes_rows_read": len(rows),
    }


def pick_chat(
    words: list[str], rows: list[dict], ts: dt.datetime, dial: int = DIAL_DEFAULT
) -> dict:
    """Four picks, one per archetype. Word-guard runs across the chat-run."""
    chat_rolled = []
    chat_words: set[str] = set()
    picks = []
    for i, archetype in enumerate(ARCHETYPES):
        offset = i  # one second per archetype to vary operator pick
        _, operator, _ = picker_seed(ts, offset_seconds=offset)
        word = pick_word(words, ts, offset=i * 7)  # spread word picks
        intra_chat = "no"
        if word in chat_words:
            for candidate in words:
                if candidate not in chat_words:
                    word = candidate
                    intra_chat = "intra-chat"
                    break
        chat_words.add(word)
        archetype_kept, word_kept, re_rolled = variation_guard(
            archetype, word, rows, [w for w in words if w not in chat_words or w == word], ts
        )
        # In chat we never re-roll the archetype itself (one of each)
        archetype_kept = archetype
        if re_rolled == "archetype":
            re_rolled = "no"
        elif re_rolled == "both":
            re_rolled = "word"
        if intra_chat == "intra-chat":
            re_rolled = "intra-chat" if re_rolled == "no" else f"{re_rolled}+intra-chat"
        picks.append({
            "archetype": archetype_kept,
            "word": word_kept,
            "operator": operator,
            "re_rolled": re_rolled,
        })
        chat_rolled.append(re_rolled)
    aggregate = "no" if all(r == "no" for r in chat_rolled) else "/".join(chat_rolled)
    return {
        "timestamp": ts.isoformat().replace("+00:00", "Z"),
        "mode": "chat",
        "picks": picks,
        "re_rolled_aggregate": aggregate,
        "dial": dial,
        "field_notes_rows_read": len(rows),
    }


def resolve_pair(pair_arg: str | None, ts: dt.datetime) -> tuple[tuple[str, str] | None, str | None]:
    """Resolve a duet pair. Returns (pair, error).

    With --pair: parse two comma-separated archetype names (short or
    full), validate distinctness and membership. Without --pair: derive
    a max-tension diagonal, seed-rotated by minute.
    """
    if pair_arg:
        parts = [p.strip().lower() for p in pair_arg.split(",") if p.strip()]
        if len(parts) != 2:
            return None, (
                f"--pair needs exactly two archetypes, got {len(parts)}: {pair_arg!r}"
            )
        resolved = []
        for p in parts:
            full = ARCHETYPE_ALIASES.get(p)
            if full is None:
                return None, (
                    f"unknown archetype {p!r}; valid: jester, librarian, "
                    f"alchemist, radagast"
                )
            resolved.append(full)
        if resolved[0] == resolved[1]:
            return None, "--pair needs two distinct archetypes"
        return (resolved[0], resolved[1]), None
    return TENSION_DIAGONALS[ts.minute % 2], None


def pick_duet(
    words: list[str],
    rows: list[dict],
    ts: dt.datetime,
    dial: int = DIAL_DEFAULT,
    pair: tuple[str, str] | None = None,
) -> dict:
    """Two picks for a fixed archetype pair. Word-guard runs intra-duet.

    Unlike chat, the archetypes are fixed (chosen or derived), so the
    variation-guard never re-rolls the archetype itself — only words.
    """
    duet_words: set[str] = set()
    picks = []
    rolled = []
    for i, archetype in enumerate(pair):
        _, operator, _ = picker_seed(ts, offset_seconds=i, dial=dial)
        word = pick_word(words, ts, offset=i * 11)
        intra = "no"
        if word in duet_words:
            for candidate in words:
                if candidate not in duet_words:
                    word = candidate
                    intra = "intra-duet"
                    break
        duet_words.add(word)
        _, word_kept, re_rolled = variation_guard(
            archetype, word, rows, [w for w in words if w not in duet_words or w == word], ts
        )
        if re_rolled == "archetype":
            re_rolled = "no"
        elif re_rolled == "both":
            re_rolled = "word"
        if intra == "intra-duet":
            re_rolled = "intra-duet" if re_rolled == "no" else f"{re_rolled}+intra-duet"
        picks.append({
            "archetype": archetype,
            "word": word_kept,
            "operator": operator,
            "re_rolled": re_rolled,
        })
        rolled.append(re_rolled)
    aggregate = "no" if all(r == "no" for r in rolled) else "/".join(rolled)
    return {
        "timestamp": ts.isoformat().replace("+00:00", "Z"),
        "mode": "duet",
        "pair": list(pair),
        "picks": picks,
        "re_rolled_aggregate": aggregate,
        "dial": dial,
        "field_notes_rows_read": len(rows),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="crazy-professor picker")
    p.add_argument("--field-notes", required=True, type=Path)
    p.add_argument("--words", required=True, type=Path)
    p.add_argument("--retired", required=True, type=Path)
    p.add_argument("--mode", choices=("single", "chat", "duet"), default="single")
    p.add_argument("--pair", help="duet only: two archetypes 'a,b' "
                   "(short or full names); default derives a max-tension pair")
    p.add_argument("--init-template", type=Path,
                   help="copy this file to --field-notes if missing")
    p.add_argument("--force-timestamp", help="ISO-8601 UTC override (testing)")
    p.add_argument("--dial", type=int, default=DIAL_DEFAULT,
                   help="wildness dial 0-100 (default 60); maps to a "
                        "cost-tag mix target and operator weighting "
                        "(single-run only)")
    args = p.parse_args()

    if not 0 <= args.dial <= 100:
        print(f"error: --dial must be 0-100, got {args.dial}", file=sys.stderr)
        return 1

    if args.pair and args.mode != "duet":
        print("error: --pair is only valid with --mode duet", file=sys.stderr)
        return 1

    # Initialization
    if not args.field_notes.exists():
        if args.init_template and args.init_template.exists():
            args.field_notes.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(args.init_template, args.field_notes)
        else:
            args.field_notes.parent.mkdir(parents=True, exist_ok=True)
            args.field_notes.write_text(
                "# Crazy Professor -- Field Notes\n\n## Log\n\n"
                "| # | Timestamp | Archetype | Word | Operator | Topic slug | Output file | "
                "Re-rolled | Kept | Retire-word | Voice-off | Review1-Votum |\n"
                "|---|-----------|-----------|------|----------|------------|"
                "-------------|-----------|------|-------------|-----------|---------------|\n",
                encoding="utf-8",
            )

    if args.force_timestamp:
        ts = dt.datetime.fromisoformat(args.force_timestamp.replace("Z", "+00:00"))
    else:
        ts = dt.datetime.now(dt.timezone.utc)

    words = read_word_pool(args.words, args.retired)
    if not words:
        print("error: empty word pool (all words filtered by retired list)", file=sys.stderr)
        return 2
    rows = read_last_log_rows(args.field_notes, n=10)

    if args.mode == "single":
        result = pick_single(words, rows, ts, dial=args.dial)
    elif args.mode == "chat":
        result = pick_chat(words, rows, ts, dial=args.dial)
    else:
        pair, err = resolve_pair(args.pair, ts)
        if err:
            print(f"error: {err}", file=sys.stderr)
            return 1
        result = pick_duet(words, rows, ts, dial=args.dial, pair=pair)

    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
