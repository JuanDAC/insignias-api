
from app.core.entities.insignia.insignia_entity import Insignia as InsigniaEntity
from pydantic import BaseModel, field_validator, Field

class InsigniaCreate(BaseModel, InsigniaEntity):
  description: str
  name: str = Field(max_length=255, min_length=3) 
  description: str = Field(max_length=255)

  @field_validator('name')
  @classmethod
  def validate_name(cls, value):
    if not value.strip():
      raise ValueError("Insignia name cannot be empty")
    return value

  @field_validator('description')
  @classmethod
  def validate_description(cls, value):
    if not value.strip():
      raise ValueError("Insignia description cannot be empty")
    return value

