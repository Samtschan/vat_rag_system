import requests
import json

# Test predict endpoint
response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"data": "Invoice for IT consulting services\nAmount: £1,000\nDescription: Technical consulting for cloud migration\nDate: 2024-03-15"}
)
print(response.json())