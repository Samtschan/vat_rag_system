import uvicorn
import mlflow
from pathlib import Path

# Configure MLFlow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("vat-predictions")

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
    """Note server address seems best as 127.0.0.1:8000"""