from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path



app = FastAPI(
    title="Applied Programmierung Course HS-Coburg",
    description="Simple note management API",
    version="1.0.0"
)

####################################################################
#### Note API Endpoints (Day 2)
####################################################################

class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []


class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str] = []
    created_at: str


NOTES_FILE = Path("data/notes.json")


def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    notes_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            # Set counter to max ID + 1
            if notes_db:
                notes_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, notes_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:
    """Create a new note"""

    notes_db, notes_id_counter = load_notes()

    new_note = Note(
        id=notes_id_counter,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=note.tags,
        created_at=datetime.now(timezone.utc).isoformat()
    )

    notes_db.append(new_note)
    save_notes(notes_db)
    
    return new_note


@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None
) -> list[Note]:
    """
    List notes with optional filters:
    - category: filter by category
    - search: search in title and content
    - tag: filter by tag
    """
    notes_db, _ = load_notes()

    filtered_notes = []

    for note in notes_db:
        # Filter by category
        if category and note.category != category:
            continue

        # Filter by search text in title or content
        if search:
            search_lower = search.lower()
            title_match = search_lower in note.title.lower()
            content_match = search_lower in note.content.lower()

            if not (title_match or content_match):
                continue

        # Filter by tag
        if tag and tag not in note.tags:
            continue

        filtered_notes.append(note)

    return filtered_notes


@app.get("/notes/category/{category}")
def get_notes_by_category(category: str) -> list[Note]:
    """Get all notes in a specific category"""
    notes_db, _ = load_notes()

    filtered_notes = []

    for note in notes_db:
        if note.category == category:
            filtered_notes.append(note)

    return filtered_notes


@app.get("/notes/stats")
def get_notes_stats():
    """Get statistics about notes"""
    notes_db, _ = load_notes()

    categories = {}

    for note in notes_db:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1

    return {
        "total_notes": len(notes_db),
        "by_category": categories
    }


@app.get("/tags")
def list_tags() -> list[str]:
    """Get all unique tags from all notes"""
    notes_db, _ = load_notes()

    all_tags = set()

    for note in notes_db:
        for tag in note.tags:
            all_tags.add(tag)

    return sorted(list(all_tags))

@app.get("/notes/{note_id}")
def get_note(note_id: int) -> Note:
    """Get a specific note by ID"""
    notes_db, _ = load_notes()

    for note in notes_db:
        if note.id == note_id:
            return note

    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate) -> Note:
    """Update an existing note"""
    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated_note = Note(
                id=note.id,
                title=note_update.title,
                content=note_update.content,
                category=note_update.category,
                tags=note_update.tags,
                created_at=note.created_at
            )

            notes_db[i] = updated_note
            save_notes(notes_db)

            return updated_note

    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    """Delete a note"""
    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            save_notes(notes_db)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )


@app.get("/queryparameters")
def query_parameters(param1: str = None, param2: int = None) -> dict:

    print("start query_parameters")
    print(param1, param2)
    
    """
    Example endpoint to demostrate query parameters

    - **param1**: A string parameter
    - **param2**: An integer parameter

    Returns a JSON onject with the provided parameters
    
    """
    namen = ['martin', 'sophia', 'michael', 'maryam', 'arezoo', 'armin']

    if not param1:
        return {"namen": namen}
             
    namen_gefiltert = []
    for name in namen:
        if param1 and param1 in name:
            namen_gefiltert.append(name)

    return {
        "param1": param1,
        "param2": param2, 
        "namen": namen_gefiltert
    }