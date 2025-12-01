from fastapi import FastAPI

from database import Base, engine
import models
from domain.question.question_router import router as question_router


app = FastAPI()

# Create tables on startup (idempotent for SQLite)
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(question_router)


@app.get('/')
def read_root() -> dict:
    return {'message': 'OK'}


