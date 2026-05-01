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
-Die neue Präsentationsdatei mit Git zum Repository hinzugefügt, committed und erfolgreich auf GitHub gepusht.

-REST API Design:
 Wichtige Erkenntnis: Bei REst APIs stegt die Aktion nicht direkt in der URL, sondern wird über die HTTP-Methode bestimmt:
- `GET` zum Lesen von Daten
- `POST` zum Erstellen neuer Daten
- `PUT` zum Aktualisieren bestehender Daten
- `DELETE` zum Löschen von Daten

-Bei REST APIs beschreibt die URL nur die Ressource, die HTTP-Methode bestimmt die Aktion, und der HTTP-Status-Code zeigt, ob die Anfrage erfolgreich war oder welcher Fehler passiert ist.

-`Path Parameter` sind feste Bestandteile der URL, werden zur Identifikation bestimmter Ressourcen genutzt und die Reihenfolge der Endpoints ist wichtig, weil allgemeinere Routen wie "/test/{wert}" spezifische routen wie "/test/123" abfangen können.

-FASTAPI prüft und konventiert Path Parameters automatisch. Dadurch muss man nicht selbst konttrollieren, ob zum Beispiel eine ID wirklich eine Zahl ist.

-`Query Parameters` stehen nach dem ? in der URL, sind meistens optional und werden verwendet, um Ergebnisse zu filtern, zu suchen, zu sortieren oder mehrere Bedingungen wie semster, min_ects und search miteinander zu kombinieren.

-Der bestehende `GET /notes` Endpoint wurde erweitert, sodass Notizen jetzt mit optionalen Query Parameters nach `category`, `search` und `tag` gefiltert werden können; dabei werden nicht passende Notizen mit `continue` übersprungen und nur passende Ergebnisse zurückgegeben.

-Der `DELETE /notes/{note_id}` Endpoint wurde angepasst und getestet, sodass eine bestehende Notiz anhand ihrer ID gelöscht wird; bei erfolgreichem Löschen gibt die API den Status Code `204 No Content` zurück, während bei einer nicht vorhandenen ID ein `404 Not Found` Fehler erscheint.

-Der neue `GET /tags` Endpoint wurde implementiert und getestet; er sammelt alle Tags aus den gespeicherten Notizen, entfernt doppelte Einträge mithilfe eines Sets und gibt die eindeutigen Tags als sortierte Liste zurück.

-Der Endpoint `GET /tags/{tag_name}/notes` wurde hinzugefügt, um alle Notizen mit einem bestimmten Tag abzurufen. Dafür werden alle gespeicherten Notizen geladen, nach dem angegebenen Tag durchsucht und nur die passenden Notizen als Liste zurückgegeben.

Homework:

-Der `GET /notes`Endpoint wurde mit mehreren Query-Parametern gleichzeitig getestet, sodass category, search und tag gemeinsam als AND-Filter funktionieren.

-Der neue Endpoint `GET /notes/stats` wurde erstellt und getestet, um Statistiken über die gespeicherten Notes auszugeben, darunter die Gesamtanzahl, Notes pro Kategorie, die Top 5 Tags und die Anzahl eindeutiger Tags.

-Der neue Categories-Resource-Endpoint wurde erstellt und getestet, um alle eindeutigen Kategorien über `/categories` auszugeben und über `/categories/{category_name}/notes` alle Notes einer bestimmten Kategorie abzurufen.

-Der neue PATCH `/notes/{note_id}`Endpoint wurde implementiert und getestet, um einzelne Felder einer Note teilweise zu aktualisieren, ohne die gesamte Note ersetzen zu müssen.

-Der bestehende GET /notes-Endpoint wurde um die optionalen Query-Parameter created_after und created_before erweitert, damit Notes zusätzlich nach einem Datumsbereich gefiltert werden können.

-Der bisherige JSON-basierte Speicher wurde durch eine SQLite-Datenbank mit SQLModel ersetzt. Dafür wurden Datenbank-Modelle für Notes, Tags und die Verbindung zwischen Notes und Tags erstellt. Anschließend wurden die Speicherfunktionen so angepasst, dass Notes aus der Datenbank geladen und dort gespeichert werden.

-Der bisherige JSON-basierte Speicher wurde auf eine SQLite-Datenbank mit SQLModel umgestellt. Dafür wurden Datenbank-Modelle für Notes, Tags und die Verbindung zwischen Notes und Tags erstellt. Danach wurden die wichtigsten Endpoints Schritt für Schritt auf Datenbank-Sessions mit SessionDep umgebaut und getestet: POST, GET, PATCH, PUT, DELETE, /notes/stats, /categories und /categories/{category_name}/notes.


---

#### 2. 🚧 What challenges did I face?
-Beim Testen des Tag-Endpunkts habe ich nach dem Tag `sport` gesucht, aber die erwartete Note nicht gefunden, obwohl sie mit einem Sport-Tag markiert war. Zuerst war mir nicht klar, woran das Problem lag.

Homework:

-Beim Testen kamen zuerst leere Ergebnisse ([]) zurück, weil die vorhandenen Notes nicht zu den geforderten Filterwerten wie work, urgent, personal, family und vacation passten.

-Eine Herausforderung war, dass ich die Counter-Dokumentation zuerst verstehen musste, bevor ich sie im Code richtig anwenden konnte. Das hat mehr Zeit gekostet als erwartet.

-Beim Testen wurde zuerst versehentlich ein vollständiger Body bzw. ungültiges JSON mit einem Komma am Ende gesendet, wodurch nicht klar erkennbar war, ob PATCH wirklich nur einzelne Felder aktualisiert.

-Es war schwer zu verstehen, wie die gespeicherten created_at-Werte mit den neuen Datumsfiltern verglichen werden können, ohne eine komplizierte Datumskonvertierung einzubauen.

-Eine Herausforderung war, die bestehende API-Struktur beizubehalten, obwohl die Speicherung intern von JSON auf SQLite umgestellt wurde. Besonders wichtig war dabei, die Tags korrekt als eigene Datenbankeinträge zu speichern und trotzdem im API-Response weiterhin als einfache Liste auszugeben.


---

#### 3. 💡 How did I overcome them?
-Um das Problem zu lösen, habe ich eine weitere Test-Note erstellt und den Tag `sport` verwendet. Danach habe ich den Endpoint `GET /tags/{tag_name}/notes` erneut getestet und die neue Note gefunden. Nach längerem Prüfen wurde klar, dass die erste Note nicht angezeigt wurde, weil der ursprüngliche Tag `Sport` mit großem Anfangsbuchstaben gespeichert war und der Endpoint Groß- und Kleinschreibung unterscheidet.

Homework:

-Ich habe zuerst die gespeicherten Notes überprüft und danach passende Test-Notes erstellt, damit die Kombinationen aus category, search und tag korrekt getestet werden konnten.

-Ich habe Gemini gefragt, ob es mir nur die wichtigsten und notwendigen Punkte aus der Counter-Dokumentation für Task 2 erklären kann. Danach habe ich verstanden, wie Counter zum automatischen Zählen von Kategorien und Tags verwendet wird und wie man mit most_common(5) die fünf häufigsten Tags ausgibt. Prompt, den ich Gemini gegeben habe: "Can you explain only the necessary parts of the Python Counter documentation that I need for this task? I need to create a /notes/stats endpoint that counts total notes, notes per category, top 5 most used tags, and the number of unique tags. Please explain it simply with a small example."

-Beim Testen wurde zuerst versehentlich ein vollständiger Body bzw. ungültiges JSON mit einem Komma am Ende gesendet, wodurch nicht klar erkennbar war, ob PATCH wirklich nur einzelne Felder aktualisiert.

-Ich habe zuerst die SQLModel-Struktur vorbereitet und anschließend Hilfsfunktionen verwendet, um Datenbank-Objekte wieder in normale API-Objekte umzuwandeln. Danach habe ich alle wichtigen Endpoints getestet: POST, GET, PATCH, PUT, DELETE, /notes/stats und /categories.



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













