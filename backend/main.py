from fastapi import FastAPI
from backend.database import Base, engine
from backend import models
from backend.auth import router as auth_router
from backend.routes.signals import router as signals_router  # 👈 ADD THIS

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam Signal OS API")

app.include_router(auth_router)
app.include_router(signals_router)  # 👈 ADD THIS

@app.get("/health")
def health():
    return {"status": "ok"}
