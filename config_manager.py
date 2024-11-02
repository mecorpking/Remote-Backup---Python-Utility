import json
import os

CONFIG_FILE = 'config.json'

def save_config(data):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}