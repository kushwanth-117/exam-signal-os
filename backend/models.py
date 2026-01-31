from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class UnitSignal(Base):
    __tablename__ = "unit_signals"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(String)
    unit_name = Column(String)
    questions_asked = Column(Integer)
    marks_weight = Column(Float)
    years_active = Column(Integer)
