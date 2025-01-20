from app.infra.adapters.db.users.user_orm import User
from sqlmodel import Session


def user_register(db: Session, user: User) -> User:
  db.add(user)
  db.commit()
  db.refresh(user)
  return User.model_validate(user) 