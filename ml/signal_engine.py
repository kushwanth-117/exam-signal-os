# ml/signal_engine.py

import pandas as pd

def compute_unit_signals(questions_df):
    grouped = questions_df.groupby("unit_id")

    signals = []

    for unit, g in grouped:
        signals.append({
            "unit_id": unit,
            "frequency": len(g),
            "total_marks": g["marks"].sum(),
            "years_active": g["year"].nunique()
        })

    return pd.DataFrame(signals)
