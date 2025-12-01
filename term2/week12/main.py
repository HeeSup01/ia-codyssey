from fastapi import FastAPI

from database import Base, engine
from domain.question.question_router import router as question_router
import models  # noqa: F401  # ensure models are imported for metadata


app = FastAPI()

# Create tables on startup (simple approach for tutorial-style apps)
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(question_router)


@app.get('/', summary='Health check')
def root() -> dict:
    return {'status': 'ok'}


