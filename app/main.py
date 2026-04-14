from fastapi import FastAPI, HTTPException, Path, Depends, Query, status
from app.models import Item, ItemCreate, ItemUpdate, ItemInDB
from typing import List, Optional
from uuid import uuid4, UUID
from pydantic import BaseModel
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

items_db: List[ItemInDB] = []
id_generator = 1

# Pydantic model for HTTP responses
class ItemOut(Item):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Custom exception for item not found
class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: UUID):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f'Item with ID {item_id} not found')

# Utility function to find item by ID
def _find_item(item_id: UUID) -> Optional[ItemInDB]:
    return next((item for item in items_db if item.id == item_id), None)


@app.post('/items/', response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate) -> ItemInDB:
    global id_generator
    item_id = UUID(str(id_generator))
    item_in_db = ItemInDB(**item.dict(), id=item_id)
    items_db.append(item_in_db)
    return item_in_db

@app.get('/items/', response_model=List[ItemOut])
async def read_items() -> List[ItemInDB]:
    return items_db

@app.get('/items/{item_id}', response_model=ItemOut)
async def read_item(item_id: UUID = Path(..., title='The ID of the item to retrieve')) -> ItemInDB:
    item = _find_item(item_id)
    if not item:
        raise ItemNotFoundException(item_id)
    return item

@app.put('/items/{item_id}', response_model=ItemOut)
async def update_item(
    item_id: UUID = Path(..., title='The ID of the item to update'),
    item: ItemUpdate = Depends()
) -> ItemInDB:
    item_in_db = _find_item(item_id)
    if not item_in_db:
        raise ItemNotFoundException(item_id)

    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(item_in_db, key, value)
        item_in_db.updated_at = datetime.now()

    return item_in_db

@app.delete('/items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID = Path(..., title='The ID of the item to delete')) -> None:
    global items_db
    item = _find_item(item_id)
    if not item:
        raise ItemNotFoundException(item_id)
    items_db = [i for i in items_db if i.id != item_id]
