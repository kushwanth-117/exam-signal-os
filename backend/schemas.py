from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UnitSignalOut(BaseModel):
    unit_id: str
    unit_name: str
    questions_asked: int
    marks_weight: float
    years_active: int
