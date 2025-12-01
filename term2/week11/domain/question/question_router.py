from typing import Generator, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import SessionLocal


router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', summary='Get question list')
def question_list(db: Session = Depends(get_db)) -> List[dict]:
    questions = db.query(models.Question).all()
    return [
        {
            'id': question.id,
            'subject': question.subject,
            'content': question.content,
            'created_at': question.created_at.isoformat() if question.created_at else None,
        }
        for question in questions
    ]


