from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question


router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)


@router.get('', summary='Get question list')
@router.get('/', summary='Get question list (slash)')
def question_list(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    questions = db.query(Question).all()
    results: List[Dict[str, Any]] = []
    for item in questions:
        results.append(
            {
                'id': item.id,
                'subject': item.subject,
                'content': item.content,
                'created_at': item.created_at.isoformat() if item.created_at else None,
            }
        )
    return results


