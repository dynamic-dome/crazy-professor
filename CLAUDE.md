# CLAUDE.md — crazy-professor

Pflichtlektüre zuerst: `HOW-TO-USE.md` (Wegweiser), dann je nach Aufgabe
`docs/PROJECT.md` und `docs/CHANGELOG.md`.

## Projekt-Konventionen für Agenten

1. **Versions-Bump nur per `docs/VERSIONING.md`.** MINOR bei jedem
   user-sichtbaren Verhalten, PATCH bei Fixes/Doku. Die Version lebt an
   **8 Stellen** (plugin.json ist Source of Truth; SKILL.md,
   output-template, chat-output-template, chat-mode-flow ×2,
   chat-curator, chat-round-1/2-wrapper spiegeln). Nie nur eine Stelle
   bumpen. Commit-Message: `crazy-professor | vX.Y.Z: ...` + Git-Tag.
2. **Pfad-Konvention:** Inter-File-Referenzen in SKILL.md/references/
   commands schreiben sich als `<repo-root>/...` — beibehalten.
3. **field-notes.md ist append-only Audit-Trail.** Automation editiert
   keine Review-Spalten — einzige Ausnahme: der Harvest-Pfad als
   Protokollant expliziter User-Verdikte (Schema:
   `skills/crazy-professor/resources/field-notes-schema.md`).
4. **Outputs gehören ins Zielprojekt**, nicht in dieses Repo:
   `<target-project>/.agent-memory/lab/crazy-professor/`. Die
   field-notes in DIESEM Repo entstehen nur, wenn der Skill auf das
   Plugin-Repo selbst angewandt wird.
5. **Hard Rules sind nicht verhandelbar** (`references/hard-rules.md`):
   nie Beratung, Banner immer, Anker-Pflicht, genau 1 Experiment,
   keine Archetyp-Kontamination, ehrliche Cost-Tags (Dial steuert die
   Mischung, nie das einzelne Tag).
6. **Vor neuen Features:** Lektion v0.13.0 respektieren — keine
   Infrastruktur vor dem Datenstrom. Erweiterungs-Backlog E4-E10 in
   `docs/reviews/2026-06-12-fable-multi-perspektiven-analyse.md`
   setzt funktionierende Harvest-Daten voraus.
7. **Doku-Update-Trigger:** neue Capability → CAPABILITIES.md;
   Architektur-Änderung → ARCHITECTURE.md; jede Session mit Substanz →
   CHANGELOG.md; neue Komponente → HOW-TO-USE.md.

Vorrang: explizite User-Anweisung > `~/AI/SESSION-WORKFLOW.md` > diese
Datei > globale Defaults.
