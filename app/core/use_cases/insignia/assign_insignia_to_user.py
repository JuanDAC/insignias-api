from app.infra.adapters.db.insignias.insignia_orm  import Insignia
from app.core.entities.base_entity import ID
from sqlmodel import Session

from .get_insignia_by_id import get_insignia_by_id

def assign_insignia_to_user(db: Session, insignia_id: int, user_id: ID) -> Insignia | None:

  insignia = get_insignia_by_id(db, insignia_id)

  if insignia is None:
    return None

  insignia.user_id = user_id

  db.add(insignia)
  db.commit()
  db.refresh(insignia)