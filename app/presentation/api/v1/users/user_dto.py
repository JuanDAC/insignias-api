from app.core.entities.user.user_entity import User as UserEntity
from pydantic import BaseModel, EmailStr, field_validator, Field
from re import match

USERNAME_ALPHANUMERIC_REGEX = r"^[a-zA-Z0-9_]+$"
PASSWORD_STRONG_WITH_SPECIAL_CHARS_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

class UserCreate(BaseModel, UserEntity):
  id = Field(max_length=255)
  username = Field(max_length=255)
  password = Field(min_length=8)
  email: EmailStr

  @field_validator('username', mode='before')
  @classmethod
  def validate_username(cls, value):
    if not match(USERNAME_ALPHANUMERIC_REGEX, value):
      raise ValueError("Username must be alphanumeric or contain underscores")
    return value

  @field_validator('password')
  @classmethod
  def validate_password(cls, value):
    if not match(PASSWORD_STRONG_WITH_SPECIAL_CHARS_REGEX, value):
      raise ValueError("Password must contain at least one uppercase, one lowercase, one number, and one special character")
    return value

