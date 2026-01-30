from fastapi import FastAPI
from backend.database import Base, engine
from backend.routes import auth, signals

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam Signal OS API")

app.include_router(auth.router)
app.include_router(signals.router)

@app.get("/health")
def health():
    return {"status": "ok"}
