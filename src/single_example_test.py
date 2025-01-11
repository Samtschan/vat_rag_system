import requests

url = "http://127.0.0.1:8000/predict"
data = {"data": "Sample invoice text for consulting services with 20% VAT"}

response = requests.post(url, json=data)
print("Prediction Results:", response.json())
