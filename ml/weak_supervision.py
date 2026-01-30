# ml/weak_supervision.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ml.config import SIMILARITY_TOP_K, SIMILARITY_THRESHOLD

def weak_label_questions(
    question_embeddings: np.ndarray,
    unit_embeddings: np.ndarray,
    unit_ids: list[str]
):
    similarity_matrix = cosine_similarity(
        question_embeddings,
        unit_embeddings
    )

    weak_labels = []

    for q_idx, similarities in enumerate(similarity_matrix):
        top_indices = similarities.argsort()[-SIMILARITY_TOP_K:][::-1]

        for idx in top_indices:
            if similarities[idx] >= SIMILARITY_THRESHOLD:
                weak_labels.append({
                    "question_index": q_idx,
                    "unit_id": unit_ids[idx],
                    "confidence": float(similarities[idx]),
                    "source": "weak"
                })

    return weak_labels
