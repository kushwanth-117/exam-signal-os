# ml/label_utils.py

import pandas as pd

def merge_manual_and_weak_labels(
    questions_df,
    weak_labels,
    manual_labels_df
):
    # ---- Manual labels (always trusted) ----
    manual_df = manual_labels_df.copy()
    manual_df["confidence"] = 1.0
    manual_df["source"] = "manual"

    # ---- Handle weak labels safely ----
    if weak_labels and len(weak_labels) > 0:
        weak_df = pd.DataFrame(weak_labels)

        # Only proceed if expected column exists
        if "question_index" in weak_df.columns:
            weak_df["question_id"] = weak_df["question_index"].apply(
                lambda i: questions_df.iloc[i]["question_id"]
            )

            weak_df = weak_df[["question_id", "unit_id", "confidence", "source"]]
        else:
            weak_df = pd.DataFrame(columns=["question_id", "unit_id", "confidence", "source"])
    else:
        weak_df = pd.DataFrame(columns=["question_id", "unit_id", "confidence", "source"])

    # ---- Merge (manual overrides weak) ----
    final_labels = pd.concat(
        [manual_df, weak_df],
        ignore_index=True
    )

    final_labels = final_labels.drop_duplicates(
        subset=["question_id", "unit_id"],
        keep="first"
    )

    return final_labels
