from app.infra.adapters.db.insignias.insignia_orm import Insignia
from sqlmodel import Session

from .get_insignia_by_id import get_insignia_by_id

def upload_insignia_image(db: Session, insignia_id: int, image_url: str) -> Insignia | None:
  insignia = get_insignia_by_id(db, insignia_id)

  if insignia is None:
    return None

  insignia.image_url = image_url

  db.add(insignia)
  db.commit()
  db.refresh(insignia)

  return Insignia.model_validate(insignia)