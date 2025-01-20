from datetime import datetime
from typing import Optional, TypeVar
ID = TypeVar('ID')

class BaseEntity():
  id: ID
  created_at: datetime
  updated_at: datetime
  deleted_at: Optional[datetime] = None