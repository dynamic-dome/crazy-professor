---
project: crazy-professor
status: active
started: 2026-04
stack: [Markdown, Claude-Code-Plugin, Codex-Subagent]
repo: C:\Users\domes\Desktop\Claude-Plugins-Skills\crazy-professor
wiki_entity: "[[crazy-professor]]"
---
# crazy-professor

## Einzeiler

Divergence-Generator als Claude-Code-Plugin: vier Archetypen produzieren strange-aber-anchored Provokationen, niemals Ratschlaege.

## Aktueller Stand

v0.15.0 released 2026-06-14. Single-Run (mit Wildness-Dial `--dial 0-100` und Pflicht-Sektion "Extracted Concepts"), Chat-Mode, neuer **Duett-Modus** (`--duet [a,b]`: zwei Archetypen kreuzen sich in ~4 Calls ohne Codex → 6 destillierte Ideen, Mittel-Tier zwischen Single und Chat), statisches Lab-HTML und Harvest-Modus (`--harvest`) aktiv. Basis bleibt der v0.13.0-Lean-Kern: ein Python-Helper (`picker.py`), 4 Archetype-Templates, Chat-Mode-Distillation via Codex-Subagent; Phase-4-8-Subsysteme bleiben zurückgebaut. v0.15.0 hebt das D4-Gate auf: der erste echte Harvest (2026-06-14, 3 Runs / 3 kept) lieferte reale kept-Daten, womit das E4-E10-Backlog aus der Multi-Perspektiven-Analyse (`docs/reviews/`) freigeschaltet ist; E5 (Duett) ist der erste daraus gebaute Punkt. Versions-Policy in `docs/VERSIONING.md`.

## Kernfaehigkeiten

Siehe [CAPABILITIES.md](CAPABILITIES.md) fuer die vollstaendige Liste.

Kurzfassung:
- Single-Run: 1 Archetype, 10 Provokationen + 3 Extracted Concepts, 1 Next-Experiment, ~30s; `--dial 0-100` steuert die wild/tame-Mischung
- Chat-Mode (`--chat`): alle 4 Archetypen, 3 Runden, 20 destillierte Ideen, 2-4 min
- Duett-Modus (`--duet [a,b]`): 2 Archetypen, gegenseitige Cross-Pollination, 6 destillierte Ideen, ~4 Calls/~1 min (kein Codex)
- Lab (`--lab`): statisches HTML zum Reviewen gepasteter Outputs, kein LLM-Call
- Harvest (`--harvest`): Triage pending Runs, Verdikte in field-notes, kept-Experimente ins TODO-System
- Variation-Guard: Anti-Streak-Logik gegen Archetype-/Wort-Wiederholungen
- Field-Notes-Log: jeder Run wird in `.agent-memory/lab/crazy-professor/field-notes.md` protokolliert
- Museum-Clause: Skill zieht sich nach 10 Runs ohne Keeper selbst zurueck

## Offene Baustellen

- [x] Phase 1: Vertragsbereinigung & Quick-Wins (✅ v0.6.0)
- [x] Phase 2: Picker als Skript + field-notes-Schema (✅ v0.7.0)
- [x] Phase 3: Linter-Trio + Eval-Suite (✅ v0.8.0 → in v0.13.0 zurückgebaut)
- [x] Phase 4: Telemetrie + Patch-Suggestion-Loop (✅ v0.9.0 → in v0.13.0 zurückgebaut)
- [x] Phase 5: Run-Planner (✅ v0.10.0 → in v0.13.0 zurückgebaut)
- [x] Phase 6: Cross-Pollination + Compact-Mode + 4. PO-Operator (✅ v0.11.0 → teilweise in v0.13.0 zurückgebaut, 4. Operator bleibt)
- [x] Phase 7: Single-File-HTML-Playground (✅ v0.12.0 → in v0.13.0 zurückgebaut)
- [x] v0.13.0 (2026-05-02): Phasen 4-8 zurückgebaut, Skill auf Kern reduziert
- [x] v0.14.0 (2026-06-12): E1 Harvest-Modus + E2 Wildness-Dial + E3 Extracted Concepts (aus Multi-Perspektiven-Analyse)
- [x] E1-Bewährung: erster echter Harvest 2026-06-14 (3 Runs / 3 kept, 2 Experimente → DCO #7925/#7926) — kept-Loop produziert Daten, D4-Gate aufgehoben
- [x] v0.15.0 (2026-06-14): E5 Duett-Modus (erster Bau aus dem E4-E10-Backlog)
- [ ] E4/E6-E10 aus dem Backlog (`docs/reviews/2026-06-12-...`) — nach Bedarf; E10/E7 weiter datengated bis ~10 Runs

## Abhaengigkeiten

- Claude Code CLI (Plugin-Host)
- Codex-Subagent (`codex:codex-rescue`) fuer Chat-Mode Round-3-Distillation, Claude-Fallback verfuegbar
- Eigene Repo-interne Resources (`provocation-words.txt`, `po-operators.md`, `prompt-templates/`)

## Beziehungen zu anderen Projekten

- **Nutzt:** Codex-Plugin (Round-3-Destillator), agentic-os (Field-Notes liegen in `.agent-memory/lab/`)
- **Wird genutzt von:** plan-merger Skill nutzt crazy-professor als Beispiel fuer Auto-Mode-Tests
