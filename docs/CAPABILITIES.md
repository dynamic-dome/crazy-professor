# Faehigkeiten — crazy-professor

## Tools & Integrationen

| Tool / Feature | Status | Seit | Beschreibung |
|----------------|--------|------|--------------|
| Single-Run-Mode | aktiv | 2026-04-22 | 1 Archetype, 10 Provokationen + 3 Extracted Concepts + 1 Next-Experiment, ~30s |
| Chat-Mode (`--chat`) | aktiv | 2026-04-23 | 4 Archetypen, 3 Runden, 20 destillierte Ideen, ~10 LLM-Calls |
| Duett-Modus (`--duet [a,b]`) | aktiv | 2026-06-14 | 2 Archetypen, je 5 Provokationen + gegenseitige Cross-Pollination, Main-Model-Destillation auf 6 Ideen + 1 Experiment, ~4 Calls/~1 min (kein Codex). Ohne Paar: Max-Spannungs-Diagonale. |
| Lab (`--lab`) | aktiv | 2026-04-30 | Standalone Browser für Output-Triage, paste-only, kein LLM-Call |
| Wildness-Dial (`--dial 0-100`) | aktiv | 2026-06-12 | Soll-Mischung wild/tame über die Cost-Tags (Default 60 → 6 wild / 4 tame) + dial-gewichteter Operator-Pick. Hard Rule 7: Tags bleiben ehrlich, Abweichung >±1 wird diagnostiziert. |
| Extracted Concepts | aktiv | 2026-06-12 | de Bonos Movement-Schritt: 3 Mechanismus-Konzepte pro Single-Run, je 2-3 verankerte Pfade. Hard Rule 8: Substantiv-Phrasen, keine Imperativform, kein Ranking. |
| Harvest-Modus (`--harvest`) | aktiv | 2026-06-12 | Triage-Dialog über pending field-notes-Zeilen, Verdikte vom User, kept-Experimente landen im TODO-System (DCO/Wiki) oder `experiments-backlog.md`. Schliesst den Museum-Clause-/Field-Test-Loop. |
| Variation-Guard | aktiv | 2026-04-22 | Anti-Streak-Logik in `picker.py` (Archetype-Streak ≥3, Wort-Window 10) |
| Field-Notes-Log | aktiv | 2026-04-22 | Markdown-Tabelle in `.agent-memory/lab/crazy-professor/field-notes.md` |
| Museum-Clause | aktiv | 2026-04-22 | Skill zieht sich nach 10 Runs ohne Keeper selbst zurueck; Zaehlerstand-Report im Harvest seit v0.14.0 |
| Codex-Round-3-Distiller | aktiv | 2026-04-23 | `codex:codex-rescue` als Round-3-Juror in Chat-Mode |
| Claude-Distiller-Fallback | aktiv | 2026-04-23 | Falls Codex nicht erreichbar |
| Picker-Skript | aktiv | 2026-04-27 | `picker.py` (stdlib-only): mod-4 archetype, dial-gewichteter operator, microsecond-seeded word, JSON-Output mit `dial` + `cost_mix_target`. Force-Flags + wishful-share v0.13.0 entfernt. |
| Output-Template + Field-Notes-Schema | aktiv | 2026-04-27 | Marker-Pattern + Tabellen-Spec, Format ist Soll-Vertrag im Prompt (kein Linter mehr) |

Status-Werte: `aktiv`, `experimentell`, `geplant`, `out of scope`, `deprecated`, `entfernt`

## Profile / Modi

- **Single-Run** (default): 1 Archetype-Pick via mod-4 + Variation-Guard, 10 Provokationen, 3 Extracted Concepts, 1 Next-Experiment. Optional `--dial 0-100` fuer die wild/tame-Mischung.
- **Chat-Mode** (`--chat`): alle 4 Archetypen parallel in Runde 1 (5 Provokationen je), Cross-Pollination in Runde 2 (counter/extend), Codex-Distillation in Runde 3 (5 Final-Ideen je Archetype = 20 total). `--dial` wird durchgereicht, constraint die Runden aber nicht.
- **Chat-Mode Dry-Run** (`--chat --dry-run-round1`): nur Runde 1, kein Round-2/3, fuer internes Testen.
- **Duett-Modus** (`--duet [a,b]`): genau 2 Archetypen, je 5 Provokationen (Runde 1), gegenseitige counter/extend-Cross-Pollination (Runde 2, jeder sieht nur die 5 des anderen), Main-Model-Destillation auf 6 Ideen + 1 Experiment. ~4 Calls, kein Codex. Ohne `--pair` leitet der Picker eine Max-Spannungs-Diagonale ab (jester×radagast / librarian×alchemist), seed-rotiert. `--dial` gewichtet nur die Operatoren (kein Cost-Mix-Korridor bei 6 Items).
- **Lab** (`--lab`): standalone Browser, paste-only, kein LLM-Call.
- **Harvest** (`--harvest`): standalone Triage-Dialog, keine Generierung, kein Picker-Call. Pending Runs reviewen, Verdikte protokollieren, kept-Experimente materialisieren.

## MCP-Server

Nicht zutreffend — crazy-professor exponiert keinen MCP-Server. Es nutzt das Codex-Plugin als Subagent fuer Round-3-Distillation, kommuniziert sonst nur ueber Datei-Output.

## Einschraenkungen

- **Lokal nur**: kein Cloud-Sync, kein Multi-Maschinen-State (field-notes liegt pro Projekt)
- **Manuelles Triggering**: kein Auto-Schedule, kein Webhook, kein Bot
- **Single-Topic pro Run**: Chat-Mode kann keinen Multi-Topic-Batch
- **Keine Modell-Mix-Optionen**: Claude fuer Runde 1+2, Codex fuer Runde 3 ist fix
- **Format-Vertrag ist Soll**: kein Pre-Write-Validator mehr (v0.13.0 zurückgebaut). Format-Drift wird beim Lesen sichtbar.
- **Picker-Skript ist optional**: Plugin laeuft auch ohne Python (Fallback-Prosa-Mechanik in operating-instructions Step 2 / picker.py docstring)

## Entfernte Funktionen (v0.13.0, 2026-05-02)

Phase-4-8-Funktionalität entfernt — siehe `docs/CHANGELOG.md` v0.13.0 Eintrag. Wenn etwas davon zurückkommen soll: git-Historie als Archiv.
