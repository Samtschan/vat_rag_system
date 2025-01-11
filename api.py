from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import mlflow
from .gl_predictor import GLPredictor
from .vat_rag import VatRag


class InvoiceRequest(BaseModel):
    data: str


class PredictionResponse(BaseModel):
    vat_prediction: Dict[str, Any]
    category_prediction: Dict[str, Any]


app = FastAPI()

# Initialize VAT RAG and GL Predictor
vat_rag = VatRag("data/vat_legislation.csv")
vat_rag.load_documents()
vat_rag.build_index()
predictor = GLPredictor(vat_rag)

"""
Paste in the below /predict thing and ask Claude
How can i use curl in the temirnal to send a test post request to the belwo / above route in fast api? Note it is on 127.0.0.1:8000 

it will give you a command starting with curl that you can paste into a temrinal / command box (in windows)
Make sure the server is runing through main .py first

“<BACKGROUND INFO>
Reformat the below CV into the JSON structure provided beneath it. Above are two examples of how to reformat correctly:
<CV that I want to put in the required client formatting>
“
 
RAG
“<BACKGROUND INFO>
What is the VAT Rate for the UK?”
 
RAG tries to auto construct the background info. 
The issue is that anything automated can fail and go wrong.
And often RAG fails to pick the most relevant background info
To “train” the AI at the top of the prompt.


"""
@app.post("/predict", response_model=PredictionResponse)
async def predict_gl_codes(request: InvoiceRequest):
    """Endpoint to predict VAT rate and Chart of Account category"""
    try:
        # Get predictions
        predictions = predictor.predict(request.data)

        # Log to MLFlow
        with mlflow.start_run():
            mlflow.log_metrics({
                "vat_rouge_score": predictions["vat_prediction"]["rouge_score"],
                "category_rouge_score": predictions["category_prediction"]["rouge_score"]
            })

        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def home():
    return "Hello I'm working! And I'm a bit like Flask aren't I?"

@app.post("/evaluate")
async def evaluate_predictions(data: Dict[str, Dict[str, str]]):
    """Endpoint to evaluate predictions against actual values"""
    try:
        with mlflow.start_run():
            # Calculate accuracy metrics
            vat_match = data["VAT %"]["original"] == data["VAT %"]["prediction"]
            category_match = data["Chart of Account"]["original"] == data["Chart of Account"]["prediction"]

            # Log metrics
            mlflow.log_metrics({
                "vat_accuracy": int(vat_match),
                "category_accuracy": int(category_match),
                "overall_accuracy": (int(vat_match) + int(category_match)) / 2
            })

            return {
                "status": "Success",
                "metrics": {
                    "vat_accuracy": int(vat_match),
                    "category_accuracy": int(category_match)
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))