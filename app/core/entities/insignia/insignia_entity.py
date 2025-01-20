from app.core.entities.base_entity import BaseEntity, ID

class Insignia(BaseEntity):
  name: str
  description: str
  url_image: str
  user_id: ID 
