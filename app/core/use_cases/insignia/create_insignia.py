from app.infra.adapters.db.insignias.insignia_orm import Insignia
from sqlmodel import Session

def create_insignia(db: Session, insignia: Insignia) -> Insignia:
  db.add(insignia)
  db.commit()
  db.refresh(insignia)
  return Insignia.model_validate(insignia)