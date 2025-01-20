from sqlmodel import Column, String, Integer 

from app.infra.adapters.db.base_orm import BaseSQLModel
from app.core.entities.user.user_entity import User as UserEntity

class User(UserEntity, BaseSQLModel):
  __tablename__ = 'users'

  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password_hash = Column(String)
  experience = Column(Integer, default=0)
  level = Column(Integer, default=1)
