from fastapi.testclient import TestClient

from main_day_5 import app, TagDB

client = TestClient(app)


def create_valid_note():
    """Helper function to create a valid note for PATCH tests."""
    response = client.post(
        "/notes",
        json={
            "title": "Valid Work Note",
            "content": "This is valid content.",
            "category": "work",
            "tags": ["work", "urgent"],
        },
    )
    assert response.status_code in (200, 201)
    return response.json()


def test_create_note_rejects_short_title():
    response = client.post(
        "/notes",
        json={
            "title": "Hi",
            "content": "This is valid content.",
            "category": "work",
            "tags": ["work"],
        },
    )

    assert response.status_code == 422


def test_create_note_rejects_empty_content():
    response = client.post(
        "/notes",
        json={
            "title": "Valid Title",
            "content": "",
            "category": "work",
            "tags": ["work"],
        },
    )

    assert response.status_code == 422


def test_create_note_rejects_unknown_category():
    response = client.post(
        "/notes",
        json={
            "title": "Valid Title",
            "content": "This is valid content.",
            "category": "holiday",
            "tags": ["holiday"],
        },
    )

    assert response.status_code == 422


def test_create_note_rejects_extra_field():
    response = client.post(
        "/notes",
        json={
            "title": "Valid Title",
            "content": "This is valid content.",
            "category": "work",
            "tags": ["work"],
            "priority": "high",
        },
    )

    assert response.status_code == 422


def test_create_note_rejects_work_category_without_work_tag():
    response = client.post(
        "/notes",
        json={
            "title": "Valid Title",
            "content": "This is valid content.",
            "category": "work",
            "tags": ["urgent"],
        },
    )

    assert response.status_code == 422


def test_create_note_normalizes_category_and_tags():
    response = client.post(
        "/notes",
        json={
            "title": "Valid Title",
            "content": "This is valid content.",
            "category": "WORK",
            "tags": ["work", "Urgent", "urgent"],
        },
    )

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["category"] == "work"
    assert "work" in data["tags"]
    assert "urgent" in data["tags"]
    assert data["tags"].count("urgent") == 1


def test_patch_empty_body_is_allowed():
    note = create_valid_note()

    response = client.patch(
        f"/notes/{note['id']}",
        json={},
    )

    assert response.status_code in (200, 201)

def test_patch_rejects_empty_title():
    note = create_valid_note()

    response = client.patch(
        f"/notes/{note['id']}",
        json={
            "title": "",
        },
    )

    assert response.status_code == 422

def test_tag_name_rejects_uppercase():
    tag = TagDB.model_validate({"name": "Sport"})

    assert tag.name == "sport"
    assert tag.name != "Sport"
    