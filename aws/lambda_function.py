import json
import boto3
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("AyushCareVitals")


def lambda_handler(event, context):

    payload = json.loads(event["Records"][0]["Sns"]["Message"])

    table.put_item(
        Item={
            "patient_id": payload["patient_id"],
            "timestamp": datetime.now().isoformat(),
            "heart_rate": Decimal(str(payload["heart_rate"])),
            "spo2": Decimal(str(payload["spo2"])),
            "temperature": Decimal(str(payload["temperature"]))
        }
    )

    return {
        "statusCode": 200
    }
