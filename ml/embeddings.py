# ml/embeddings.py

import numpy as np
from sentence_transformers import SentenceTransformer
from ml.config import EMBEDDING_MODEL_NAME

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def encode(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )
        return embeddings
