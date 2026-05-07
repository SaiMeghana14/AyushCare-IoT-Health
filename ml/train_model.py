from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd

data = pd.DataFrame({

    "spo2": [98, 97, 85, 88, 99],
    "heart_rate": [75, 82, 120, 110, 70],
    "temperature": [36.8, 37.1, 39.5, 38.9, 36.5],

    "risk": [
        "Low",
        "Low",
        "Critical",
        "Moderate",
        "Low"
    ]
})

X = data[
    ["spo2", "heart_rate", "temperature"]
]

y = data["risk"]

model = RandomForestClassifier()

model.fit(X, y)

joblib.dump(model, "health_model.pkl")
