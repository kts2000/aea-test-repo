from pydantic import BaseModel
from typing import Optional

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


class ItemInDB(ItemBase):
    id: int

    class Config:
        orm_mode = True
