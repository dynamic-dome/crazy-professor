---
title: crazy-professor — Operating Instructions
status: v0.15.0 (E5 Duet-Mode; E1 Harvest, E2 Dial, E3 Extracted Concepts)
load_when: any invocation, after parsing the trigger
path_convention: all paths are relative to plugin repo root <repo-root> = crazy-professor/
---

# Operating Instructions

Claude follows these steps on every invocation. Steps 1-5 cover the
default single-run path; Steps C1-C6 cover Chat-Mode (`--chat`); Steps
D1-D5 cover Duet-Mode (`--duet`); Step L1 covers `--lab`; Steps H1-H4
cover Harvest (`--harvest`). All file paths are relative to the plugin
repo root (`<repo-root>` = `crazy-professor/`).

## Single-Run Path

**Step 1: Parse the topic.** Strip to a single sentence.

- If `$ARGUMENTS` contains `--lab`: jump to Step L1 (no topic parsing,
  no generation).
- If `$ARGUMENTS` contains `--harvest`: jump to Step H1 (no topic
  parsing, no generation). `--harvest` is standalone; combined with
  `--chat` or a topic, reject with:
  `--harvest is standalone. Run /crazy --harvest on its own.`
- If `$ARGUMENTS` contains `--duet`: jump to Step D1 (checked here,
  BEFORE the single-run/chat resolution below, so a `topic --duet` is
  never mis-routed to single-run). `--duet` takes an optional pair
  argument immediately after the flag (`--duet jester,radagast`);
  without it the picker derives a max-tension pair. `--duet` is mutually
  exclusive with `--chat`, `--lab`, and `--harvest` — reject any
  combination with:
  `--duet cannot be combined with --chat/--lab/--harvest.` A topic is
  mandatory (same rule as chat-mode).
- If `$ARGUMENTS` contains `--dial <n>`: parse n as integer 0-100
  (reject anything else with a one-line error). Default when absent:
  60. With `--chat`, the dial is accepted but only echoed into the
  picker JSON — it does not constrain chat-round generation (note this
  in the run summary if the user passed it explicitly).
- **Single-run with topic** (no `--duet`/`--chat` flag): proceed.
- **Single-run without topic:** use the most recent concrete task,
  plan, or problem from the current conversation as topic. If the
  conversation context is empty, meta, or too vague ("tell me a
  story", "how does this skill work"), ask one clarifying question
  and stop — do not fabricate a topic.
- **Chat-mode with topic:** proceed (jump to Step C1).
- **Chat-mode without topic** (`--chat` flag but no topic text):
  reject explicitly. Return:
  `Chat-mode requires an explicit topic. Run /crazy <topic> --chat or use single-run for ambient topics.`

**Step 2: Pick stochastic elements (picker call).**

```bash
python <repo-root>/skills/crazy-professor/scripts/picker.py \
  --field-notes <target-project>/.agent-memory/lab/crazy-professor/field-notes.md \
  --words <repo-root>/skills/crazy-professor/resources/provocation-words.txt \
  --retired <repo-root>/skills/crazy-professor/resources/retired-words.txt \
  --mode single --dial <dial>
```

Parses one JSON object from stdout: `archetype`, `word`, `operator`,
`re_rolled`, `timestamp`, `dial`, `cost_mix_target` (`{"wild": w,
"tame": t}` — wild = cost `high`/`system-break`, tame = `low`/`medium`).
The variation-guard (3-archetype-streak re-roll, 10-row word-window
dedup) is applied inside the script. The dial also weights the operator
pick (≥75 favors exaggeration/escape, ≤25 favors
reversal/wishful-thinking, mid-range stays equal).

If Python is unavailable, use the prose fallback documented in the
`picker.py` module docstring: `archetype = ARCHETYPES[utc_minute % 4]`,
`operator = OPERATORS[utc_second % 4]`, random word from the active
pool minus retired, then variation-guard manually; `cost_mix_target` =
`wild: round(dial/10)`, `tame: 10 - wild`.

**Step 3: Load the archetype's prompt template.** Read the matching
`<repo-root>/skills/crazy-professor/prompt-templates/<archetype>.md`
file. Its System-Prompt-Kern is the authoritative voice rules.

**Step 4: Generate 10 provocations.** Follow the archetype rules
strictly. Each provocation carries an Adoption-Cost-Tag (`low` |
`medium` | `high` | `system-break`) and a one-phrase anchor. Format
per line:

`<provocation text> -- [cost: <level>] -- anchor: <link>`

The cost tag is honest per provocation — but generation AIMS at the
`cost_mix_target` from Step 2 (Hard Rule 7, Cost-Mix Corridor): out of
10 provocations, ~`wild` should honestly land at `high`/`system-break`
and ~`tame` at `low`/`medium`. Self-check after drafting: count the
honest tags. If the count deviates from the target by more than ±1,
add the one-line cost-mix diagnosis from the output template below the
provocation list. Never re-label a tag to hit the target.

**Step 4b: Extract 3 concepts (Hard Rule 8).** Distill the 10
provocations into exactly 3 transferable mechanism-concepts — de
Bono's movement step. Each concept: a noun phrase, ≥1 source
provocation cited by number, one mechanism sentence (no imperative
form), and 2-3 anchored realization paths at honest cost levels.
Concepts open options; they do not rank or recommend.

**Step 4c: Pick ONE next experiment.** Preferred source: a concept
path from Step 4b (paths are already sized); direct pick from a
provocation remains allowed. Criterion unchanged: testable in under
one hour with tools the user already has.

Write the output file using the frontmatter and body structure
defined in
`<repo-root>/skills/crazy-professor/resources/output-template.md`
(provocations → cost-mix line if due → Extracted Concepts → Next
Experiment → Self-Flag), to path
`<target-project>/.agent-memory/lab/crazy-professor/YYYY-MM-DD-HHMM-<topic-slug>.md`.
Create the directory if it does not exist.

**Step 5: Append a row to field-notes.md.** One Markdown table row in
`<target-project>/.agent-memory/lab/crazy-professor/field-notes.md`
matching the existing table columns (see
`<repo-root>/skills/crazy-professor/resources/field-notes-schema.md`).
At minimum: timestamp, archetype, word, operator, topic slug, output
filename, `re-rolled` value. Default review columns to `pending`.

## Chat-Mode Path (`--chat`)

**Step C1: Parse arguments.** Topic mandatory; reject `--chat` without
topic per Step 1 rule. Optional `--chat --dry-run-round1` runs only
round 1 (internal testing, no round 2/3).

**Step C2: Generate 4 picker calls.**

```bash
python <repo-root>/skills/crazy-professor/scripts/picker.py \
  --field-notes <target-project>/.agent-memory/lab/crazy-professor/field-notes.md \
  --words <repo-root>/skills/crazy-professor/resources/provocation-words.txt \
  --retired <repo-root>/skills/crazy-professor/resources/retired-words.txt \
  --mode chat
```

Returns 4 picks (one per archetype) in a single JSON object. Word-guard
runs intra-chat (no duplicate word within the chat-run; if duplicate,
re-roll with marker `re-rolled: intra-chat`).

**Step C3: Round 1 — 4 parallel LLM calls.** Each archetype with its
standard prompt template + `chat-round-1-wrapper.md` override block.
User message: topic + word + operator. Each archetype returns 5
provocations. Collect all 20.

If ≥2 of 4 archetypes return empty/format-broken output, abort
chat-mode and fall back to a single-run with a note in the output file
that chat-mode failed in round 1.

**Step C4: Round 2 — 4 parallel LLM calls.** Each archetype with its
standard prompt template + `chat-round-2-wrapper.md` override block.
User message: topic + the 15 provocations from the OTHER three
archetypes' round 1. Each archetype returns 2-3 provocations with
`counter:`/`extend:` markers.

Degradation: If ≥2 of 4 archetypes return fewer than 2 provocations,
set `round2_status: degraded` in the frontmatter, skip round-2 outputs
entirely, and pass only round-1 data to round 3. NOT an abort.

**Step C5: Round 3 — Codex distillation.** Invoke `codex:codex-rescue`
subagent with `chat-curator.md` prompt. Direct Markdown return: no
scratch file, no path-only response. Output must have exactly 4
sections × 5 ideas, a Top-3 Cross-Pollination block, and a Next
Experiment block.

If Codex fails (timeout/error/rate-limit) or returns broken structure
after one retry: run the identical distillation prompt through Claude
self-call. Mark `distiller: claude (codex-fallback)` in frontmatter
plus a `distiller_reason`.

**Step C6: Write output + append field-notes row.** Output to
`<target-project>/.agent-memory/lab/crazy-professor/chat/YYYY-MM-DD-HHMM-<topic-slug>.md`
using `chat-output-template.md`. Field-notes row marks `mode: chat`,
`archetype: all-4`, `word: multi`, `operator: multi`. Brief
user-facing summary: topic + 4 picks + round-2 status + distiller +
output-file pointer. Do NOT repeat the 20 final ideas in the chat —
the user reads them in the file.

## Duet-Mode Path (`--duet`)

Duet is the mid-tier between single (1 call) and chat (~10 calls): two
archetypes, a mutual cross-pollination round, and a main-model
distillation — ~4 calls, ~1 minute. It exists to fill the cost gap and
to make the *pairing* itself creative material (break vs. shelter reads
differently than foreign-import vs. self-analysis).

**Step D1: Parse arguments.** Topic mandatory; reject `--duet` without
topic exactly like chat-mode. Optional pair right after the flag
(`--duet jester,radagast`; short or full archetype names). `--duet` is
standalone-generative: never combined with `--chat`/`--lab`/`--harvest`
(rejected in Step 1). `--dial` is accepted and weights the operator
pick per archetype; there is NO hard cost-mix corridor over a duet (too
few final items) — the dial is echoed in the output frontmatter.

**Step D2: Picker call.**

```bash
python <repo-root>/skills/crazy-professor/scripts/picker.py \
  --field-notes <target-project>/.agent-memory/lab/crazy-professor/field-notes.md \
  --words <repo-root>/skills/crazy-professor/resources/provocation-words.txt \
  --retired <repo-root>/skills/crazy-professor/resources/retired-words.txt \
  --mode duet [--pair <a,b>] --dial <dial>
```

Returns one JSON object: `pair` (the two resolved full archetype
names), `picks` (one `{archetype, word, operator, re_rolled}` per
archetype), `re_rolled_aggregate`, `dial`. Without `--pair` the picker
derives a max-tension diagonal (jester×radagast or
librarian×alchemist), seed-rotated by minute. Word-guard runs
intra-duet (no duplicate word across the two; marker `intra-duet`).
Prose fallback if Python is missing: pick the diagonal by
`utc_minute % 2`, then two words/operators as in the single-run
fallback with the intra-duet dedup applied manually.

**Step D3: Round 1 — 2 parallel LLM calls.** Each archetype with its
standard prompt template + the `chat-round-1-wrapper.md` override block
(exactly 5 provocations, no cost-tag, no experiment, no self-flag). The
wrapper's "three other archetypes" framing is cosmetic here — substitute
"one other archetype". User message: topic + word + operator. Each
returns 5 provocations; collect all 10. If EITHER archetype returns
empty/format-broken output, abort duet and fall back to a single-run
with a note in the output file that duet failed in round 1.

**Step D4: Round 2 — 2 parallel LLM calls (mutual cross-pollination).**
Each archetype with its standard template + the
`chat-round-2-wrapper.md` override block, but it sees only the OTHER
archetype's 5 round-1 provocations (not 15). Each returns 2-3
provocations with `counter:`/`extend:` markers, staying strictly in its
own voice. Word/operator carry over from round 1 (no re-roll).

Degradation: if EITHER archetype returns fewer than 2 provocations, set
`round2_status: degraded` in the frontmatter, skip round-2 outputs
entirely, and pass only round-1 data to distillation. NOT an abort.

**Step D5: Distillation — main-model, Top-6 + 1 experiment.** The
main-model (NOT Codex — that is chat-mode's distiller; duet stays cheap
and dependency-free) distills the round-1 + round-2 material into
exactly **6** ideas, each with a `[cost: ...]` tag (assigned here, as in
chat round 3), an anchor, and the W/U/S score from the Review Rubric.
Counter/extend provenance markers are preserved where an idea came from
round 2. The 6 are NOT ranked or crowned (Hard Rule 1) — they are the
distilled survivors. Then pick exactly ONE next experiment (Hard Rule
5), testable within the hour. Honor the cost-tag honesty rule: tags are
honest per idea, never bent.

Write the output using
`<repo-root>/skills/crazy-professor/resources/duet-output-template.md`
to
`<target-project>/.agent-memory/lab/crazy-professor/duet/YYYY-MM-DD-HHMM-<topic-slug>.md`
(create the `duet/` directory if missing). Then append a field-notes
row marking `mode: duet`, `archetype: <a>+<b>`, `word: multi`,
`operator: multi`, with the `re_rolled` aggregate. Brief user-facing
summary: topic + the pair + round-2 status + output-file pointer. Do
NOT repeat the 6 final ideas in the chat — the user reads them in the
file.

## Lab Path (`--lab`, standalone)

**Step L1: Open the static lab.** Verify
`<repo-root>/skills/crazy-professor/lab/index.html` exists. Open it
via Python `webbrowser.open(...)`. Fallback if that fails: print
`Open this file manually: file://<absolute-path>`. No LLM call, no
file write, no field-notes row, no telemetry. Done.

The lab is paste-only: the user pastes an existing crazy-professor
output, scores ideas, copies one experiment card. Browser-side
JavaScript only.

## Harvest Path (`--harvest`, standalone)

Closes the kept-loop: turns `pending` review columns into user
verdicts and lands kept experiments outside the lab folder. Binding
rules in `<repo-root>/skills/crazy-professor/references/hard-rules.md`
("Harvest Rules"). No LLM generation, no picker call, no new output
file.

**Step H1: Collect pending runs.** Read
`<target-project>/.agent-memory/lab/crazy-professor/field-notes.md`.
Select Log rows where `Kept` or `Review1-Votum` is `pending`. If none:
report `Nothing to harvest — all runs reviewed.` and stop. If more
than 5 are pending, take the 5 OLDEST first (announce how many remain).

**Step H2: Triage dialog.** For each selected run, read its output
file and present a compact card: topic, archetype × word × operator,
the Next Experiment paragraph, and the experiment's source provocation
(plus one further provocation if the experiment came from a concept).
Then ask for ONE verdict per run — `kept`, `conditional`, `backlog`,
or `discarded` — plus two optional flags: `retire-word` (output felt
like a near-variation of earlier runs) and `voice-off` (archetype
sounded wrong). Batch the questions (one AskUserQuestion per run, or
one combined prompt for ≤3 runs). A run the user skips stays
`pending` — never infer a verdict.

**Step H3: Record verdicts.** Update the harvested rows in
field-notes.md (this is the sanctioned exception to the
automation-never-edits-review-columns rule — the agent records, the
user judged). Mapping:

| Verdict | Kept | Review1-Votum |
|---|---|---|
| kept | `yes` | `kept` |
| conditional | `pending` (until the named artefact lands) | `conditional` |
| backlog | `no` | `backlog` |
| discarded | `no` | `discarded` |

`retire-word` flag → `Retire-word: yes`, else `no`. `voice-off` flag →
short description string, else `no`. After writing, check the
Field-Test-Rule (any word now at 3 retire-flags → move it to
`retired-words.txt`) and the Museum-Clause counter (≥10 runs reviewed
→ report the kept-count against the 3-of-10 gate; the verdict on the
skill itself belongs to the user).

**Step H4: Land kept experiments.** For every `kept` run, materialize
its Next Experiment outside the lab folder, in this order of
preference: (a) the user's TODO system if available in the environment
(e.g. DCO `tools/add_todo.py` wrapper — announce "→ DCO #NNNN
angelegt"; or a `wiki/wiki/todos/` folder per its README schema);
(b) fallback: append a dated entry to
`<target-project>/.agent-memory/lab/crazy-professor/experiments-backlog.md`
(create with a `# Experiments Backlog` header if missing — one section
per experiment: date, topic, source run file, the experiment
paragraph). Announce every destination in the chat. `conditional`
verdicts get a 14-day deadline note in the same entry instead of a
TODO. End with a one-line harvest summary: N reviewed, counts per
verdict, destinations.
