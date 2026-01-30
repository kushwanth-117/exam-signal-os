# scripts/run_pipeline.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np

from ml.preprocess import clean_text
from ml.embeddings import EmbeddingGenerator
from ml.weak_supervision import weak_label_questions
from ml.label_utils import merge_manual_and_weak_labels
from ml.data_prep import prepare_training_data
from ml.train_model import train_multilabel_model
from ml.signal_engine import compute_unit_signals
from ml.evaluate import evaluate


# ---------- LOAD DATA ----------
questions_df = pd.read_csv("data/processed/questions.csv")
units_df = pd.read_csv("data/processed/syllabus_units.csv")
manual_labels_df = pd.read_csv("data/labels/manual_labels.csv")

# ---------- CLEAN TEXT ----------
questions_df["clean_text"] = questions_df["question_text"].apply(clean_text)
units_df["clean_text"] = units_df["unit_description"].apply(clean_text)

# ---------- EMBEDDINGS ----------
embedder = EmbeddingGenerator()

question_embeddings = embedder.encode(
    questions_df["clean_text"].tolist()
)

unit_embeddings = embedder.encode(
    units_df["clean_text"].tolist()
)

# ---------- WEAK SUPERVISION ----------
weak_labels = weak_label_questions(
    question_embeddings,
    unit_embeddings,
    units_df["unit_id"].tolist()
)

# ---------- MERGE LABELS ----------
final_labels = merge_manual_and_weak_labels(
    questions_df,
    weak_labels,
    manual_labels_df
)

# ---------- TRAIN ----------
X, y = prepare_training_data(question_embeddings, final_labels)

model, mlb = train_multilabel_model(X, y)

# ---------- EVALUATION ----------
eval_df = evaluate(
    model=model,
    X=X,
    y_true=y,
    mlb=mlb
)

eval_df.to_csv(
    "data/processed/evaluation_report.csv",
    index=True
)

print("📊 Evaluation report saved to data/processed/evaluation_report.csv")


# ---------- PREDICT ALL ----------
predictions = model.predict(question_embeddings)
predicted_units = mlb.inverse_transform(predictions)

# ---------- ATTACH PREDICTIONS (STRING SAFE) ----------
questions_df["predicted_units"] = [
    ",".join(units) if len(units) > 0 else ""
    for units in predicted_units
]

# ---------- SAVE FOR DASHBOARD ----------
questions_df.to_csv(
    "data/processed/questions_with_predictions.csv",
    index=False
)


print("Sample predictions:")
print(questions_df[["question_text", "predicted_units"]].head(5))


# ---------- SIGNAL ENGINE ----------
exploded = questions_df.explode("predicted_units")
exploded = exploded.rename(columns={"predicted_units": "unit_id"})

signals_df = compute_unit_signals(exploded)

signals_df.to_csv("data/processed/unit_signals.csv", index=False)

print("✅ Pipeline completed successfully")

