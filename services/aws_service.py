import boto3
    region_name=AWS_REGION,
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

# Table

table = dynamodb.Table("AyushCareVitals")

# SNS Client

sns_client = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

ALERT_PHONE = "+91XXXXXXXXXX"


def save_to_dynamodb(patient_id, vitals):

    try:
        table.put_item(
            Item={
                "patient_id": patient_id,
                "timestamp": datetime.now().isoformat(),
                "temperature": Decimal(str(vitals["temperature"])),
                "heart_rate": Decimal(str(vitals["heart_rate"])),
                "spo2": Decimal(str(vitals["spo2"])),
                "bp": vitals["bp"],
                "respiratory_rate": Decimal(str(vitals["respiratory_rate"]))
            }
        )

        save_history(patient_id, vitals)

    except Exception as e:
        st.warning(f"AWS Upload Failed: {e}")


def send_emergency_alert(message):

    try:
        sns_client.publish(
            PhoneNumber=ALERT_PHONE,
            Message=message
        )

    except Exception as e:
        st.warning(f"SNS Alert Failed: {e}")
