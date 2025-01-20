from app.infra.adapters.db.users.user_orm import User
from sqlmodel import Session, select

def update_user_experience(db: Session, user_id: int, experience_delta: int) -> User | None:

  user = db.exec(select(User).filter(User.user_id == user_id)).first()

  if not user:
    return None

  user.experience += experience_delta

  db.add(user)
  db.commit()
  db.refresh(user)

  return User.model_validate(user) 