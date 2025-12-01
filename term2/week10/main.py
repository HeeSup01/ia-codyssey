from datetime import datetime

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Question


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get('/health')
def health() -> dict:
    return {'status': 'ok'}


@app.get('/questions')
def list_questions(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.query(Question).order_by(Question.id.desc()).all()
    results: list[dict] = []
    for row in rows:
        results.append(
            {
                'id': row.id,
                'subject': row.subject,
                'content': row.content,
                'create_date': row.create_date.isoformat() if isinstance(row.create_date, datetime) else None,
            }
        )
    return results


