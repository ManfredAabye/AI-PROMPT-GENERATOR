# TODO — VSCode Copilot Planning-Style Integration

für [AI-PROMPT-GENERATOR](https://github.com/ManfredAabye/AI-PROMPT-GENERATOR.git?utm_source=chatgpt.com)

## Phase 1 — Grundlage

### Kernarchitektur

* [ ] Analyse der bestehenden Prompt-Pipeline
* [ ] Identifizieren, wo Reasoning-Strategien injiziert werden
* [ ] Neue `planning` Prompt-Kategorie definieren
* [ ] Task-Typ-Erkennung erweitern
* [ ] Komplexitätserkennung hinzufügen
* [ ] Strategie-Injektionsschicht erstellen

---

## Phase 2 — Planungsstrategie-System

### Neue Verzeichnisstruktur

```text
/strategies
    /planning
    /reflection
    /verification
    /decomposition
```

### Planungsvorlagen

* [ ] `discovery.md`
* [ ] `alignment.md`
* [ ] `design.md`
* [ ] `refinement.md`

### Kognitive Muster

* [ ] TODO-Tracking-Anweisungen
* [ ] Schrittzerlegung
* [ ] Abhängigkeitsanalyse
* [ ] Meilensteinplanung
* [ ] Risikoerkennung
* [ ] Selbstüberprüfung
* [ ] Verifizierungsschicht

---

## Phase 3 — Strategie-Engine

### `strategy_selector.py`

* [ ] Task-Typ-Zuordnung
* [ ] Komplexitätsbewertung
* [ ] Dynamische Strategieauswahl
* [ ] Token-Budget-Bewusstsein
* [ ] Minimale vs. tiefe Planungsmodi

### `reasoning_engine.py`

* [ ] Strategie-Lader
* [ ] Prompt-Injektionslogik
* [ ] Strategie-Reihenfolge
* [ ] Konfliktlösung
* [ ] Entfernung von Duplikaten

---

## Phase 4 — VSCode-Planungsmodus-Vorlagen

### Neue Prompt-Modi

* [ ] `planning-agent`
* [ ] `architect-agent`
* [ ] `implementation-planner`
* [ ] `refinement-agent`
* [ ] `enterprise-coding-agent`

### VSCode-ähnliche Verhaltensweisen

* [ ] Entdeckungsphase
* [ ] Abstimmungsphase
* [ ] Entwurfsphase
* [ ] Verfeinerungsphase
* [ ] Fortschrittsverfolgung
* [ ] TODO-Pflege
* [ ] Kontextvalidierung

---

## Phase 5 — TODO-System

### TODO-Erzeugung

* [ ] Automatische Aufgabenzerlegung
* [ ] Hierarchische TODO-Listen
* [ ] Meilensteinerzeugung
* [ ] Prioritätskennzeichnung
* [ ] Abhängigkeitsverfolgung
* [ ] Fortschrittsmarkierungen

### TODO-Prompt-Muster

* [ ] "Führe eine laufende TODO-Liste"
* [ ] "Aktualisiere abgeschlossene Schritte"
* [ ] "Bewerte nach jedem Meilenstein neu"
* [ ] "Verfolge Blockaden und Annahmen"

---

## Phase 6 — Prompt-Optimierung

### Optimierungsschicht

* [ ] Entferne redundantes Reasoning
* [ ] Komprimiere sich wiederholende Anweisungen
* [ ] Führe kompatible Strategien zusammen
* [ ] Dynamische Ausführlichkeitssteuerung
* [ ] Kurze/mittlere/tiefe Modi

---

## Phase 7 — Exportformate

### Exportziele

* [ ] Generischer LLM-Prompt
* [ ] VSCode Copilot-Prompt
* [ ] Cursor-Regeln
* [ ] Claude Code-Prompt
* [ ] Windsurf-Prompt
* [ ] OpenAI-System-Prompt

---

## Phase 8 — Erweiterte Planungsfunktionen

### Adaptive Planung

* [ ] Leichte Planung für einfache Aufgaben
* [ ] Tiefe Planung für Architekturaufgaben
* [ ] Automatische Auswahl der Planungstiefe

### Reflexionssystem

* [ ] Selbstkritik-Prompts
* [ ] Konsistenzprüfung
* [ ] Randfallanalyse
* [ ] Halluzinationsreduzierung

---

## Phase 9 — Tests

### Auswertung

* [ ] Vergleiche Prompts mit/ohne Planung
* [ ] Bewertung der Codequalität
* [ ] Messung des Token-Overheads
* [ ] Validierung des TODO-Nutzens
* [ ] Test der VSCode Copilot-Kompatibilität

---

## MVP (Empfohlen)

Wenn du schnell etwas Funktionierendes willst:

## Unbedingt zuerst bauen

* [ ] Strategie-Injektionsschicht
* [ ] Planungsvorlagen
* [ ] TODO-Prompt-Muster
* [ ] Komplexitätserkennung
* [ ] `planning-agent`-Modus

Das reicht bereits für einen starken VSCode-ähnlichen Planungsmodus.

---

## Beispiel Endziel

## Eingabe

```text
Erstelle eine skalierbare Microservice-Architektur
```

## Ausgabe

```text
Du bist ein erfahrener Planungs-Agent.

Führe eine laufende TODO-Liste.

PHASE 1 — ENTDECKUNG
...

PHASE 2 — ENTWURF
...

Verfolge den Fortschritt kontinuierlich.
Bewerte Architekturentscheidungen nach jedem Meilenstein neu.
Validiere Annahmen vor der Implementierung.
```

Das ist praktisch ein Copilot-Planungs-Agent — aber vollständig promptbasiert.

---

## Prüfergebnis

Das Originaldokument ist **strukturell sauber, gut durchdacht und technisch sinnvoll**. Die Übersetzung ist präzise und behält alle Fachbegriffe sowie die Checklisten-Struktur bei. Keine inhaltlichen Fehler erkennbar. ✅
