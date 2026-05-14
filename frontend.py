import streamlit as st
import requests

NO_API_URL = "https://naas.isalman.dev/no"
API_BASE_URL = "http://127.0.0.1:8000"
NOTES_API_URL = f"{API_BASE_URL}/notes"
CATEGORIES_API_URL = f"{API_BASE_URL}/categories"


def load_notes():
    response = requests.get(NOTES_API_URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "notes" in data:
        return data["notes"]

    return []


def load_categories():
    response = requests.get(CATEGORIES_API_URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "categories" in data:
        return data["categories"]

    return []


def create_note(title, content, category, tags):
    note_data = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
    }

    response = requests.post(NOTES_API_URL, json=note_data, timeout=10)
    response.raise_for_status()
    return response.json()


st.title("Day 7 - Streamlit Frontend")

tab_no, tab_notes = st.tabs(["Say no App", "Notes API"])


with tab_no:
    st.header("Say no App")
    st.write("Click the button to ask the No-as-a-Service API for a response.")

    if st.button("Say no"):
        try:
            response = requests.get(NO_API_URL, timeout=10)
            response.raise_for_status()

            try:
                data = response.json()
                st.success("API request was successful.")
                st.json(data)
            except ValueError:
                st.success("API request was successful.")
                st.write(response.text)

        except requests.RequestException as error:
            st.error("API request failed.")
            st.write(error)


with tab_notes:
    st.header("Notes API")

    categories = ["general", "ideas", "personal", "school", "work"]

    st.subheader("Create a new note")

    with st.form("create_note_form"):
        title = st.text_input("Title")
        content = st.text_area("Content")

        category = st.selectbox("Category", categories)

        tags_input = st.text_input("Tags", placeholder="Example: sport, plan, study")

        submitted = st.form_submit_button("Create note")

        if submitted:
            tags = [
                tag.strip()
                for tag in tags_input.split(",")
                if tag.strip()
            ]

            if not title.strip():
                st.error("Title is required.")
            elif not content.strip():
                st.error("Content is required.")
            else:
                try:
                    created_note = create_note(
                        title=title.strip(),
                        content=content.strip(),
                        category=category,
                        tags=tags,
                    )
                    st.success("New note was created successfully.")
                    st.json(created_note)

                except requests.HTTPError as error:
                    st.error("The backend rejected the new note.")
                    st.write(error.response.text)

                except requests.RequestException as error:
                    st.error("Could not send the new note to the backend.")
                    st.write(error)

    st.divider()

    st.subheader("All Notes")
    st.write("This section loads all notes from the FastAPI backend.")

    if st.button("Reload notes"):
        st.rerun()

    try:
        notes = load_notes()

        if not notes:
            st.info("No notes found.")
        else:
            note_options = []

            for note in notes:
                note_id = note.get("id", "no id")
                note_title = note.get("title", "No title")
                note_options.append(f"{note_id} - {note_title}")

            selected_option = st.selectbox(
                "Choose a note title:",
                note_options
            )

            selected_index = note_options.index(selected_option)
            selected_note = notes[selected_index]

            st.subheader(selected_note.get("title", "No title"))

            st.write("Content:")
            st.text(selected_note.get("content", ""))

            st.write("Category:")
            st.write(selected_note.get("category", "-"))

            st.write("Tags:")
            selected_tags = selected_note.get("tags", [])

            if isinstance(selected_tags, list):
                st.write(", ".join(selected_tags))
            else:
                st.write(selected_tags)

            with st.expander("Show full note data"):
                st.json(selected_note)

    except requests.RequestException as error:
        st.error("Could not load notes from the FastAPI backend.")
        st.write(error)
