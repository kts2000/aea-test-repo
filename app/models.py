from pydantic import BaseModel, Field
from typing import Optional, List, UUID
from uuid import UUID, uuid4

# Item model
class Item(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

# Item create model
class ItemCreate(Item):
    id: None = None

# Item update model
class ItemUpdate(Item):
    id: Optional[UUID] = None

# List of items
Items = List[Item]
