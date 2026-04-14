from pydantic import BaseModel, Field
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime

# Pydantic model for item input
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

    class Config:
        orm_mode = True

# Pydantic model for item update
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None

    class Config:
        orm_mode = True

# Pydantic model for item output
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

    class Config:
        orm_mode = True

# Custom Pydantic model for in-memory storage
class ItemInDB(Item):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True