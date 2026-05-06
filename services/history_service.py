import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"


def load_history():

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)

    return {}


def save_history(patient_id, vitals):

    history = load_history()

    if patient_id not in history:
        history[patient_id] = []

    history[patient_id].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "temperature": vitals["temperature"],
        "heart_rate": vitals["heart_rate"],
        "spo2": vitals["spo2"]
    })

    history[patient_id] = history[patient_id][-15:]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
