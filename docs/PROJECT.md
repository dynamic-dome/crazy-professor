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

v0.14.0 released 2026-06-12. Single-Run (jetzt mit Wildness-Dial `--dial 0-100` und Pflicht-Sektion "Extracted Concepts"), Chat-Mode, statisches Lab-HTML und neuer Harvest-Modus (`--harvest`, Triage pending Runs → Verdikte → kept-Experimente ins TODO-System) aktiv. Basis bleibt der v0.13.0-Lean-Kern: ein Python-Helper (`picker.py`), 4 Archetype-Templates, Chat-Mode-Distillation via Codex-Subagent; Phase-4-8-Subsysteme bleiben zurückgebaut. Anlass für v0.14.0: Multi-Perspektiven-Analyse 2026-06-12 (`docs/reviews/`) — kept-Loop ohne Wiedervorlage tot, 60/40-Ziel nicht steuerbar, Movement-Schritt zwischen Provokation und Experiment fehlte. Versions-Policy in `docs/VERSIONING.md`.

## Kernfaehigkeiten

Siehe [CAPABILITIES.md](CAPABILITIES.md) fuer die vollstaendige Liste.

Kurzfassung:
- Single-Run: 1 Archetype, 10 Provokationen, 1 Next-Experiment, ~30s
- Chat-Mode (`--chat`): alle 4 Archetypen, 3 Runden, 20 destillierte Ideen, 2-4 min
- Lab (`--lab`): statisches HTML zum Reviewen gepasteter Outputs, kein LLM-Call
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
- [ ] E1-Bewährung: erste 2-3 Harvest-Läufe zeigen, ob der kept-Loop jetzt Daten produziert (Voraussetzung für alles Weitere, siehe Analyse E4-E10)

## Abhaengigkeiten

- Claude Code CLI (Plugin-Host)
- Codex-Subagent (`codex:codex-rescue`) fuer Chat-Mode Round-3-Distillation, Claude-Fallback verfuegbar
- Eigene Repo-interne Resources (`provocation-words.txt`, `po-operators.md`, `prompt-templates/`)

## Beziehungen zu anderen Projekten

- **Nutzt:** Codex-Plugin (Round-3-Destillator), agentic-os (Field-Notes liegen in `.agent-memory/lab/`)
- **Wird genutzt von:** plan-merger Skill nutzt crazy-professor als Beispiel fuer Auto-Mode-Tests
