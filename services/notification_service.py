import json
import os
from datetime import datetime

NOTIFICATION_FILE = "notifications.json"


def save_alert(patient_id, severity, message):

    alerts = []

    if os.path.exists(NOTIFICATION_FILE):

        with open(NOTIFICATION_FILE, "r") as f:
            alerts = json.load(f)

    alerts.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "patient_id": patient_id,
        "severity": severity,
        "message": message
    })

    with open(NOTIFICATION_FILE, "w") as f:
        json.dump(alerts, f, indent=4)
