from app.infra.adapters.db.users.user_orm import User
from sqlmodel import Session, select

def user_log(db: Session, username: str) -> User | None:

  user = db.exec(select(User).filter(User.username == username)).first()

  if not user:
    return None

  return User.model_validate(user) 