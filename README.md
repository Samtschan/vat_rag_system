
# VAT Compliance Retrieval-Augmented Generation (RAG) System

## Overview
This project is a VAT Compliance Retrieval-Augmented Generation (RAG) system designed to predict VAT rates and Chart of Account categories for invoices based on HMRC VAT legislation. The system retrieves relevant legislation, makes predictions using an AI model, and evaluates accuracy using ROUGE-1 scores.

## Key Components
- **VAT RAG System (`vat_rag.py`)**: Retrieves relevant VAT legislation to support predictions.
- **GL Code Predictor (`gl_predictor.py`)**: Predicts VAT rate and accounting category for invoices.
- **Test Dataset Generator (`Test Dataset Generator.py`)**: Creates a test dataset for evaluation.
- **Test Evaluation Script (`Test Evaluation Script.py`)**: Evaluates predictions against the test dataset.
- **FastAPI API (`api.py`)**: Provides endpoints for VAT and category predictions and evaluation.

## Features
- **Prediction and Evaluation**: Predicts VAT % and Chart of Account category and evaluates accuracy using ROUGE-1 scores.
- **MLFlow Integration**: Tracks performance metrics for model evaluation.
- **Scalability**: Configurable for handling large invoice datasets.

## Setup Instructions

### Prerequisites
- Python 3.8 or above
- A valid OpenAI API key (for language model access)
- PostgreSQL (optional, if switching from CSV to database integration)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory with your OpenAI API key:
     ```plaintext
     OPENAI_API_KEY=<your-openai-api-key>
     ```

4. **Prepare Data**:
   - Place the VAT legislation data in `data/vat_legislation.csv` (if using CSV).
   - If using PostgreSQL, load the `vat_legislation` table into your database and update the data source in `vat_rag.py`.

5. **Start the FastAPI Server**:
   - Run the server using `main.py`:
     ```bash
     python main.py
     ```
   - Access the API at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Usage

### Prediction Endpoint
1. **Single Prediction**:
   - Use the `/predict` endpoint with JSON input:
     ```json
     {
       "data": "<Doc Transcript of Invoice>"
     }
     ```
   - Response includes VAT rate prediction, category prediction, and ROUGE-1 score.

2. **Evaluate Predictions**:
   - Use the `/evaluate` endpoint to compare predictions against known values.

### Testing a Single Prediction
To test the prediction endpoint with a sample invoice, use `single_example_test.py`:
```bash
python single_example_test.py
```
This script sends a sample invoice to the `/predict` endpoint and prints the prediction results.

### Testing the System
1. **Generate Test Dataset**:
   - Run `Test Dataset Generator.py` to create sample invoices with VAT rates and categories, generating `test_dataset.csv` for use in evaluation.

2. **Evaluate Predictions**:
   - Use `Test Evaluation Script.py` to run predictions on the test set and compute performance metrics. Outputs include average ROUGE scores and accuracy metrics.

3. **Track Model Performance with MLFlow**:
   - Results from prediction accuracy and ROUGE scores are logged in MLFlow, enabling you to track and visualize model performance.

## Directory Structure
- `vat_rag.py`: VAT RAG system for document retrieval and query.
- `gl_predictor.py`: General Ledger Code Predictor.
- `api.py`: FastAPI server providing prediction and evaluation endpoints.
- `main.py`: Starts the FastAPI server.
- `single_example_test.py`: Sends a single test prediction request to the `/predict` endpoint.
- `Test Dataset Generator.py`: Script to create test dataset.
- `Test Evaluation Script.py`: Evaluates model predictions.
- `requirements.txt`: Lists required Python packages.

## Contributing
Feel free to open issues or submit pull requests for improvements.

## License
This project is licensed under the MIT License.

## Demo Video
The demo video is available in the repository: [VAT RAG Demo.zip](VAT%20RAG%20Demo.zip)


---
