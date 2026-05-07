import joblib
import pandas as pd

model = joblib.load("health_model.pkl")


def predict_risk(vitals):

    df = pd.DataFrame([{
        "spo2": vitals["spo2"],
        "heart_rate": vitals["heart_rate"],
        "temperature": vitals["temperature"]
    }])

    prediction = model.predict(df)[0]

    return prediction
