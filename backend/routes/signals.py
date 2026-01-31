from fastapi import APIRouter, Depends

from backend.auth import get_current_user

router = APIRouter(prefix="/signals", tags=["signals"])

@router.get("/")
def get_unit_signals(user_email: str = Depends(get_current_user)):
    # TEMP: safe mock data for deployment
    return {
        "user": user_email,
        "data": [
            {
                "unit_id": "U1",
                "frequency": 1,
                "total_marks": 2,
                "years_active": 1,
            },
            {
                "unit_id": "U2",
                "frequency": 1,
                "total_marks": 1,
                "years_active": 1,
            },
        ]
    }
