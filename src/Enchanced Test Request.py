import requests
import json


def test_prediction(invoice_text: str) -> None:
    """Test prediction endpoint with given invoice text"""
    url = "http://127.0.0.1:8000/predict"

    # Prepare request data
    payload = {"data": invoice_text}

    # Make request
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for bad status codes

        # Format and print results
        result = response.json()
        print("\nInvoice Text:")
        print("-" * 50)
        print(invoice_text)
        print("\nPrediction Results:")
        print("-" * 50)
        print(f"VAT Rate: {result['vat_prediction']['rate']}%")
        print(f"VAT Confidence Score: {result['vat_prediction']['rouge_score']:.3f}")
        print(f"Category: {result['category_prediction']['category']}")
        print(f"Category Confidence Score: {result['category_prediction']['rouge_score']:.3f}")
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")


# Test cases with more detailed invoice descriptions
test_cases = [
    """INVOICE
Date: 2024-03-15
Service: Professional IT Consulting Services
Description: Strategic technical consulting for enterprise cloud migration project
Including:
- Architecture design and planning
- Security assessment
- Performance optimization
Amount: £5,000.00
Payment Terms: Net 30""",

    """INVOICE
Date: 2024-03-15
Service: Business Advisory Services
Project: Financial Systems Implementation
Scope:
- Requirements analysis
- System configuration
- Staff training and support
Professional Fee: £3,500
Travel Expenses: £500
Total Amount: £4,000""",

    """INVOICE
Date: 2024-03-15
Professional Services Rendered:
1. Management Consulting
   - Strategic planning sessions
   - Business process optimization
2. Implementation Support
   - Project management
   - Quality assurance
Rate: £1,200 per day
Days: 5
Total Amount: £6,000""",

    """INVOICE
Type: Consulting Services Invoice
Date: 2024-03-15
Client: ABC Corporation
Service Details:
- Technical Architecture Review
- Cloud Migration Strategy
- Security Assessment
- Performance Optimization
Hours Worked: 40
Rate per Hour: £150
Total Professional Fees: £6,000"""
]

# Test each case
for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest Case {i}")
    test_prediction(test_case)