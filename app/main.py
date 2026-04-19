import uvicorn
from fastapi import FastAPI, HTTPException, Path, Body, Depends
from pydantic import BaseModel, validator
from typing import List, Optional
from app.models import Item, ItemCreate, ItemUpdate
from uuid import uuid4, UUID

app = FastAPI()

items = []

# In-memory data store
class InMemoryStore:
    def add_item(self, item: Item) -> int:
        item.id = len(items) + 1
        items.append(item)
        return item.id

    def get_item(self, item_id: int) -> Optional[Item]:
        return next((item for item in items if item.id == item_id), None)

    def update_item(self, item_id: int, item: Item) -> Optional[Item]:
        existing_item = self.get_item(item_id)
        if existing_item:
            existing_item.name = item.name
            existing_item.description = item.description
            existing_item.price = item.price
            existing_item.in_stock = item.in_stock
            return existing_item
        return None

    def delete_item(self, item_id: int) -> bool:
        global items
        items = [item for item in items if item.id != item_id]
        return True if item_id in [item.id for item in items] else False

store = InMemoryStore()

@app.post('/items', response_model=Item, status_code=201)
def create_item(item: ItemCreate) -> Item:
    new_item = Item(**item.dict())
    item_id = store.add_item(new_item)
    new_item.id = item_id
    return new_item

@app.get('/items', response_model=List[Item])
def read_items() -> List[Item]:
    return items

@app.get('/items/{item_id}', response_model=Item, status_code=200)
def read_item(item_id: int = Path(..., gt=0)) -> Item:
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@app.put('/items/{item_id}', response_model=Item, status_code=200)
def update_item(item_id: int = Path(..., gt=0), item: ItemUpdate = Body(...)) -> Item:
    updated_item = store.update_item(item_id, Item(**item.dict()))
    if updated_item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return updated_item

@app.delete('/items/{item_id}', status_code=200)
def delete_item(item_id: int = Path(..., gt=0)) -> bool:
    success = store.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail='Item not found')
    return success
