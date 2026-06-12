# Output Template

Every invocation produces a Markdown file in this exact shape. The skill
fills in the angle-bracketed fields.

---

```markdown
---
skill: crazy-professor
version: 0.14.0
mode: single
timestamp: <ISO-8601 UTC, e.g. 2026-04-22T06:30:00Z>
topic: "<user input, one line, unmodified>"
archetype: <first-principles-jester | labyrinth-librarian | systems-alchemist | radagast-brown>
provocation_word: <lowercase phrase, 1-3 words, hyphens allowed>
po_operator: <reversal | exaggeration | escape | wishful-thinking>
dial: <0-100, from the picker JSON; default 60>
---

# Provocations: <topic>

**Archetype:** <archetype> | **Provocation Word:** <word> | **Operator:** <operator> | **Dial:** <dial> (target: <wild> wild / <tame> tame)

> DIVERGENCE WARNING: This output is provocation material, not advice.
> The ideas below are deliberately exaggerated, one-sided, or absurd.
> They exist to destabilize fixed thinking, not to be implemented as-is.
> Do not read this as recommendation. Do not cite this as analysis.
> Pick what moves you, discard the rest, and use the "Next Experiment"
> section to turn one nudge into something testable.

## 10 Provocations

1. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
2. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
3. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
4. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
5. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
6. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
7. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
8. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
9. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>
10. <provocation text> -- [cost: <low|medium|high|system-break>] -- anchor: <one-phrase link to user infrastructure>

<!-- Cost-mix line: only when the honest tag distribution deviates from
     the dial target by more than +/-1. See hard-rules "Cost-Mix Corridor". -->
*Cost-mix: <actual wild>/<actual tame> vs. target <wild>/<tame> -- <one-line diagnosis, e.g. "topic produced only heavyweights; probably framed too abstractly">*

## Extracted Concepts (movement material, not advice)

<!-- Exactly 3 concepts. Each names a transferable mechanism carried by
     the provocations above -- de Bono's "extract the concept" movement
     step. Noun phrases only, no imperative form. Paths are sketches of
     what the concept COULD look like at different cost levels; they
     open options, they do not recommend one. -->

1. **<concept name, noun phrase>** -- from provocations <n>, <m>. <one
   sentence naming the mechanism, no imperative form.>
   - path [low|medium]: <tame realization sketch, anchored>
   - path [medium|high]: <second realization sketch, anchored>
2. **<concept name>** -- from provocations <n>, <m>. <mechanism sentence.>
   - path [...]: <...>
   - path [...]: <...>
3. **<concept name>** -- from provocations <n>, <m>. <mechanism sentence.>
   - path [...]: <...>
   - path [...]: <...>

## Next Experiment (one, only)

<Concept <K>, path [<level>]> OR <Provocation number <N>> is testable
in the next hour with tools you already have. Here is the concrete test:

<one-paragraph description of the test: what you do, when, what you
observe, what counts as "this was worth trying">

## Self-Flag (for field-notes.md)

- [ ] kept (landed in wiki/inbox, ISSUES2FIX, or skills-backlog within 14 days)
- [ ] retire-word? (word produced only near-variations of earlier outputs)
- [ ] voice-off? (archetype sounded wrong or like a different archetype)
```

---

## Notes on the template

- The divergence warning is **not optional.** It is the safety framing
  that lets the skill avoid the accuracy-degradation risk
  documented for persona-prompting in knowledge-heavy tasks.
- Adoption cost tags are a diagnostic label, not a recommendation:
  `low` (<= 30 min, no new infra), `medium` (1-2h, minor refactor),
  `high` (multi-day, meaningful change to pipeline/process), and
  `system-break` (requires policy/architecture break or is intentionally
  "impossible" without redesign).
- **Dial / cost-mix (since v0.14.0):** "wild" = `high`/`system-break`,
  "tame" = `low`/`medium`. The dial target steers the MIX during
  generation; it never bends an individual tag. Tags stay honest per
  provocation. If the honest distribution deviates from the target by
  more than +/-1, the cost-mix diagnostic line below the provocations
  is mandatory; otherwise omit it.
- **Extracted Concepts (since v0.14.0):** exactly 3, each citing at
  least one source provocation by number. Concepts are de Bono's
  movement step between provocation and experiment — they name the
  transferable mechanism so a wild provocation can have tame children.
  Noun phrases only; any imperative phrasing ("do X", "introduce Y")
  is advisor-drift and must be rewritten. Paths carry their own honest
  cost level and an anchor. The divergence banner covers this section
  too.
- The "Next Experiment" section enforces the one-experiment-per-run
  rule. The pick comes from a concept path (preferred, because paths
  are already sized) or directly from a provocation. If the skill
  produces 10 provocations and no single experiment pick, the run is
  incomplete.
- The Self-Flag checkboxes are the minimum signal the user needs to
  feed back into field-notes.md for the field-test rule and the
  museum-clause gate to work. If the user never ticks any box, the
  skill has no evidence base for retirement and should default to
  the museum after 10 runs.
- Provocation-word format: lowercase phrase of 1 to 3 tokens, separated
  by spaces or hyphens. Examples: `museum`, `paradox tax`, `gravity well`,
  `false-bottom`. Decision 2026-04-27 (Phase 1, point 1.5): the pool
  contains both single words and 2-3-word phrases because phrases like
  `shadow pricing`, `ritual debt`, `paradox tax` are stronger provocation
  anchors than any single-word reduction. The rule is a prose contract
  since v0.13.0 (the Phase-3 word-pool linter was rolled back).
