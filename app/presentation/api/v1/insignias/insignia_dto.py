
from app.core.entities.insignia.insignia_entity import Insignia as InsigniaEntity
from pydantic import BaseModel, field_validator, Field
from urllib.parse import urlparse
import requests

class InsigniaCreate(BaseModel, InsigniaEntity):
  description: str
  name: str = Field(max_length=255, min_length=3) 
  description: str = Field(max_length=255)
  url_image: str = Field(max_length=255)

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

  @field_validator('url_image')
  @classmethod
  def validate_url_image(cls, value):
    if not value.strip():
      raise ValueError("Insignia URL cannot be empty")

    try:
      result = urlparse(value)
      if not (result.scheme and result.netloc):
        raise ValueError("Invalid URL format")
    except ValueError:
      raise ValueError("Invalid URL format")

    try:
      response = requests.head(value)
      content_type = response.headers.get('content-type')
      if not content_type.startswith('image/'):
        raise ValueError("Invalid image content type")
    except requests.exceptions.RequestException as e:
      raise ValueError(f"Error fetching image: {e}")

    return value 


