# Duet-Mode Output Template

Every `--duet` invocation produces a Markdown file in this exact shape.
The skill fills in the angle-bracketed fields.

Pfad: `.agent-memory/lab/crazy-professor/duet/YYYY-MM-DD-HHMM-<topic-slug>.md`

---

```markdown
---
skill: crazy-professor
mode: duet
version: 0.15.0
timestamp: <ISO-8601 UTC>
topic: "<user input, one line, unmodified>"
pair: [<archetype-a>, <archetype-b>]
rounds: 2
distiller: main-model
dial: <0-100, echoed from the picker JSON; default 60>
picks:
  <archetype-a>: { word: <w>, operator: <op> }
  <archetype-b>: { word: <w>, operator: <op> }
round2_status: <full | degraded>
round2_reason: <only if degraded: why>
llm_calls: <number, expected 4 (2 round-1 + 2 round-2); distillation is inline>
---

# Duet: <topic>

**Mode:** duet | **Pair:** <archetype-a> × <archetype-b> | **Distiller:** main-model | **Dial:** <dial>

> DIVERGENCE WARNING: This output is provocation material, not advice.
> The ideas below are deliberately exaggerated, one-sided, or absurd.
> They exist to destabilize fixed thinking, not to be implemented as-is.
> Do not read this as recommendation. Do not cite this as analysis.
> The six distilled ideas are survivors of a two-voice crossing, still
> provocations — not a ranking, not a winner. Pick what moves you,
> discard the rest, and use the "Next Experiment" section to turn one
> nudge into something testable.

## Round 1 — Two Voices (5 Provocations each)

### <Archetype-A> (word: <w>, operator: <op>)

1. <provocation> — anchor: <link>
2. <provocation> — anchor: <link>
3. <provocation> — anchor: <link>
4. <provocation> — anchor: <link>
5. <provocation> — anchor: <link>

### <Archetype-B> (word: <w>, operator: <op>)

1. <provocation> — anchor: <link>
2. <provocation> — anchor: <link>
3. <provocation> — anchor: <link>
4. <provocation> — anchor: <link>
5. <provocation> — anchor: <link>

## Round 2 — Cross-Pollination (2-3 each, counter/extend)

Wenn round2_status: degraded: dieser Block traegt einen Disclaimer am
Anfang: "Runde 2 degradiert: einer der zwei Archetypen lieferte unter 2
Provokationen. Nur Runde-1-Daten sind in die Destillation eingeflossen."

### <Archetype-A> — Runde 2

- counter: <archetype-b> #<n> — <provokation> — anchor: <link>
- extend: <archetype-b> #<n> — <provokation> — anchor: <link>

### <Archetype-B> — Runde 2

- counter: <archetype-a> #<n> — <provokation> — anchor: <link>
- extend: <archetype-a> #<n> — <provokation> — anchor: <link>

## Distillation — The Six (main-model)

*Exactly 6 ideas distilled from rounds 1-2. Scoring: W = Wert,
U = Umsetzbarkeit, S = Systemfit (each 1-5). Cost-Tag: low | medium |
high | system-break (honest per idea, assigned here). Counter/extend
provenance preserved where the idea came from round 2. These six are
NOT ranked and NOT a winner — they are the survivors.*

1. <idee> — [cost: X] — anchor: Y — [score: W=n U=n S=n] <(opt. "from <a> counter: <b> #n")>
2. <idee> — [cost: X] — anchor: Y — [score: W=n U=n S=n]
3. <idee> — [cost: X] — anchor: Y — [score: W=n U=n S=n]
4. <idee> — [cost: X] — anchor: Y — [score: W=n U=n S=n]
5. <idee> — [cost: X] — anchor: Y — [score: W=n U=n S=n]
6. <idee> — [cost: X] — anchor: Y — [score: W=n U=n S=n]

## Next Experiment (one, only)

Idea number **<n from The Six>** is testable in the next hour with
tools you already have.

<one-paragraph description of the test: what you do, when, what you
observe, what counts as "this was worth trying">

## Self-Flag (for field-notes.md)

- [ ] kept (at least 1 of the 6 distilled ideas landed in wiki/inbox, ISSUES2FIX, or skills-backlog within 14 days)
- [ ] round2-was-degraded (track if degradation was triggered)
- [ ] retire-word? (a word produced only near-variations of earlier outputs)
- [ ] voice-off? (one of the two archetypes sounded wrong or like the other)
```

---

## Notes on the template

- **Divergence warning** is mandatory and duet-specific (mentions the
  two-voice crossing and the no-ranking rule). Keep verbatim.
- **Distiller is the main-model, never Codex.** That is the deliberate
  difference from chat-mode: duet is the cheap, dependency-free
  mid-tier (~4 calls). No `distiller_reason`, no Codex-fallback field.
- **Exactly 6 distilled ideas** — fewer than chat's 20, more curated
  than single's 10. The six are survivors of the crossing, never a
  ranked list and never a crowned winner (Hard Rule 1).
- **Cost-tags assigned at distillation** (as in chat round 3), honest
  per idea. There is no cost-mix corridor over a duet — too few final
  items — so the dial only weighted the operators in Step D2.
- **Counter/extend provenance** is preserved into The Six where an idea
  originated in round 2, so the user sees which crossing produced it.
- **Next Experiment** enforces the one-experiment-per-run rule
  (Hard Rule 5).
- **Round 2 degradation** is marked in BOTH frontmatter
  (`round2_status`) and a body disclaimer — frontmatter for tooling,
  body for the reader.
- **Self-Flag** carries duet-specific flags (round2-degraded) alongside
  the shared retire-word / voice-off / kept signals the harvest reads.
