import os
import json

DATA_FILE = "dados.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def clear_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
