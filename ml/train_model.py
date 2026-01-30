# ml/train_model.py

import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer

def train_multilabel_model(X, y_labels):
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y_labels)

    model = OneVsRestClassifier(
        LogisticRegression(max_iter=1000)
    )

    model.fit(X, y)

    return model, mlb
