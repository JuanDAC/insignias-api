from sqlmodel import Field, DateTime, SQLModel
from datetime import utcnow
from uuid import uuid4
from uuid import uuid4

from app.core.entities.base_entity import BaseEntity

class BaseSQLModel(BaseEntity, SQLModel, table=True):
  id = Field(default_factory=uuid4, primary_key=True)
  created_at = DateTime(default=utcnow())
  updated_at = DateTime(default=utcnow(), onupdate=utcnow())
  deleted_at = None