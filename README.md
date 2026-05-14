# Applied Programming Notes API

Dieses Repository enthält mein Lernprojekt für den Kurs **Angewandete Programmierung**. Die Anwendung ist eine einfache Notes API mit **FastAPI**, **Pydantic**, **SQLModel** und **SQLite**.

Im Projekt wurden mehrere Kursthemen kombiniert: REST-Endpunkte, Query Parameter, Validierung, Datenbankanbindung, Tags, Kategorien und einfache Statistiken.

---

## Setup & Entwicklung

Abhängigkeiten installieren:

```bash
uv sync
```

FastAPI-Server starten:

```bash
uv run fastapi dev main.py
```

Nach dem Start ist die Swagger-Dokumentation erreichbar unter:

```text
http://127.0.0.1:8000/docs
```

Tests ausführen:

```bash
uv run pytest test_notes_api.py -v
```

Dieser Befehl wird verwendet, um die wichtigsten API-Tests für die Notes-Anwendung auszuführen.

---

## Projektstruktur

```text
applied-programmierung-project/
├── main.py                 # Hauptdatei der FastAPI-Anwendung
├── frontend.py             # Streamlit-Frontend für die Anwendung
├── test_notes_api.py       # Tests für die wichtigsten API-Funktionen
├── work-log.md             # Dokumentation der eigenen Arbeitsschritte
└── README.md               # Projektdokumentation
```

---

## Architektur

Die Anwendung besteht aus einer FastAPI-App, mehreren Pydantic-Modellen für Eingabe und Ausgabe sowie SQLModel-Tabellen für die Datenbank.

### FastAPI

Die API stellt verschiedene Endpunkte bereit, mit denen Notizen erstellt, gelesen, bearbeitet und gelöscht werden können. Zusätzlich gibt es Endpunkte für Kategorien, Tags, Statistiken und Query-Parameter.

### Pydantic-Modelle

Die Eingabedaten werden mit Pydantic validiert:

* `NoteCreate` wird für das Erstellen neuer Notizen verwendet.
* `NoteUpdate` wird für PATCH-Anfragen verwendet, bei denen nur einzelne Felder geändert werden.
* `NoteResponse` beschreibt die Antwort, die an den Client zurückgegeben wird.
* `Note` wird noch von älteren Hilfsfunktionen genutzt.

Dabei werden unter anderem Titel, Inhalt, Kategorien und Tags geprüft. Kategorien werden vereinheitlicht und nur bestimmte Kategorien sind erlaubt. Tags werden bereinigt, in Kleinschreibung umgewandelt und doppelte Tags werden entfernt.

### SQLite und SQLModel

Die Daten werden nicht mehr nur in einer JSON-Datei gespeichert, sondern in einer SQLite-Datenbank.

Dafür wurden folgende Datenbankmodelle erstellt:

* `NoteDB` für Notizen
* `TagDB` für Tags
* `NoteTagLink` als Verbindungstabelle zwischen Notizen und Tags

Zwischen Notizen und Tags besteht eine **Many-to-Many-Beziehung**, da eine Notiz mehrere Tags haben kann und ein Tag zu mehreren Notizen gehören kann.

### Migration von JSON zu SQLite

Falls noch alte Daten in `data/notes.json` vorhanden sind, können diese beim Start der Anwendung automatisch in die SQLite-Datenbank übernommen werden. Bereits vorhandene Notizen werden dabei übersprungen, damit keine Duplikate entstehen.

---

## Wichtige Endpunkte

### Startseite

```http
GET /
```

Gibt eine kurze Übersicht über die API und die wichtigsten Endpunkte zurück.

### Alle Notizen abrufen

```http
GET /notes
```

Optional können Filter verwendet werden:

```http
GET /notes?category=work
GET /notes?search=meeting
GET /notes?tag=urgent
GET /notes?created_after=2026-05-12
GET /notes?created_before=2026-05-14
```

### Neue Notiz erstellen

```http
POST /notes
```

Beispiel-Body:

```json
{
  "title": "Meeting vorbereiten",
  "content": "Agenda schreiben und Unterlagen sammeln",
  "category": "work",
  "tags": ["work", "urgent"]
}
```

### Einzelne Notiz abrufen

```http
GET /notes/{note_id}
```

### Notiz vollständig ersetzen

```http
PUT /notes/{note_id}
```

PUT ersetzt die komplette Notiz durch die neu gesendeten Daten.

### Notiz teilweise bearbeiten

```http
PATCH /notes/{note_id}
```

PATCH ändert nur die Felder, die in der Anfrage mitgeschickt werden.

Beispiel:

```json
{
  "title": "Neuer Titel"
}
```

### Notiz löschen

```http
DELETE /notes/{note_id}
```

Löscht eine Notiz aus der Datenbank.

### Statistiken abrufen

```http
GET /notes/stats
```

Gibt einfache Statistiken zurück:

* Gesamtanzahl der Notizen
* Anzahl der Notizen pro Kategorie
* Top 5 Tags
* Anzahl der eindeutigen Tags

### Kategorien abrufen

```http
GET /categories
```

Gibt alle verwendeten Kategorien sortiert zurück.

```http
GET /categories/{category_name}/notes
```

Gibt alle Notizen einer bestimmten Kategorie zurück.

### Tags abrufen

```http
GET /tags
```

Gibt alle verwendeten Tags sortiert und ohne Duplikate zurück.

```http
GET /tags/{tag_name}/notes
```

Gibt alle Notizen zurück, die ein bestimmtes Tag besitzen.

### Query-Parameter-Beispiel

```http
GET /queryparameters?param1=ar&param2=5
```

Dieser Endpunkt zeigt, wie Query Parameter in FastAPI verwendet und verarbeitet werden können.

---

## Validierung

Beim Erstellen und Bearbeiten von Notizen werden mehrere Regeln geprüft:

* Der Titel muss mindestens 3 Zeichen lang sein.
* Der Inhalt darf nicht leer sein.
* Die Kategorie muss zu den erlaubten Kategorien gehören.
* Tags dürfen nicht leer sein.
* Tags werden in Kleinschreibung gespeichert.
* Doppelte Tags werden entfernt.
* Zusätzliche, nicht definierte Felder sind nicht erlaubt.

Dadurch sollen ungültige oder uneinheitliche Daten verhindert werden.

---

## Testen

Die Anwendung kann mit Pytest getestet werden.

Typische Testbereiche sind:

* Erstellen von Notizen
* Validierung ungültiger Eingaben
* Abrufen einzelner und mehrerer Notizen
* Aktualisieren mit PUT und PATCH
* Löschen von Notizen
* Sortierte und eindeutige Tags
* Statistiken über Kategorien und Tags

Tests können mit folgendem Befehl gestartet werden:

```bash
uv run pytest test_notes_api.py -v
```

---

## Hinweise

* Die Anwendung nutzt SQLite als lokale Datenbank.
* Beim Start werden die Datenbanktabellen automatisch erstellt.
* Alte JSON-Daten aus `data/notes.json` können automatisch migriert werden.
* Die Swagger-Dokumentation unter `/docs` kann verwendet werden, um die API direkt im Browser zu testen.
* Für die finale Abgabe sollte geprüft werden, dass jeder Endpoint nur einmal definiert ist, besonders `/notes/stats`.

---

## Lernziele

In diesem Projekt wurden folgende Themen praktisch umgesetzt:

* Aufbau einer FastAPI-Anwendung
* REST-Endpunkte mit GET, POST, PUT, PATCH und DELETE
* Query Parameter
* Request- und Response-Modelle mit Pydantic
* Eingabevalidierung mit Validatoren
* Speicherung von Daten mit SQLite und SQLModel
* Many-to-Many-Beziehung zwischen Notizen und Tags
* Migration von JSON-Daten in eine Datenbank
* Testen der API mit Pytest
* Arbeiten mit Swagger UI zur manuellen API-Prüfung

---

## Persönliche Umsetzung

Der Fokus lag darauf, die Notes API Schritt für Schritt zu erweitern. Zuerst wurden einfache Endpunkte für Notizen umgesetzt. Danach kamen Validierung, Kategorien, Tags, Statistiken und schließlich die Umstellung auf eine SQLite-Datenbank dazu.

Besonders wichtig war dabei, dass die Daten konsistent bleiben. Deshalb werden Kategorien und Tags normalisiert, doppelte Tags entfernt und ungültige Eingaben durch klare Validierungsregeln abgefangen.

Durch die Umstellung auf SQLite ist die Anwendung näher an einer echten Backend-Anwendung. Gleichzeitig bleibt das Projekt übersichtlich, weil alle zentralen Funktionen in `main.py` nachvollziehbar zusammengeführt
