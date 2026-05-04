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


def test_filter_by_category():
    """Test filtering notes by category."""
    note_data = make_note_data()
    note_data["category"] = f"FilterCategory-{uuid4().hex[:8]}"

    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    assert create_response.status_code == 201
    created_note = create_response.json()

    response = requests.get(
        f"{BASE_URL}/notes",
        params={"category": note_data["category"]}
    )

    assert response.status_code == 200

    notes = response.json()
    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert note["category"] == note_data["category"]


def test_filter_by_search():
    """Test filtering notes by search text."""
    unique_word = f"SearchWord-{uuid4().hex[:8]}"

    note_data = make_note_data()
    note_data["title"] = f"Search Test {unique_word}"
    note_data["content"] = f"This content contains {unique_word}"

    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    assert create_response.status_code == 201
    created_note = create_response.json()

    response = requests.get(
        f"{BASE_URL}/notes",
        params={"search": unique_word}
    )

    assert response.status_code == 200

    notes = response.json()
    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids


def test_filter_by_tag():
    """Test filtering notes by tag."""
    unique_tag = f"tag-{uuid4().hex[:8]}"

    note_data = make_note_data()
    note_data["tags"] = [unique_tag, "filter-test"]

    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    assert create_response.status_code == 201
    created_note = create_response.json()

    response = requests.get(
        f"{BASE_URL}/notes",
        params={"tag": unique_tag}
    )

    assert response.status_code == 200

    notes = response.json()
    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert unique_tag in note["tags"]


def test_combined_filters():
    """Test using category, search, and tag filter together."""
    unique_id = uuid4().hex[:8]
    unique_category = f"CombinedCategory-{unique_id}"
    unique_tag = f"combined-tag-{unique_id}"
    unique_word = f"CombinedSearch-{unique_id}"

    note_data = {
        "title": f"Combined Filter Test {unique_word}",
        "content": f"This note is used for combined filter test {unique_word}",
        "category": unique_category,
        "tags": [unique_tag, "combined"]
    }

    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    assert create_response.status_code == 201
    created_note = create_response.json()

    response = requests.get(
        f"{BASE_URL}/notes",
        params={
            "category": unique_category,
            "search": unique_word,
            "tag": unique_tag
        }
    )

    assert response.status_code == 200

    notes = response.json()
    note_ids = [note["id"] for note in notes]

    assert created_note["id"] in note_ids

    for note in notes:
        assert note["category"] == unique_category
        assert unique_tag in note["tags"]
        assert unique_word in note["title"] or unique_word in note["content"]


def test_create_note_missing_field():
    """Test creating a note with missing required fields."""
    invalid_note = {
        "title": "Invalid Test Note"
        # content and category are missing
    }

    response = requests.post(f"{BASE_URL}/notes", json=invalid_note)

    assert response.status_code == 422


def test_get_nonexistent_note():
    """Test getting a note that does not exist."""
    response = requests.get(f"{BASE_URL}/notes/999999999")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_update_nonexistent_note():
    """Test updating a note that does not exist."""
    updated_data = {
        "title": "Updated nonexistent note",
        "content": "This note should not exist",
        "category": "Error Test",
        "tags": ["error", "put"]
    }

    response = requests.put(f"{BASE_URL}/notes/999999999", json=updated_data)

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_nonexistent_note():
    """Test deleting a note that does not exist."""
    response = requests.delete(f"{BASE_URL}/notes/999999999")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_notes_statistics():
    """Test getting note statistics."""
    response = requests.get(f"{BASE_URL}/notes/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total_notes" in data
    assert "by_category" in data
    assert "top_tags" in data
    assert "unique_tags_count" in data

    assert isinstance(data["total_notes"], int)
    assert isinstance(data["by_category"], dict)
    assert isinstance(data["top_tags"], list)
    assert isinstance(data["unique_tags_count"], int)

    assert data["total_notes"] >= 0
    assert data["unique_tags_count"] >= 0

    if data["top_tags"]:
        first_tag = data["top_tags"][0]
        assert "tag" in first_tag
        assert "count" in first_tag
        assert isinstance(first_tag["tag"], str)
        assert isinstance(first_tag["count"], int)


def test_patch_note():
    """Test partially updating a note with PATCH."""
    created_note = create_test_note()
    note_id = created_note["id"]

    patch_data = {
        "title": "Patched Test Title"
    }

    response = requests.patch(f"{BASE_URL}/notes/{note_id}", json=patch_data)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note_id
    assert data["title"] == patch_data["title"]

    # These fields should stay unchanged because PATCH only updates selected fields
    assert data["content"] == created_note["content"]
    assert data["category"] == created_note["category"]
    assert set(data["tags"]) == set(created_note["tags"])

