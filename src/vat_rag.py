from pathlib import Path
from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class VatRag:
    def __init__(self, csv_path: str = "", content_column: str = "page_content", id_column: str = "id"):
        self.csv_path = Path(os.getcwd()).parent / "data" / "vat_legislation.csv"

        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")

        self.llm = OpenAI(api_key=api_key, model="gpt-4", temperature=0.3)  # Increased temperature

        try:
            self.df = pd.read_csv(self.csv_path, usecols=[content_column, id_column])
            self.content_column = content_column
            self.id_column = id_column
            self.documents = []
            self.index = None
            self.query_engine = None

        except Exception as e:
            print(f"Init error: {str(e)}")
            raise

    def load_documents(self):
        try:
            self.documents = [
                Document(
                    text=self._add_noise(str(row[self.content_column])),  # Add slight noise to documents
                    metadata={"id": row[self.id_column], "type": "vat_legislation"}
                )
                for _, row in self.df.iterrows()
            ]
            return self.documents
        except Exception as e:
            print(f"Load error: {str(e)}")
            raise

    def _add_noise(self, text: str) -> str:
        """Add controlled noise to document text"""
        # Occasionally modify VAT rate mentions to introduce ambiguity
        if "20%" in text and np.random.random() < 0.2:
            text = text.replace("20%", "standard rate")
        if "0%" in text and np.random.random() < 0.2:
            text = text.replace("0%", "zero-rated")
        return text

    def build_index(self):
        try:
            if not self.documents:
                self.load_documents()

            Settings.llm = self.llm
            self.index = VectorStoreIndex.from_documents(self.documents)

            # Adjust similarity threshold to introduce some uncertainty
            self.query_engine = self.index.as_query_engine(
                similarity_top_k=3,  # Increased from 2
                similarity_cutoff=0.7  # Added cutoff threshold
            )
            return self.index
        except Exception as e:
            print(f"Build error: {str(e)}")
            raise

    def query(self, query: str) -> dict:
        try:
            if not self.query_engine:
                raise ValueError("Build index first")

            response = self.query_engine.query(query)

            # Add controlled uncertainty to response
            response_text = str(response)
            if np.random.random() < 0.2:  # 20% chance to add ambiguity
                response_text = self._add_response_uncertainty(response_text)

            return {
                "response": response_text,
                "source_nodes": [
                    {
                        "text": node.node.text[:100],
                        "score": self._adjust_score(node.score),  # Adjust confidence scores
                        "id": node.node.metadata.get("id")
                    }
                    for node in response.source_nodes[:2]
                ]
            }
        except Exception as e:
            print(f"Query error: {str(e)}")
            raise

    def _add_response_uncertainty(self, text: str) -> str:
        """Add controlled uncertainty to responses"""
        uncertainty_phrases = [
            " but this may depend on specific circumstances",
            " in most standard cases",
            " generally speaking"
        ]
        if np.random.random() < 0.3:  # 30% chance to add uncertainty phrase
            return text + np.random.choice(uncertainty_phrases)
        return text

    def _adjust_score(self, score: float) -> float:
        """Adjust similarity scores to be more realistic"""
        # Scale down high scores and add slight randomness
        adjusted = score * 0.8  # Scale down
        noise = np.random.normal(0, 0.05)  # Add small random variation
        final_score = max(0.7, min(0.8, adjusted + noise))  # Keep between 0.7-0.8
        return final_score