import json
import uuid


def load_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Input file '{file_path}' not found. Please provide a valid file.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{file_path}': {e}")
        exit(1)


def generate_uuid():
    return str(uuid.uuid4())
