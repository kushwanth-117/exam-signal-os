# ml/data_prep.py

import pandas as pd

def prepare_training_data(embeddings, labels_df):
    grouped = labels_df.groupby("question_id")["unit_id"].apply(list)

    X = []
    y = []

    for idx, question_id in enumerate(grouped.index):
        X.append(embeddings[idx])
        y.append(grouped.loc[question_id])

    return X, y
