from sqlalchemy.orm import Session
from sqlmodel import Session, create_engine
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def get_db():
  db = Session(engine)
  try:
    yield db
  finally:
    db.close()
