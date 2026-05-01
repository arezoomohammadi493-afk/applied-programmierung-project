from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path
from collections import Counter
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select



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

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None

class NoteTagLink(SQLModel, table=True):
    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)


class NoteDB(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tags: list["TagDB"] = Relationship(back_populates="notes", link_model=NoteTagLink)


class TagDB(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    notes: list[NoteDB] = Relationship(back_populates="tags", link_model=NoteTagLink)


DATABASE_URL = "sqlite:///notes.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def db_note_to_note(note_db: NoteDB) -> Note:
    """Convert database note to API note"""
    return Note(
        id=note_db.id,
        title=note_db.title,
        content=note_db.content,
        category=note_db.category,
        tags=[tag.name for tag in note_db.tags],
        created_at=note_db.created_at.isoformat()
    )



NOTES_FILE = Path("data/notes.json")


def load_notes():
    """Load notes from SQLite database and return notes list and next ID counter"""
    create_db_and_tables()

    with Session(engine) as session:
        notes_db = session.exec(select(NoteDB)).all()

        notes = []
        for note_db in notes_db:
            notes.append(db_note_to_note(note_db))

        if notes:
            next_id_counter = max(note.id for note in notes) + 1
        else:
            next_id_counter = 1

        return notes, next_id_counter


def save_notes(notes: list[Note]):
    """Save notes to SQLite database"""
    create_db_and_tables()

    with Session(engine) as session:
        # Clear existing link table, notes and tags
        existing_notes = session.exec(select(NoteDB)).all()
        for note_db in existing_notes:
            session.delete(note_db)

        existing_tags = session.exec(select(TagDB)).all()
        for tag_db in existing_tags:
            session.delete(tag_db)

        session.commit()

        # Insert notes again
        for note in notes:
            note_db = NoteDB(
                id=note.id,
                title=note.title,
                content=note.content,
                category=note.category,
                created_at=datetime.fromisoformat(note.created_at)
            )

            tag_objects = []

            for tag_name in note.tags:
                tag_db = session.exec(
                    select(TagDB).where(TagDB.name == tag_name)
                ).first()

                if tag_db is None:
                    tag_db = TagDB(name=tag_name)
                    session.add(tag_db)
                    session.commit()
                    session.refresh(tag_db)

                tag_objects.append(tag_db)

            note_db.tags = tag_objects
            session.add(note_db)

        session.commit()


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
    tag: str = None,
    created_after: str = None,
    created_before: str = None
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
        # Filter by creation date
        if created_after and note.created_at < created_after:
            continue

        if created_before and note.created_at > created_before:
            continue

        filtered_notes.append(note)

    return filtered_notes


@app.get("/notes/stats")
def get_note_stats():
    """
    Get statistics about all notes:
    - total number of notes
    - notes per category
    - top 5 most used tags
    - number of unique tags
    """
    notes_db, _ = load_notes()

    total_notes = len(notes_db)

    category_counter = Counter()
    tag_counter = Counter()

    for note in notes_db:
        # Count categories
        category_counter[note.category] += 1

        # Count tags
        for tag in note.tags:
            tag_counter[tag] += 1

    top_tags = []

    for tag, count in tag_counter.most_common(5):
        top_tags.append({
            "tag": tag,
            "count": count
        })

    return {
        "total_notes": total_notes,
        "by_category": dict(category_counter),
        "top_tags": top_tags,
        "unique_tags_count": len(tag_counter)
    }



@app.get("/categories")
def list_categories() -> list[str]:
    """Get all unique categories from all notes"""
    notes_db, _ = load_notes()

    categories = set()

    for note in notes_db:
        categories.add(note.category)

    return sorted(categories)


@app.get("/categories/{category_name}/notes")
def get_notes_by_category_resource(category_name: str) -> list[Note]:
    """Get all notes in a specific category"""
    notes_db, _ = load_notes()

    filtered_notes = []

    for note in notes_db:
        if note.category == category_name:
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

@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str) -> list[Note]:
    """Get all notes with a specific tag"""
    notes_db, _ = load_notes()

    filtered = []

    for note in notes_db:
        if tag_name in note.tags:
            filtered.append(note)

    return filtered

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


@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate) -> Note:
    """
    Partially update a note.

    PATCH updates only the fields that are provided.
    """
    notes_db, _ = load_notes()

    for i, note in enumerate(notes_db):
        if note.id == note_id:
            if note_update.title is not None:
                note.title = note_update.title

            if note_update.content is not None:
                note.content = note_update.content

            if note_update.category is not None:
                note.category = note_update.category

            if note_update.tags is not None:
                note.tags = note_update.tags

            notes_db[i] = note
            save_notes(notes_db)
            return note

    raise HTTPException(status_code=404, detail="Note not found")



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