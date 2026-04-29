# Work Log

**Student Name:** Arezoo Mohammadi

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?



---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?




---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 2

#### 1. ✅ What did I accomplish?
- Ich habe die Note Taking API ab Step 10 weiterentwickelt und mehrere neue Endpoints erstellt und getestet.

- Ich habe `GET /notes/{note_id}` umgesetzt, damit man eine einzelne Note über ihre ID abrufen kann. Dabei habe ich Path Parameters in FastAPI geübt und getestet, dass nicht vorhandene IDs einen `404 Not Found` Fehler zurückgeben.

- Ich habe File Persistence eingebaut, sodass Notes in `data/notes.json` gespeichert und nach einem Server-Neustart wieder geladen werden. Dafür habe ich `load_notes()` und `save_notes()` verwendet.

- Ich habe das `category` Feld zu den Notes hinzugefügt. Dafür habe ich die Models `NoteCreate` und `Note` erweitert und `create_note()` angepasst, damit neue Notes auch eine Kategorie speichern.

- Ich habe den Endpoint `GET /notes/category/{category}` erstellt, um Notes nach Kategorie zu filtern, zum Beispiel alle Notes mit der Kategorie `study`.

- Ich habe den Endpoint `GET /notes/stats` erstellt, der die Gesamtzahl der Notes und die Anzahl der Notes pro Kategorie zurückgibt.

- Ich habe als Extra Task den Endpoint `DELETE /notes/{note_id}` erstellt, damit Notes über ihre ID gelöscht werden können. Nach dem Löschen wird `data/notes.json` aktualisiert.

- Ich habe alle Endpoints in Swagger UI `/docs` getestet: `POST /notes`, `GET /notes`, `GET /notes/{note_id}`, `GET /notes/category/{category}`, `GET /notes/stats` und `DELETE /notes/{note_id}`.


---

#### 2. 🚧 What challenges did I face?
- Eine Schwierigkeit war zu verstehen, an welcher Stelle neue Endpoints eingefügt werden müssen. Besonders wichtig war, dass `/notes/stats` und `/notes/category/{category}` vor `/notes/{note_id}` stehen müssen.

- Ich hatte einen `IndentationError`, weil der Code unter `def get_note(...)` nicht richtig eingerückt war. Dadurch konnte der Server nicht starten.

- Ich hatte ein ID-Problem: Alle Notes hatten zuerst `id: 1`. Der Grund war ein falscher Variablenname beim ID-Counter in `load_notes()`.

- Neue Notes waren in VS Code nicht sofort in `notes.json` sichtbar. Später habe ich gemerkt, dass VS Code die geöffnete Datei nicht automatisch aktualisiert hatte.

- Nach dem Hinzufügen von `category` kam zuerst ein `500 Internal Server Error`, weil alte Notes in `data/notes.json` noch kein `category` Feld hatten.

- Beim DELETE Endpoint war zuerst unklar, dass ich mit `GET /notes` zuerst eine existierende ID suchen muss, bevor ich diese ID mit `DELETE /notes/{note_id}` löschen kann.


---

#### 3. 💡 How did I overcome them?

- Eine Schwierigkeit war zu verstehen, an welcher Stelle neue Endpoints eingefügt werden müssen. Besonders wichtig war, dass `/notes/stats` und `/notes/category/{category}` vor `/notes/{note_id}` stehen müssen.

- Ich hatte einen `IndentationError`, weil der Code unter `def get_note(...)` nicht richtig eingerückt war. Dadurch konnte der Server nicht starten.

- Ich hatte ein ID-Problem: Alle Notes hatten zuerst `id: 1`. Der Grund war ein falscher Variablenname beim ID-Counter in `load_notes()`.

- Neue Notes waren in VS Code nicht sofort in `notes.json` sichtbar. Später habe ich gemerkt, dass VS Code die geöffnete Datei nicht automatisch aktualisiert hatte.

- Nach dem Hinzufügen von `category` kam zuerst ein `500 Internal Server Error`, weil alte Notes in `data/notes.json` noch kein `category` Feld hatten.

- Beim DELETE Endpoint war zuerst unklar, dass ich mit `GET /notes` zuerst eine existierende ID suchen muss, bevor ich diese ID mit `DELETE /notes/{note_id}` löschen kann.


---

### Day 3

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 5

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 6

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













