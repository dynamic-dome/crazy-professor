# HOW-TO-USE — crazy-professor

Wegweiser für User und Agent. Stand: v0.14.0 (2026-06-12). Was das Plugin
*ist*, steht im Einzeiler: ein Divergenz-Generator — vier Archetypen
produzieren seltsame, aber verankerte Provokationen, niemals Ratschläge.

## Schnellstart

```text
/crazy <topic>                  # Single-Run: 10 Provokationen + 3 Konzepte + 1 Experiment (~30s)
/crazy <topic> --dial 80        # wilder (Dial 0-100, Default 60 = 6 wild / 4 machbar)
/crazy <topic> --chat           # alle 4 Stimmen, 3 Runden, 20 destillierte Ideen (~2-4 min)
/crazy --lab                    # statischer Review-Browser (paste-only, kein LLM)
/crazy --harvest                # pending Runs reviewen, kept-Experimente ins TODO-System
```

Ohne Topic nimmt der Single-Run das letzte konkrete Thema aus der
Konversation. `--chat` ohne Topic wird abgelehnt (bewusst — der Modus
kostet ~10 LLM-Calls). Trigger-Phrasen statt Slash-Command funktionieren
auch ("crazy professor", "provoke me", "verrueckter professor", ...).

## Der empfohlene Arbeitszyklus

1. **Generieren:** `/crazy <topic>` wenn ein Plan zu schnell konvergiert
   oder die erste Idee zu normal ist. Dial hochdrehen, wenn die Outputs
   zu zahm sind; runterdrehen, wenn nur Schwergewichte kommen.
2. **Lesen:** Output landet im **Zielprojekt** unter
   `.agent-memory/lab/crazy-professor/`. Die "Extracted Concepts" sind
   der Verwertungspfad — wilde Provokationen, zahm gemachte Mechanismen.
3. **Ernten:** Nach ein paar Runs `/crazy --harvest` — Verdikte vergeben
   (`kept`/`conditional`/`backlog`/`discarded`), kept-Experimente landen
   automatisch im DCO/Wiki-TODO oder in `experiments-backlog.md`.
   **Ohne Harvest bleibt die Museum-Clause blind** — der Skill misst
   seinen Wert ausschließlich an geernteten Verdikten.

## Komponenten

| Komponente | Pfad | Zweck |
|---|---|---|
| Slash-Command | `commands/crazy.md` | Flag-Parsing + Dispatch |
| Skill-Kern | `skills/crazy-professor/SKILL.md` | Einstieg, Modi-Tabelle, Archetypen |
| Operating-Instructions | `skills/crazy-professor/references/operating-instructions.md` | Steps 1-5 / C1-C6 / L1 / H1-H4 |
| Hard Rules | `skills/crazy-professor/references/hard-rules.md` | 8 Hard Rules, Museum-Clause, Harvest Rules, Review-Rubrik |
| Archetyp-Templates | `skills/crazy-professor/prompt-templates/` | Voice-Verträge (Pflicht-/verbotenes Vokabular) |
| Picker | `skills/crazy-professor/scripts/picker.py` | Archetyp × Wort × Operator + Dial, stdlib-only |
| Lab | `skills/crazy-professor/lab/index.html` | Browser-Triage, kein LLM |
| Wort-Pool | `skills/crazy-professor/resources/provocation-words.txt` | 176 aktive Provokationswörter |

## Wo welche Doku lebt

- `docs/PROJECT.md` — Steckbrief + aktueller Stand
- `docs/CAPABILITIES.md` — Fähigkeiten-Tabelle mit Status
- `docs/ARCHITECTURE.md` — Datenfluss, Persistenz, Sicherheit
- `docs/CHANGELOG.md` — Versions-Historie (neueste oben)
- `docs/VERSIONING.md` — Bump-Policy (8 Versions-Stellen!)
- `docs/chat-mode-flow.md` — kanonische Chat-Mode-Spec
- `docs/reviews/` — externe Analysen (Perplexity 2026-06-03, Fable Multi-Perspektiven 2026-06-12 inkl. Erweiterungs-Backlog E4-E10)
- `skills/crazy-professor/references/roadmap.md` — bewusst geparkte Features

## Install / Update

```bash
claude plugin marketplace add dynamic-dome/crazy-professor
claude plugin install crazy-professor --scope user
claude plugin update crazy-professor
```

Marketplace-Updates greifen erst nach Commit + Tag + `plugin update`
(Versions-Tag-Konvention siehe `docs/VERSIONING.md`).

## Troubleshooting

- **Picker schlägt fehl / kein Python:** Prosa-Fallback in
  `operating-instructions.md` Step 2 (mod-4-Mechanik von Hand).
- **Picker Exit 2:** Wort-Pool leer (alles retired) —
  `retired-words.txt` prüfen.
- **Codex-Distiller fällt aus (Chat-Mode):** automatischer
  Claude-Fallback, im Frontmatter als `distiller: claude
  (codex-fallback)` markiert. Kein Eingriff nötig.
- **Output wirkt wie Beratung:** Bug melden — Hard Rule 1 verbietet
  das; der Divergence-Banner muss in jedem Output stehen.
- **Skill „verschwunden":** Museum-Clause prüfen — nach 10 Runs ohne
  3 kept zieht er sich nach `.agent-memory/museum/` zurück. Gegenmittel:
  ernten (`--harvest`), nicht bauen.

## Grenzen

Lokal only, manuelles Triggern, ein Topic pro Run, kein MCP-Server.
Phase-4-8-Subsysteme (Telemetrie, Linter, Playground, Telegram) wurden
in v0.13.0 bewusst zurückgebaut — git-Historie ist das Archiv.
