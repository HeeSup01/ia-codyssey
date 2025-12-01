from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from database import Base  # type: ignore[no-redef]


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


