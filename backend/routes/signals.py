from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models import UnitSignal, SyllabusUnit

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("/")
def get_unit_signals(
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rows = (
        db.query(UnitSignal, SyllabusUnit)
        .join(SyllabusUnit, UnitSignal.unit_id == SyllabusUnit.unit_id)
        .all()
    )

    return {
        "user": user_email,
        "data": [
            {
                "unit_id": us.unit_id,
                "unit_name": su.unit_name,
                "questions_asked": us.questions_asked,
                "marks_weight": us.marks_weight,
                "years_active": us.years_active,
            }
            for us, su in rows
        ]
    }
