# Task: Deep Analysis & Expansion Report — "crazy-professor" Claude Code Plugin

You have read access to the Git repository for a Claude Code plugin called
**crazy-professor**. Your job has four phases: (1) fully understand it, (2) assess
and judge it, (3) map its relationships and visualize them, (4) sketch ambitious
expansion possibilities. Deliver everything as one Markdown report (in German — see
"Output" below).

## What this plugin is (orientation — verify against the repo, do not take my word)

crazy-professor is a *divergence generator*, NOT an advisor or coach. On any topic it
produces 10 deliberately strange-but-anchored "provocations" using a random
combination of: one of four ARCHETYPES (voices), one provocation WORD, and one of
de Bono's PO (Provocation Operation) OPERATORS. Its explicit design constraint is that
output is *never advice* — only hypotheses / "what if" nudges away from the obvious.
The current version is v0.13.0, which deliberately ROLLED BACK a large amount of
tooling (Phases 4–8: telemetry, patch-suggester, run-planner, linters, eval-suite,
telegram scaffold, browser playground) because 18 runs produced zero usage of those
subsystems. Read the v0.13.0 CHANGELOG entry and the rollback decision carefully — the
"less is more" rollback philosophy is central to this project's identity.

## Phase 1 — Read & fully illuminate the repo

Read at minimum (paths relative to repo root):

- `README.md`, `docs/PROJECT.md`, `docs/ARCHITECTURE.md`, `docs/CAPABILITIES.md`,
  `docs/CHANGELOG.md` (esp. the v0.13.0 entry), `docs/VERSIONING.md`,
  `docs/chat-mode-flow.md`
- `commands/crazy.md` (the `/crazy` slash command + argument dispatch)
- `skills/crazy-professor/SKILL.md` (the core logic / frontmatter / trigger phrases)
- `skills/crazy-professor/references/operating-instructions.md` (Steps 1–5 single-run,
  C1–C6 chat-mode, L1 lab)
- `skills/crazy-professor/references/hard-rules.md` (output-is-never-advice,
  Museum-Clause, Field-Test-Rule, Review-Rubric — the constitutional rules)
- `skills/crazy-professor/references/roadmap.md` (deferred / out-of-scope design intent)
- All four archetype prompt-templates in `skills/crazy-professor/prompt-templates/`:
  `first-principles-jester.md`, `labyrinth-librarian.md`, `systems-alchemist.md`,
  `radagast-brown.md` (note radagast's "Activation Amendments" — the binding voice rules)
- The chat-mode wrappers: `chat-round-1-wrapper.md`, `chat-round-2-wrapper.md`,
  `chat-curator.md`
- `skills/crazy-professor/resources/`: `po-operators.md`, `provocation-words.txt`,
  `retired-words.txt`, `output-template.md`, `chat-output-template.md`,
  `field-notes-schema.md`
- `skills/crazy-professor/scripts/picker.py` (the only helper — deterministic
  stochastic picker with a variation-guard; understand the mod-4 archetype/operator
  selection, microsecond-seeded word pick, and anti-streak re-roll logic)
- `skills/crazy-professor/lab/index.html` (static, browser-only review surface)

Produce a precise mental model of: the three run modes (Single-Run, Chat-Mode `--chat`,
Lab `--lab`), the data flow, the persistence model (field-notes.md is the ONLY
machine-readable run log), the four archetype voices and how they are kept from
contaminating each other, the PO operators, and the self-governance mechanisms
(Museum-Clause, Chat-Mode Museum-Clause, Field-Test-Rule).

## Phase 2 — Assess & judge (the heart of the report)

Give a substantive, opinionated evaluation. Cover:

- **Coherence of the concept** — does "divergence generator, never an advisor" hold up
  consistently across SKILL.md, the templates, the hard-rules, and the picker?
- **Quality of the voice design** — are the four archetypes genuinely distinct, or do
  they bleed into each other? Judge the verbotenes-Vokabular bans and radagast's
  Activation Amendments specifically.
- **Soundness of the self-governance** — are the Museum-Clause and Field-Test-Rule
  real mechanisms or decorative? Is the v0.13.0 rollback a sign of discipline or of a
  project that over-built then panicked?
- **Technical assessment** of picker.py — correctness of the variation-guard, the
  determinism choices, edge cases (empty pool, exhausted pool, chat intra-dedup).
- **Gaps, risks, contradictions** — anything internally inconsistent, any dead
  references, any place where the prose contract (no automated linter since v0.13.0)
  is likely to drift.
- **Connections / "Zusammenhang erkennen"** — explicitly articulate how the pieces
  relate: command → skill → operating-instructions → templates → picker → field-notes
  → museum-clause feedback loop. Make the system's *logic* legible.

## Phase 3 — Visualize

Embed at least these diagrams as **Mermaid** code blocks inside the Markdown report
(GitHub-flavored Mermaid syntax, so they render in any Mermaid-aware viewer):

1. A component/data-flow diagram of the three run modes (command dispatch → picker →
   archetype template → generation → output file → field-notes → museum feedback loop).
2. A diagram of the picker's decision/variation-guard logic.
3. A relationship map ("Zusammenhang") showing how the archetypes, PO operators, the
   word pool, the governance rules, and the persistence layer interlock.

Keep diagrams readable; prefer 2–3 clear diagrams over one giant one.

## Phase 4 — Expansion possibilities (scope-free, be ambitious)

Sketch **as many strong/wild expansion ideas as you can** — do NOT constrain yourself
to the current lean v0.13.0 scope, and do NOT avoid ideas just because they resemble
the rolled-back Phases 4–8. I will filter for fit myself. For each idea give: a name, a
one-paragraph description, what it would unlock, and a rough effort/complexity tag. Aim
for genuine range — new archetypes, new operators, new modes, new integrations
(Telegram/mobile, multi-topic batch, cross-plugin orchestration, devil's-advocate
pressure-testing, model-mix experiments), new output surfaces, ways to close the
adoption-measurement gap that triggered the rollback, etc. Bonus: note which ideas
would *contradict* the project's stated philosophy, so the contradiction is visible.

## External comparison (use your web research)

Beyond the repo, research the public landscape and position crazy-professor against it:
other Claude Code / LLM ideation & divergence skills/plugins, Edward de Bono lateral-
thinking / PO tooling, "creativity prompting" patterns, persona/archetype-prompting
research (including the known finding that persona prompting can reduce factual
accuracy on knowledge-heavy tasks — the repo cites ~30pp). Cite your sources. Say what
crazy-professor does that comparable tools don't, and vice versa.

## Output

- One **Markdown report**, written **in German** (technical terms / code identifiers
  stay in their original English form). Keep German orthography fully correct
  (Umlaute/ß).
- Structure: Executive Summary → Phase-1 System-Verständnis → Phase-2 Bewertung →
  Phase-3 Diagramme (Mermaid) → Phase-4 Erweiterungs-Ideen → Externer Vergleich (mit
  Quellen) → Fazit.
- Be concrete and cite file paths (`skills/crazy-professor/...`) when you make a claim
  about the code, so every judgment is traceable to the repo.
- Save/return the report so it can be dropped into the repo (suggested path:
  `docs/reviews/2026-06-03-perplexity-analysis.md`).
