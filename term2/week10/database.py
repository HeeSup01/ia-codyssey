from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file placed in the project root
SQLALCHEMY_DATABASE_URL = 'sqlite:///./app.db'

# For SQLite, check_same_thread must be False when using in web apps
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

# As required: autocommit is False
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


