import os
import json


def read_json_file(path):
    try:
        with open(path, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found → {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON in {path} → {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def write_json_file(path, data, indent=4):
    try:
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=indent)
        return True
    except Exception as e:
        print(f"Error writing JSON to {path} → {e}")
        return False



def read_file(path):
    data=""
    if os.path.isfile(path):
        with open(path, 'r') as file:
            data = file.read()
    else:
        with open(path, 'w') as file:
            file.write('0')
        data = '0'
    return data


def write_data(path, data):
    with open(path, 'w') as file:
        file.write(str(data))
