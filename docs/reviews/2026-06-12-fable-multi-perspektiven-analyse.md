# crazy-professor — Multi-Perspektiven-Analyse (Anwender / Agents / Ideenfindung)

**Analyse-Datum:** 2026-06-12
**Analysiertes Release:** v0.13.0
**Analyst:** Claude Fable 5 (Claude Code)
**Methodik:** Vollständige Lektüre des Repos (SKILL.md, Operating-Instructions, Hard-Rules, alle vier Archetyp-Templates, `picker.py`, Output-/Chat-Templates, Changelog inkl. v0.13.0-Rückbau, bestehende Perplexity-Analyse) plus Auswertung des realen Outputs `2026-06-12-2129-dual-bridge-erweiterung.md`. Auftrag: Bewertung des aktuellen Vorgehens im Hinblick auf Kreativität und Durchführbarkeit (Ziel: ~60/40 verrückt/machbar), Verbesserungsvorschläge, zehn ausgearbeitete Erweiterungen.

---

## 1. Was der Skill ist — Kurzverständnis

crazy-professor ist ein **Divergenz-Generator** nach de Bonos Provocation Operation (PO). Ein Run kombiniert drei Zufallselemente — **Archetyp × Provokationswort × PO-Operator** — und erzeugt daraus 10 Provokationen plus **genau ein** testbares Next-Experiment. Die vier Stimmen (first-principles-jester, labyrinth-librarian, systems-alchemist, radagast-brown) sind nicht bloß Tonalitäten, sondern über Pflicht-Vokabular, verbotenes Vokabular und (bei Radagast) bindende Activation Amendments mechanisch voneinander abgegrenzt. Drei Modi: Single-Run (1 LLM-Call, ~30s), Chat-Mode (4 Archetypen × 3 Runden, Codex-Distillation auf 20 Ideen) und das statische Lab (Browser, kein LLM).

Die Architektur hat einen geschlossenen Regelkreis über genau eine Datei: jeder Run schreibt in `field-notes.md`, und Museum-Clause (Skill stirbt nach 10 Runs ohne 3 „kept") sowie Field-Test-Rule (Wort wird nach 3 Flags pensioniert) lesen aus derselben Datei. v0.13.0 hat ~3000 Zeilen vorzeitig gebauter Infrastruktur (Telemetrie, Linter, Eval-Suite, Playground) zurückgebaut — mit der bemerkenswert ehrlichen Begründung, dass Phase 4–8 gebaut wurde, bevor Phase 1–3 je Daten lieferte.

---

## 2. Perspektive Anwender

**Was funktioniert:** Die Einstiegshürde ist minimal (`/crazy <topic>`, 30 Sekunden), und das Output-Format ist ungewöhnlich diszipliniert. Der reale dual-bridge-Output zeigt das Niveau: Provokation Nr. 8 (Flussanzapfung — „erobere nicht die Mündung, sondern die Quellen, und der manuelle Weg vertrocknet, ohne dass ihn je jemand abschaltet") ist genau die Sorte Idee, die der User selbst nicht erreicht hätte, aber sofort versteht. Drei Mechanismen tragen das: die **Anker-Pflicht** (jede Provokation muss eine real existierende Struktur nennen — `bridge_transport.py`, `SHAREPOINT_MANIFEST.md`), die **Cost-Tags** (low bis system-break) als ehrliche Machbarkeits-Etiketten, und das **Eine-Experiment-Prinzip** als Anti-Überforderungs-Ventil. Der Divergence-Warning-Banner verhindert die häufigste Fehlnutzung (Provokation als Empfehlung lesen).

**Wo es für den Anwender hakt:**

1. **Der Ernte-Loop ist tot.** Die gesamte Governance hängt an den Self-Flag-Checkboxen (`kept` / `retire-word?` / `voice-off?`), die der User binnen 14 Tagen setzen soll. Die field-notes in diesem Repo zeigen den Ist-Zustand: alle Spalten `pending`. Nach 18 Runs (Stand Rückbau) hat der Mensch fast nie kuratiert. Damit dreht der eleganteste Teil der Architektur — der selbstregulierende Loop — im Leerlauf, und die Museum-Clause kann ihr Urteil nie datenbasiert fällen. **Das ist die größte einzelne Schwäche des Plugins, und sie liegt nicht im Code, sondern im fehlenden Wiedervorlage-Mechanismus.**
2. **Outputs verschwinden im Dunkeln.** Die Dateien landen in `.agent-memory/lab/crazy-professor/` — ein Ort, den niemand spontan öffnet. Es gibt keinen Pfad zurück: kein „zeig mir die offenen Experimente", kein Anschluss an das DCO-/Wiki-TODO-System des Users.
3. **Das Lab erzwingt einen Medienbruch.** Paste-only heißt: Datei suchen, öffnen, kopieren, Browser, einfügen. Für ein Triage-Tool ist das eine Hürde, die genau die Kuration verhindert, von der das System lebt.
4. **Keine Dosierung.** 10 Provokationen sind fix; der Sprung von Single (1 Call) zu Chat (~10 Calls, 2–4 min) ist groß, dazwischen gibt es nichts.

---

## 3. Perspektive Agents

**Was funktioniert:** Aus Agentensicht ist das Plugin vorbildlich spezifiziert. `picker.py` liefert sauberes JSON, ist stdlib-only, deterministisch, hat einen Prosa-Fallback falls Python fehlt, und behandelt alle Edge-Cases (leerer Pool → Exit 2, fehlende field-notes → Auto-Init). Die `<repo-root>`-Pfadkonvention macht jede Referenz aus jedem File auflösbar. Degradationspfade sind explizit: Codex-Distiller-Ausfall → Claude-Fallback mit `distiller_reason`, Runde-2-Ausfall → `degraded` statt Abort, ≥2 kaputte Archetypen in Runde 1 → kontrollierter Fallback auf Single-Run. Der Codex-Curator-Prompt ist selbst-enthalten und hat einen harten Direct-Markdown-Return-Contract inklusive Retry-Regel. Das ist Subagent-Orchestrierung auf einem Niveau, das man selten sieht.

**Wo es für Agents hakt:**

1. **Soll-Verträge ohne Durchsetzung.** Seit dem Rückbau leben alle Voice-Verträge (verbotenes Vokabular, Pflicht-Vokabeln-im-ersten-Satz, `[opt-care]`-Marker, Anti-Ordner-Wildwuchs) als reine Prosa. Der ausführende Agent muss vier Templates plus Amendments im Kontext halten und sich selbst prüfen („scan the 10 first sentences, count Pflicht-Vokabeln") — LLM-Selbstdisziplin ohne Verifikation. Das ist für v0.13.0 die bewusste Lean-Entscheidung, aber es ist die Stelle, wo dokumentierte und durchgesetzte Regel auseinanderfallen.
2. **Die Governance verlangt sitzungsübergreifende Buchhaltung ohne Trigger.** „Nach der 10. Invocation prüfe die Museum-Clause" — kein Hook, kein Zähler, kein Signal. Ein Agent in Session 23 weiß nicht, dass Run 10 gerade passiert ist. Die Regel existiert, aber nichts feuert sie.
3. **Anker werden nicht verifiziert.** „anchor-or-it-doesnt-count" ist die wichtigste Hard Rule, aber kein Schritt prüft, ob `risk_policy.py` oder `lane-A-to-B/_processed` tatsächlich existieren. Ein halluzinierter Anker sieht identisch aus wie ein echter.
4. **Zeitbasierter Determinismus hat eine Eigenheit:** zwei Runs in derselben Minute ziehen denselben Archetyp; der Variation-Guard greift erst ab 3er-Streak. Praktisch selten relevant, aber für Tests/Demos fehlt ein `--seed`.

---

## 4. Perspektive Ideenfindung — Kreativität × Machbarkeit

**Die Kreativitätsmechanik ist werktreu und funktioniert.** Die Kombination aus erzwungenem Fremdreiz (Provokationswort), erzwungener Denkbewegung (PO-Operator) und erzwungener Stimme (Archetyp) erzeugt genau die gewünschte „Betrachtung aus verrückten Blickwinkeln" — und die Anker-Pflicht verhindert exakt das benannte Risiko („nicht nur sinnlos"). De Bonos Diktum „Provocation without movement is useless" ist als nicht verhandelbare Regel kodiert. Der dual-bridge-Output beweist es empirisch: zehn Provokationen, jede mit einem echten Mechanismus-Transfer (Brutparasitismus → Tasks in fremde Queues legen; Fassadismus → byte-identischer Vertrag bei freiem Transport-Umbau), jede an reale Dateien gebunden.

**Aber: Das 60/40-Ziel (verrückt/machbar) existiert nirgends im System.** Das ist der zentrale Befund dieser Perspektive. Die Cost-Tags sind „ehrlich pro Provokation, keine erzwungene Verteilung" (Operating-Instructions Step 4). Der reale Run verteilte sich auf 3× system-break, 3× high, 3× medium, 1× low — also eher 60% *schwer* als 60% *verrückt-aber-greifbar*. Niemand misst, niemand steuert. De Bono selbst fordert, dass ≥40% der Provokationen unbrauchbar sein *sollen* (sonst zu zahm) — das verträgt sich mit dem 60/40-Ziel, aber der Skill hat keinen Regler, keinen Soll-Korridor, keine Diagnose. Wenn ein Run zufällig 10× system-break liefert, ist das formal regelkonform und für den Zweck („den Stack nach vorne bringen") wertlos.

**Die zweite Lücke: der fehlende Mittelschritt zwischen Provokation und Experiment.** Der Skill springt von „10 wilde Provokationen" direkt zu „1 Experiment in der nächsten Stunde". De Bonos Methodik hat dazwischen die *Movement*-Techniken (extract the concept, focus on the difference). Im Output fehlt diese Ebene: Provokation Nr. 2 (Kuckucks-Ei) trägt das Konzept „Ununterscheidbarkeit als Integrationsstrategie" — aber das Konzept wird nie extrahiert, also verpufft die Idee, wenn die wörtliche Provokation zu teuer ist. 9 von 10 Provokationen sterben aktuell ohne Verwertungsschritt. Genau hier liegt die größte Hebelwirkung für „sinnvoll mehr oder weniger".

**Drittens: der Reiz-Pool altert einseitig.** 176 Wörter, durchweg englisch, thematisch auffällig homogen (Heist/Theater/Infrastruktur: counterfeit, decoy, smuggling, backstage, dead drop, feint…). Das produziert über viele Runs eine erkennbare Familienähnlichkeit der Provokationen. Die Field-Test-Rule, die das korrigieren soll, wurde nie ausgelöst — weil sie am toten Ernte-Loop hängt. Außerdem: nur 4 von de Bonos 6 Operatoren aktiv (`distortion`, `arising` reserviert).

**Chat-Mode aus Ideenfindungssicht:** konzeptionell stark (Cross-Pollination mit counter/extend-Markern, Codex als *fremde* Jurorenstimme, transparentes W/U/S-Scoring pro Idee, „Kein Rewriting"-Regel die Rohstimmen schützt). Die harte 5-pro-Archetyp-Quote ist ein zweischneidiges Schwert: sie schützt Diversität, zwingt aber explizit schwache Ideen in die Final-20 („fülle mit schwächeren Kandidaten auf"). Für ein kuratiertes Endergebnis wäre eine Mindest-, keine Fix-Quote ehrlicher.

---

## 5. Gesamtbewertung des Vorgehens

| Dimension | Urteil |
|---|---|
| Konzeptionelle Kohärenz | Exzellent — „Divergenz, nie Beratung" ist in jede Schicht eingegossen, nicht nur deklariert |
| Voice-Engineering | Exzellent — verbotenes Vokabular macht Archetypen prüfbar statt erhofft; `[opt-care]` ist intellektuell herausragend |
| Generierungsqualität | Hoch — belegt am realen Output |
| Selbst-Governance | Mechanisch echt, praktisch tot — der kept-Loop wird nicht gefüttert |
| Steuerbarkeit des Verrücktheitsgrads | Fehlt — 60/40 ist weder kodiert noch messbar |
| Verwertung der Ideen | Schwächster Punkt — 1 von 10 Provokationen bekommt einen Pfad, der Rest verpufft; kein Anschluss an TODO/Wiki-Systeme |
| Code/Robustheit | Produktionsreif für den Scope (picker.py, Fallback-Pfade) |
| Doku-Hygiene | Gut — die Perplexity-Befunde (Naming, falsches 30pp-Zitat, tote Refs) sind bereits bereinigt |

Das Vorgehen des Projekts selbst (Rückbau v0.13.0, Museum-Clause, „Adoption ist das Risiko, nicht Build") ist die richtige Disziplin. Die nächste Ausbaustufe muss deshalb nicht *mehr Maschinerie* bringen, sondern **den Ernte- und Steuerungs-Pfad** — sonst wiederholt jede Erweiterung den Phase-4-8-Fehler.

---

## 6. Verbesserungsvorschläge am bestehenden Vorgehen (ohne neue Subsysteme)

1. **Review-Reflex in den nächsten Run einbauen.** Bevor ein neuer `/crazy`-Run startet, prüft der Skill die letzte field-notes-Zeile auf `pending` und stellt genau eine Frage („Letzter Run ‚dual-bridge': kept / verworfen / Wort müde?"). Eine Zeile Operating-Instructions, kein neues System — und der Governance-Loop bekommt erstmals Futter.
2. **60/40-Korridor in die Hard Rules.** Neue Regel: pro Run eine Soll-Mischung aus zahmen (`cost ≤ medium`) und wilden (`high`/`system-break`) Provokationen; weicht die ehrliche Verteilung ab, wird das im Output diagnostisch vermerkt („Topic erzeugte nur Schwergewichte — vermutlich zu abstrakt gestellt"). Cost-Tags bleiben ehrlich, aber die Mischung wird sichtbar gesteuert.
3. **Museum-Zähler in picker.py.** Der Picker liest die field-notes ohnehin — er soll `run_count` und `museum_check_due: true/false` im JSON zurückgeben. Damit feuert die Museum-Clause automatisch statt nie.
4. **Konzept-Klammer pro Provokation** (eine kurze Mechanismus-Extraktion). Minimal-invasive Umsetzung von de Bonos Movement-Schritt im bestehenden Template.
5. **`distortion` + `arising` aktivieren** — zwei Zeilen in po-operators.md + OPERATORS-Tupel; mod-6 statt mod-4. Mehr Bewegungsarten, null Risiko.
6. **Wort-Pool kuratieren:** 30–40 deutsche Wörter und 2–3 neue Themenfelder (Biologie, Recht, Spiel, Handwerk) beimischen, um die Heist-Lastigkeit zu brechen — unabhängig von der nie ausgelösten Retirement-Mechanik.
7. **Chat-Quote von „exakt 5" auf „3–5 pro Archetyp"** lockern, damit Codex schwache Ideen aussortieren darf statt sie aufzufüllen.

---

## 7. Zehn detaillierte Erweiterungen

Sortiert nach Hebelwirkung. Jede mit Mechanik, Aufwand (S/M/L), Philosophie-Fit und Risiko. Die Mischung ist selbst ~60/40: sechs direkt umsetzbar-sinnvolle, vier bewusst schräge mit Substanz.

### E1 — Harvest-Modus: `/crazy --harvest` (der fehlende Rückweg)
**Problem:** Ideen verpuffen; der kept-Loop verhungert.
**Mechanik:** Der Modus liest alle Output-Dateien mit `pending`-Flags, zeigt pro Run das Next-Experiment plus die 2 stärksten Provokationen als kompakte Triage-Liste, und nimmt Einzeiler-Verdikte entgegen (`1 kept, 2 backlog, rest verworfen`). Verdikte werden in field-notes geschrieben; `kept`-Experimente werden automatisch als DCO-Todo (`python tools/add_todo.py --tag recherche`) oder Wiki-TODO persistiert — Anschluss an das bereits existierende TODO-System statt eines neuen Systems. **Aufwand:** M. **Fit:** perfekt — es ist die Erfüllung der Museum-Clause, nicht ihre Umgehung. **Risiko:** keines; ohne diese Erweiterung bleibt jede andere Datensammlung sinnlos.

### E2 — Wildness-Dial: `/crazy <topic> --dial 0..100`
**Problem:** Das 60/40-Ziel ist nirgends steuerbar.
**Mechanik:** Der Dial übersetzt sich in eine Soll-Verteilung der Cost-Tags (Dial 60 → 6 Provokationen wild [`high`/`system-break`], 4 machbar [`low`/`medium`]) und in Operator-Gewichtung (hoher Dial bevorzugt exaggeration/escape, niedriger Dial reversal/wishful-thinking). Default 60. Der Picker gibt die Zielverteilung im JSON mit, das Template erhält sie als Generierungs-Constraint, der Output weist die Ist-Verteilung aus. **Aufwand:** S–M. **Fit:** gut — Cost-Tags bleiben ehrlich, nur die *Mischung* wird beauftragt. **Risiko:** Tag-Inflation (Modell labelt strategisch); Gegenmittel ist die Ist/Soll-Ausweisung im Output.

### E3 — Movement-Stufe: Konzept-Fan zwischen Provokation und Experiment
**Problem:** 9 von 10 Provokationen haben keinen Verwertungspfad.
**Mechanik:** Neuer Output-Abschnitt „## Extracted Concepts": die 10 Provokationen werden auf 3 tragende Mechanismus-Konzepte verdichtet (z.B. „Annexion durch Infrastruktur-Werdung", „Vertrags-Fassade bei freiem Umbau", „Quellen statt Mündung erobern"), jedes Konzept mit 2–3 *zahmen* Realisierungspfaden unterschiedlicher Kostenstufe. Das ist de Bonos Konzept-Fan als Skill-Schritt. Das Experiment wird danach aus einem Konzept gewählt, nicht aus einer Roh-Provokation. **Aufwand:** M. **Fit:** heikel, aber lösbar — die Konzept-Ebene muss als „Bewegungsmaterial" gerahmt sein, nicht als Empfehlung (Banner gilt weiter); die Hard Rule „never advice" bleibt intakt, weil Konzepte Optionen öffnen statt eine zu küren. **Risiko:** Advisor-Drift; Gegenmittel: Konzepte dürfen keine Imperativform tragen.

### E4 — Anchor-Verifikation: `anchor: ✓` / `anchor: ✗ fiktiv`
**Problem:** Die wichtigste Hard Rule ist unprüfbar.
**Mechanik:** Nach Generierung läuft pro Anker ein Glob/Grep gegen das Zielprojekt (Datei existiert? Symbol existiert?). Echte Anker bekommen ✓, erfundene werden *nicht zensiert*, sondern als `✗ fiktiv` markiert — analog zur `[opt-care]`-Philosophie: Drift sichtbar machen statt verbieten. Quote der ✓-Anker wandert als Spalte in die field-notes. **Aufwand:** S (der Agent hat die Tools bereits). **Fit:** exzellent — macht „anchor-or-it-doesnt-count" erstmals messbar. **Risiko:** false negatives bei konzeptionellen Ankern („die Gate-Approve-Kette"); deshalb Marker, kein Reject.

### E5 — Duett-Modus: `/crazy <topic> --duet jester,radagast`
**Problem:** Kosten-Loch zwischen Single (1 Call) und Chat (~10 Calls).
**Mechanik:** Genau zwei Archetypen, je 5 Provokationen, dann eine gegenseitige counter/extend-Runde (je 2), Distillation durch das Main-Model auf Top-6 — ~4 Calls, ~1 Minute. Die Paarwahl ist selbst kreatives Material: jester×radagast (Bruch vs. Schutz) erzeugt andere Spannungen als librarian×alchemist (Fremdimport vs. Eigenanalyse). Ohne Angabe wählt der Picker das Paar mit maximaler Werte-Spannung. **Aufwand:** M (Wrapper existieren konzeptionell schon). **Fit:** sauber — reine Rekombination bestehender Mechanik. **Risiko:** gering; ein Modus mehr in der Doku.

### E6 — Plan-Destabilizer: `/crazy --counter <plan-file>`
**Problem:** Der wertvollste Einsatzmoment — „Plan konvergierte zu schnell" — steht in der Skill-Description, hat aber keinen eigenen Eingang.
**Mechanik:** Input ist kein Topic, sondern ein Plan/ADR/Spec (Datei oder Diff). Jede Provokation muss eine *konkrete Annahme des Plans* als Anker nennen (Zeile, Entscheidung, Phase) und sie mit dem gezogenen Operator attackieren. Output endet mit dem einen Experiment: „Welche Annahme in 1 Stunde falsifizierbar?" Damit dockt der Professor an den superpowers-Workflow an (brainstorming → writing-plans → **crazy --counter** → executing-plans) als bewusster Destabilizer-Schritt vor dem Festzurren. **Aufwand:** M. **Fit:** sehr gut — Konventionen angreifen, Ziele respektieren, gilt für Pläne identisch. **Risiko:** Verwechslung mit Review-Skills; klare Abgrenzung in der Description nötig (kein Finding, keine Bewertung — nur Provokation).

### E7 — Echo-Bibliothek: Cross-Projekt-Provokations-Transfer
**Problem:** `kept`-Provokationen sind das wertvollste Artefakt des Systems und sterben im Projektordner.
**Mechanik:** `kept`-markierte Provokationen werden (via bestehendem agentic-os:sync-Pfad) nach `~/.claude-memory/global/crazy-professor/echoes.md` gespiegelt — Provokation + Konzept + Herkunftsprojekt. Bei neuen Runs zieht der Picker mit 25% Wahrscheinlichkeit ein fremdes Echo als *viertes Stimulus-Element*: „Echo aus Projekt X: ‚Vertrags-Fassade bei freiem Umbau' — lass es mitschwingen." Kein Ratschlag, ein zusätzlicher Reiz — wie ein Provokationswort mit Vorgeschichte. **Aufwand:** M. **Fit:** grenzwertig konform, aber sauber, solange Echos Stimulus bleiben und nie „hat dort funktioniert, also…"-Framing tragen. **Risiko:** Selbstreferentialität (das System inspiriert sich an sich selbst); Gegenmittel: Echos altern aus (max. 90 Tage).

### E8 — Saison-Pools: rotierende Wortwelten
**Problem:** Die Heist/Theater-Homogenität des Pools erzeugt Familienähnlichkeit der Outputs; Retirement allein korrigiert keine thematische Schlagseite.
**Mechanik:** Der Pool wird in 4–6 benannte Welten partitioniert (heist, organisch, juristisch, handwerklich, sakral, spielerisch; je 30–40 Wörter, DE+EN gemischt). Der Picker rotiert die aktive Welt monatlich (oder per `--world`), die field-notes loggen die Welt. Nach einigen Monaten zeigt der Harvest-Modus (E1), welche Welt die höchste kept-Rate hat — die Field-Test-Rule bekommt damit eine zweite, gröbere Wirkebene. **Aufwand:** S–M (Kuratierungsarbeit dominiert). **Fit:** voll konform — es ist Pflege des lebenden Artefakts, das die Hard Rules ohnehin vorsehen. **Risiko:** keines; schlimmstenfalls egal.

### E9 — Fünfter Archetyp: stage-magician (aus der Roadmap geholt)
**Problem:** Die vier Achsen (Bruch / Fremdimport / Umverdrahtung / Schutz) lassen eine Lücke: **Aufmerksamkeit und Wahrnehmung** selbst.
**Mechanik:** Der stage-magician arbeitet mit Misdirection — er fragt nicht „was ist das Problem?", sondern „wohin schaut hier jeder, und was passiert währenddessen in der anderen Hand?" Pflicht-Vokabular: Bühne, Requisite, Trick, Publikum, Reveal, Timing, Vorhang, Palmieren. Verboten: alles System-, Natur- und Fremdfeld-Vokabular der anderen vier. Pflicht-Pointe: jede Provokation endet mit einem Reveal („das eigentliche Kunststück geschah, als…"). Per Roadmap bewusst geparkt bis Radagast sich beweist — Radagast ist seit 2026-04-23 aktiv und stabil, die Bedingung ist erfüllbar. **Aufwand:** M (Template + Blindtest-Protokoll analog Radagast + mod-5-Picker). **Fit:** konform, in der Roadmap vorgesehen. **Risiko:** Wartungslast wächst (5. Vokabular-Vertrag); Overlap-Gefahr mit jester (beide arbeiten mit Täuschung der Erwartung) — der Blindtest muss das vor Aktivierung trennen.

### E10 — Lab v2 als Harvest-Oberfläche (Paste-only abschaffen)
**Problem:** Das Lab ist das designierte Triage-Werkzeug, aber der Medienbruch verhindert genau die Triage.
**Mechanik:** `/crazy --lab` generiert das HTML weiterhin statisch, inlined aber beim Öffnen die aktuellen Output-Dateien und field-notes des Zielprojekts (Python liest die Dateien, schreibt sie als JS-Konstanten ins HTML — die Technik existierte schon im zurückgebauten build_playground.py und kann per `git show` reaktiviert werden). Im Browser: Run-Liste, Provokationen mit kept/backlog/verworfen-Buttons, Export als fertige field-notes-Zeile zum Einfügen (oder Copy-Paste-Kommando). Kein Server, kein LLM — die v0.13.0-Linie bleibt gewahrt. **Aufwand:** M–L. **Fit:** gut, *unter einer Bedingung*: erst bauen, wenn E1 zeigt, dass überhaupt kuratiert wird — sonst ist es exakt der Phase-7-Fehler in neuem Gewand. **Risiko:** genau dieser; deshalb als letzte der zehn gereiht.

---

## Schlussbild

Der Skill ist handwerklich und philosophisch das Gegenteil von sinnlos — die Anker-Pflicht, die Cost-Tags und das Eine-Experiment-Prinzip erzeugen bereits heute eine kreative Durchmischung mit Bodenhaftung. Was fehlt, ist nicht mehr Verrücktheit, sondern **drei Pfade**: der Regler (E2: 60/40 steuerbar machen), die Brücke (E3: Konzept-Extraktion, damit wilde Ideen zahme Kinder bekommen können) und der Rückweg (E1: Ernte ins TODO-/Wiki-System). Mit diesen dreien beginnt der Governance-Loop erstmals zu drehen — und erst danach lohnen die Ausbau-Ideen E5–E10, ohne den dokumentierten Phase-4-8-Fehler zu wiederholen.

**Umsetzungsentscheidung 2026-06-12:** E1–E3 wurden direkt im Anschluss an diese Analyse als v0.14.0 umgesetzt.
