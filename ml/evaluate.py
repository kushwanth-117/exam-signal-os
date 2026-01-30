# ml/evaluate.py

from sklearn.metrics import classification_report
import pandas as pd

def evaluate(model, X, y_true, mlb):
    y_true_bin = mlb.transform(y_true)
    y_pred_bin = model.predict(X)

    report = classification_report(
        y_true_bin,
        y_pred_bin,
        target_names=mlb.classes_,
        zero_division=0,
        output_dict=True
    )

    return pd.DataFrame(report).transpose()
