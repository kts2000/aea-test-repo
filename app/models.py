from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# Pydantic models
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

# In-memory model
class ItemInDB(ItemBase):
    id: str
