from app.core.entities.insignia.insignia_entity import Insignia
from sqlmodel import Session, select

def get_insignias(db: Session, skip: int = 0, limit: int = 100) -> list[Insignia]:
  return db.exec(select(Insignia).offset(skip).limit(limit)).all()