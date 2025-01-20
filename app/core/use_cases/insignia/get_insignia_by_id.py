from app.core.entities.insignia.insignia_entity import Insignia
from sqlmodel import Session, select

def get_insignia_by_id(db: Session, insignia_id: int) -> Insignia | None:
  return db.exec(select(Insignia).filter(Insignia.id == insignia_id)).first()