from app.core.entities.base_entity import BaseEntity

class User(BaseEntity):
  username: str
  email: str
  password_hash: str
  experience: int
  level: int