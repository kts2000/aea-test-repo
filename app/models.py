from pydantic import BaseModel, Field
from typing import List, Optional


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
