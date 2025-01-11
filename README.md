VAT Compliance Retrieval-Augmented Generation (RAG) System
Overview
This project is a VAT Compliance Retrieval-Augmented Generation (RAG) system designed to predict VAT rates and Chart of Account categories for invoices, based on HMRC VAT legislation. The system retrieves relevant legislation, makes predictions using an AI model, and evaluates the accuracy using ROUGE-1 scores.

Key Components
VAT RAG System (vat_rag.py): Retrieves relevant VAT legislation to support predictions.
GL Code Predictor (gl_predictor.py): Predicts VAT rate and accounting category for invoices.
Test Dataset Generator (Test Dataset Generator.py): Creates a test dataset for evaluation.
Test Evaluation Script (Test Evaluation Script.py): Evaluates predictions against the test dataset.
FastAPI API (api.py): Provides endpoints for VAT and category predictions and evaluation.
Features
Prediction and Evaluation: Predicts VAT % and Chart of Account category and evaluates accuracy using ROUGE-1 scores.
MLFlow Integration: Tracks performance metrics for model evaluation.
Scalability: Configurable for handling large invoice datasets.
Setup Instructions
Prerequisites
Python 3.8 or above
A valid OpenAI API key (for language model access)
PostgreSQL (optional, if switching from CSV to database integration)
Installation
Clone the Repository:

bash
Copy code
git clone <repository-url>
cd <repository-folder>
Install Required Packages: Ensure that pip is available, then run:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables:

Create a .env file in the root directory with your OpenAI API key:
bash
Copy code
OPENAI_API_KEY=<your-openai-api-key>
Prepare Data:

Place the VAT legislation data in data/vat_legislation.csv (if using CSV).
If using PostgreSQL, load the vat_legislation table into your database and update the data source in vat_rag.py.
Start the FastAPI Server: Run the server with:

bash
Copy code
uvicorn main:app --reload
Access the API at http://127.0.0.1:8000.

Usage
Prediction Endpoint
Single Prediction:

Use the /predict endpoint with JSON input:
json
Copy code
{
  "data": "<Doc Transcript of Invoice>"
}
Response includes VAT rate prediction, category prediction, and ROUGE-1 score.
Evaluate Predictions:

Use the /evaluate endpoint to compare predictions against known values.
Testing the System
Generate Test Dataset:

Run Test Dataset Generator.py to create sample invoices with VAT rates and categories.
This generates test_dataset.csv for use in evaluation.
Evaluate Predictions:

Use Test Evaluation Script.py to run predictions on the test set and compute performance metrics.
Outputs include average ROUGE scores and accuracy metrics.
Track Model Performance with MLFlow:

Results from prediction accuracy and ROUGE scores are logged in MLFlow, enabling you to track and visualise model performance.
Directory Structure
vat_rag.py: VAT RAG system for document retrieval and query.
gl_predictor.py: General Ledger Code Predictor.
api.py: FastAPI server providing prediction and evaluation endpoints.
Test Dataset Generator.py: Script to create test dataset.
Test Evaluation Script.py: Evaluates model predictions.
requirements.txt: Lists required Python packages.
Contributing
Feel free to open issues or submit pull requests for improvements.

License
This project is licensed under the MIT License.