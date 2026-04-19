from pydantic import BaseModel
from typing import Optional

# Pydantic models
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    in_stock: bool

class ItemCreate(Item):
    name: str
    description: Optional[str]
    price: float
    in_stock: bool

class ItemUpdate(Item):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    in_stock: Optional[bool]
