import requests
from uuid import uuid4

BASE_URL = "http://127.0.0.1:8000"


def make_note_data():
    """Create unique test data for each test."""
    unique_id = uuid4().hex[:8]

    return {
        "title": f"Test Note {unique_id}",
        "content": f"Test content {unique_id}",
        "category": f"Testing {unique_id}",
        "tags": ["test", unique_id]
    }


def create_test_note():
    """Helper function to create a note for tests."""
    note_data = make_note_data()
    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201

    return response.json()


def test_create_note():
    """Test creating a new note."""
    note_data = make_note_data()

    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert data["title"] == note_data["title"]
    assert data["content"] == note_data["content"]
    assert data["category"] == note_data["category"]
    assert data["tags"] == note_data["tags"]


def test_list_notes():
    """Test listing all notes."""
    response = requests.get(f"{BASE_URL}/notes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_note_by_id():
    """Test getting one specific note by id."""
    created_note = create_test_note()
    note_id = created_note["id"]

    response = requests.get(f"{BASE_URL}/notes/{note_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == created_note["title"]
    assert data["content"] == created_note["content"]


def test_update_note():
    """Test updating a note with PUT."""
    created_note = create_test_note()
    note_id = created_note["id"]

    updated_data = {
        "title": "Updated Test Title",
        "content": "Updated test content",
        "category": "Updated Category",
        "tags": ["updated", "put"]
    }

    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == updated_data["title"]
    assert data["content"] == updated_data["content"]
    assert data["category"] == updated_data["category"]
    assert set(data["tags"]) == set(updated_data["tags"])


def test_delete_note():
    """Test deleting a note."""
    created_note = create_test_note()
    note_id = created_note["id"]

    response = requests.delete(f"{BASE_URL}/notes/{note_id}")

    assert response.status_code in [200, 204]

    get_response = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert get_response.status_code == 404