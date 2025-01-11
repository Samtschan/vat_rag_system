import pandas as pd
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# VAT rates definition
vat_rates = [
    {
        "rate": "20% (VAT on Expenses)",
        "keywords": ["standard rate", "professional services", "consulting"],
        "example_text": "Standard rated supply under UK VAT regulations"
    },
    {
        "rate": "No VAT",
        "keywords": ["exempt", "outside scope", "no vat charged"],
        "example_text": "VAT exempt supply under UK VAT regulations"
    },
    {
        "rate": "Zero Rated Expenses",
        "keywords": ["zero rated", "0%", "export"],
        "example_text": "Zero-rated supply under UK VAT regulations"
    },
    {
        "rate": "Reverse Charge Expenses (20%)",
        "keywords": ["reverse charge", "construction services"],
        "example_text": "Subject to VAT reverse charge"
    }
]

categories = [
    "Computer Equipment",
    "Professional Services",
    "Cost of Goods Sold",
    "Staff Training",
    "Motor Vehicle Expenses"
]


def generate_test_invoice(vat_rate_info, category):
    """Generate test invoice using GPT-4"""
    prompt = f"""Generate a UK invoice with random but reasonable and consistent numeric values
                for a company involved in {category}. 
                The invoice must clearly show it follows the VAT rate: {vat_rate_info['rate']}.

                Include:
                1. Company details with VAT number
                2. Clear line items
                3. Explicit VAT treatment
                4. Appropriate calculations
                5. Category-specific services/products

                Keywords to include: {', '.join(vat_rate_info['keywords'])}
                VAT Context: {vat_rate_info['example_text']}

                Format it as a proper UK invoice."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating invoice: {e}")
        # Fallback to template
        base_amount = 1000.00
        vat_amount = base_amount * 0.20 if "20%" in vat_rate_info["rate"] else 0
        total = base_amount + vat_amount

        return f"""VAT INVOICE
VAT Registration Number: GB123456789
Invoice Reference: TEST-{category[:3]}-{vat_rate_info['rate'][:3]}

DESCRIPTION:
Professional services related to {category}
{vat_rate_info['example_text']}
{' '.join(vat_rate_info['keywords'])}

Amount (excl. VAT): £{base_amount:.2f}
VAT Treatment: {vat_rate_info['rate']}
VAT Amount: £{vat_amount:.2f}
Total Amount: £{total:.2f}

Payment Terms: 30 days
VAT Information: {vat_rate_info['example_text']}"""


def main():
    # Create test dataset
    test_data = []
    total_combinations = len(vat_rates) * len(categories)
    current = 0

    # Generate combinations of VAT rates and categories
    for vat_rate_info in vat_rates:
        for category in categories:
            current += 1
            print(f"Generating invoice {current}/{total_combinations}...")

            invoice_text = generate_test_invoice(vat_rate_info, category)
            test_data.append({
                "invoice_text": invoice_text,
                "vat_rate": vat_rate_info["rate"],
                "category": category
            })

    # Create DataFrame and save
    df = pd.DataFrame(test_data)
    df.to_csv('test_dataset.csv', index=False)

    print("\nGenerated test dataset with:")
    print(f"Number of test cases: {len(df)}")
    print("\nVAT Rates used:")
    for rate in vat_rates:
        print(f"- {rate['rate']}")
    print("\nExample invoice:")
    print(df['invoice_text'].iloc[0])


if __name__ == "__main__":
    main()