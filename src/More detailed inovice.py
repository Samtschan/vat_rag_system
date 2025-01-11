import requests

# More detailed test case
test_invoice = """DETAILED VAT INVOICE
Registration Number: GB123456789
Date: 2024-03-15

PROFESSIONAL SERVICES PROVIDED:
1. Management Consulting
   - Strategic Business Analysis
   - Process Optimization
   - Implementation Planning

AMOUNTS:
Professional Fees:          £5,000.00
Materials and Resources:    £1,000.00
                           ---------
Subtotal:                  £6,000.00
VAT (20%):                 £1,200.00
                           ---------
Total Due:                 £7,200.00

Payment Terms: Net 30 days
Service Category: Professional Business Consulting Services
"""

# Make request
response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"data": test_invoice}
)

# Print formatted results
result = response.json()
print("\nPrediction Results:")
print("-" * 50)
print(f"VAT Rate: {result['vat_prediction']['rate']}%")
print(f"VAT Confidence Score: {result['vat_prediction']['rouge_score']:.3f}")
print(f"Category: {result['category_prediction']['category']}")
print(f"Category Confidence Score: {result['category_prediction']['rouge_score']:.3f}")