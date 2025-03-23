import json
import os
import datetime
from src.utils.file_utils import get_data_file_path

STUDIES_DATA_FILE = get_data_file_path('studies.json')


def load_studies():
    """Load studies data from the JSON file."""
    if os.path.exists(STUDIES_DATA_FILE):
        with open(STUDIES_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_studies(data):
    """Save studies data to the JSON file."""
    with open(STUDIES_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def make_study(name, category):
    """Create a new study."""

    if name is None or category is None:
        print("Error: Name and category are required.")
        return

    studies = load_studies()

    new_id = 1 if not studies else studies[-1]['id'] + 1

    studies.append({
        'id': new_id,
        'name': name,
        'category': category,
        'topics': [],
        'status': 'In Progress',
    })

    save_studies(studies)

    print(
        f"Study '{name}' in category {category} was added successfully with ID {new_id}.")


def change_study(study_id=None, name=None, category=None):
    """Modify an existing study by ID."""
    if study_id is None:
        print("Error: Study ID is required.")
        return

    studies = load_studies()

    for study in studies:
        if study["id"] == study_id:
            if name is not None:
                study["name"] = name
            if category:
                study["category"] = category

            save_studies(studies)

            print(f"Study with ID {study_id} updated successfully.")
            return

    print(f"Error: Study with ID {study_id} not found.")


def delete_study(study_id=None):
    """Delete a study by ID."""
    studies = load_studies()

    if study_id is None:
        print("Error: Study ID is required.")
        return

    for study in studies:
        if study["id"] == study_id:
            studies.remove(study)
            save_studies(studies)
            print(f"Study with ID {study_id} deleted successfully.")
            return

    print(f"Error: Study with ID {study_id} not found.")


def list_studies(study_id=None):
    """
    List all studies.
    Usage: lsstudies [-id <id>]
    """
    studies = load_studies()
    if not studies:
        print("\nNo studies found.")
        return

    if study_id:
        study = next((s for s in studies if s['id'] == study_id), None)
        if study:
            print(f"id: {study['id']} / name: {study['name']} / category: ({study['category']}) / status: {study['status']}")
            if study.get('topics'):
                for topic in study['topics']:
                    print(f"  - {topic['date']}: {topic['name']}")
        else:
            print("Study not found.")
        return

    for study in studies:
        print(f"id: {study['id']} / name: {study['name']} / category: {study['category']} /"
              f" status: {study['status']}")


def mark_study_completed(study_id=None):
    """Mark a study as completed."""
    studies = load_studies()
    for study in studies:
        if study["id"] == study_id:
            if study['status'] == 'Completed':
                print(f"Study with ID {study_id} is already completed.")
                return
            study['status'] = 'Completed'
            save_studies(studies)
            print(f"Study with ID {study_id} marked as completed successfully.")
            return

    print(f"Error: Study with ID {study_id} not found.")


def log_study(study_id=None, name=None, date=None):
    """Log a study topic."""

    studies = load_studies()
    today = datetime.datetime.now().strftime('%d/%m/%Y')

    for study in studies:
        if study["id"] == study_id:
            if name:
                date = date or today
                study["topics"].append({'date': date, 'name': name})
                save_studies(studies)
                print(f"Topic '{name}' logged for study {study_id}.")
                return
            else:
                print("Error: Topic name is required.")
                return

        print("Error: Study not found.")
