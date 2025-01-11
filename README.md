# VAT Compliance Retrieval-Augmented Generation (RAG) System

## Overview
This project is a VAT Compliance Retrieval-Augmented Generation (RAG) system designed to predict VAT rates and Chart of Account categories for invoices based on HMRC VAT legislation. The system retrieves relevant legislation, makes predictions using an AI model, and evaluates accuracy using ROUGE-1 scores.

## Key Components
- **VAT RAG System (`vat_rag.py`)**: Retrieves relevant VAT legislation to support predictions
- **GL Code Predictor (`gl_predictor.py`)**: Predicts VAT rate and accounting category for invoices
- **Test Dataset Generator (`Test Dataset Generator.py`)**: Creates a test dataset for evaluation
- **Test Evaluation Script (`Test Evaluation Script.py`)**: Evaluates predictions against the test dataset
- **FastAPI API (`api.py`)**: Provides endpoints for VAT and category predictions and evaluation

## Features
- **Prediction and Evaluation**: 
  - VAT rate classification with ~0.75 ROUGE score
  - Chart of Account categorization with ~0.75 ROUGE score
  - Performance evaluation using ROUGE-1 metrics
- **MLFlow Integration**: Tracks performance metrics including:
  - ROUGE scores for predictions
  - Accuracy metrics
  - Error analysis
- **Scalability**: 
  - Configurable for handling large invoice datasets
  - Caching for improved performance
  - Batch processing capabilities

## Prerequisites
- Python 3.8 or above
- A valid OpenAI API key (for language model access)
- PostgreSQL (optional, if switching from CSV to database integration)
- Sufficient disk space for MLFlow tracking

## Installation

1. **Clone the Repository**:
```bash
git clone <repository-url>
cd vat-rag-project
```

2. **Create and Activate Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**:
Create a `.env` file in the root directory:
```plaintext
OPENAI_API_KEY=your_api_key_here
```

5. **Prepare Data**:
- Place VAT legislation data in `data/vat_legislation.csv`
- For PostgreSQL:
  - Load the `vat_legislation` table
  - Update connection settings in `vat_rag.py`

## Project Structure
```
vat-rag-project/
├── data/
│   └── vat_legislation.csv
├── src/
│   ├── api.py               # FastAPI endpoints
│   ├── gl_predictor.py      # Prediction logic
│   ├── vat_rag.py          # RAG implementation
│   └── main.py             # Server startup
├── tests/
│   ├── test_dataset.csv
│   ├── Test Dataset Generator.py
│   └── Test Evaluation Script.py
├── .env
├── requirements.txt
└── README.md
```

## Usage

### Starting the Server
1. Start the FastAPI server:
```bash
python src/main.py
```
2. Access the API at `http://127.0.0.1:8000`

### API Endpoints

1. **Prediction Endpoint**:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"data": "your invoice text here"}'
```

2. **Evaluation Endpoint**:
```bash
curl -X POST "http://127.0.0.1:8000/evaluate" \
     -H "Content-Type: application/json" \
     -d '{
           "VAT %": {
             "original": "20% (VAT on Expenses)",
             "prediction": "20% (VAT on Expenses)"
           },
           "Chart of Account": {
             "original": "Professional Services",
             "prediction": "Professional Services"
           }
         }'
```

### Running Tests

1. **Generate Test Dataset**:
```bash
python tests/Test\ Dataset\ Generator.py
```

2. **Run Evaluation**:
```bash
python tests/Test\ Evaluation\ Script.py
```

### MLFlow Tracking

1. Access MLFlow UI:
```bash
mlflow ui
```
2. View metrics at `http://localhost:5000`

## Performance Metrics

Current system performance:
- VAT Prediction:
  - ROUGE Score: ~0.75
  - Accuracy: ~80%
- Category Prediction:
  - ROUGE Score: ~0.75
  - Accuracy: ~70%

## Troubleshooting

Common issues and solutions:
1. **OpenAI API Issues**:
   - Check API key in `.env`
   - Verify API quota
   
2. **Server Connection**:
   - Confirm port 8000 is available
   - Check firewall settings

3. **Performance Issues**:
   - Adjust batch sizes
   - Check memory usage
   - Monitor API rate limits

## License
This project is licensed under the MIT License.