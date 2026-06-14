---
description: Invoke the crazy-professor divergence generator on a topic. Default: 10 provocations + 3 extracted concepts. With --chat: all four voices and 20 distilled ideas. With --duet [a,b]: two voices cross-pollinate into 6 distilled ideas. --dial 0-100 tunes the wild/tame cost mix. --lab: open the static review browser. --harvest: triage pending runs and land kept experiments.
argument-hint: [topic] [--duet a,b] [--chat] [--dial 0-100] [--lab] [--harvest]
---

# Crazy Professor -- On-Demand

Activate the `crazy-professor` skill and run it against the following arguments:

**Arguments:** $ARGUMENTS

Topic resolution (single source of truth — the SKILL.md operating-instructions reference is the canonical version):

- If `$ARGUMENTS` contains `--lab`, open the static Ideation Lab at `skills/crazy-professor/lab/index.html` via `webbrowser.open()`. Standalone — no topic, no `--chat`.
- If `$ARGUMENTS` contains `--harvest`, dispatch to the Harvest path (Steps H1-H4): triage pending field-notes rows with user verdicts, land kept experiments. Standalone — combined with a topic or `--chat`, reject: `--harvest is standalone. Run /crazy --harvest on its own.`
- If `$ARGUMENTS` contains `--dial <n>`, parse n as integer 0-100 (default when absent: 60). The dial sets the wild/tame cost-mix target for single-run generation; with `--chat` it is echoed but does not constrain the rounds.
- If `$ARGUMENTS` contains `--chat` and no topic text outside the flags, **reject explicitly** and stop. Return: `Chat-mode requires an explicit topic. Run /crazy <topic> --chat or use single-run for ambient topics.`
- If `$ARGUMENTS` contains `--duet`, dispatch to Duet-Mode (Steps D1-D5): two archetypes, mutual cross-pollination, main-model distillation to 6 ideas. An optional pair follows the flag (`--duet jester,radagast`); without it the picker derives a max-tension diagonal. Topic mandatory (same rule as `--chat`). Mutually exclusive with `--chat`/`--lab`/`--harvest` — reject any combination with: `--duet cannot be combined with --chat/--lab/--harvest.`
- If `$ARGUMENTS` is empty (no flags, no topic), run single-run on the most recent concrete task, plan, or problem from the current conversation. If the conversation context is empty, meta, or too vague, ask one clarifying question and stop.
- If `$ARGUMENTS` contains a topic and no `--chat` and no `--duet`, dispatch to single-run mode: one active archetype, one provocation word, one PO operator, exactly 10 provocations, 3 extracted concepts, and one next experiment.
- If `$ARGUMENTS` contains a topic and `--chat`, dispatch to Chat-Mode: all four active archetypes, 3 rounds, final 20-idea distillation.

Follow the skill's full protocol exactly. All four archetypes are active: first-principles-jester, labyrinth-librarian, systems-alchemist, radagast-brown. No advice, no softening. Strange but anchored.
