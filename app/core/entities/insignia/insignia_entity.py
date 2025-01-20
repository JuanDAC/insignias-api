from app.core.entities.base_entity import BaseEntity, ID

class Insignia(BaseEntity):
  name: str
  description: str
  user_id: ID 
