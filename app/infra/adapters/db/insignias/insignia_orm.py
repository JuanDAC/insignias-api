from sqlmodel import Field, Relationship, Column, String
from uuid import uuid4

from app.infra.adapters.db.base_orm import BaseSQLModel
from app.core.entities.user.user_entity import User as UserEntity
from app.core.entities.insignia.insignia_entity import Insignia as InsigniaEntity

class Insignia(InsigniaEntity, BaseSQLModel):
  __tablename__ = 'badges'

  name = Column(String, unique=True, index=True)
  description = Column(String)
  user_id = Field(default=uuid4(), foreign_key="users.id")
  users: list[UserEntity]  = Relationship(back_populates="badges")
