from fastapi import APIRouter, Depends
import pandas as pd

from backend.auth import get_current_user

router = APIRouter(prefix="/signals")

@router.get("/")
def get_unit_signals(
    user_email: str = Depends(get_current_user)
):
    df = pd.read_csv("data/processed/unit_signals.csv")

    return {
        "user": user_email,
        "data": df.to_dict(orient="records")
    }
