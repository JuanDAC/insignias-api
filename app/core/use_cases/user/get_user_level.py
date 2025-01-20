from app.infra.adapters.db.users.user_orm import User
from sqlmodel import Session, select


def get_user_level(db: Session, user_id: int) -> User | None:
    user= db.exec(select(User).filter(User.user_id == user_id)).first()
    return User.model_validate(user) 