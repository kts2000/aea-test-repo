from fastapi import FastAPI, HTTPException, Body, Path, Query, Depends
from app.models import Item, ItemCreate, ItemUpdate, ItemInDB
from typing import List, Optional
import uuid

app = FastAPI()

items_db = []

# Helper function to get item by ID
def get_item_by_id(id: int) -> ItemInDB:
    for item in items_db:
        if item['id'] == id:
            return ItemInDB(**item)
    raise HTTPException(status_code=404, detail='Item not found')

# CRUD endpoints
@app.get('/items', response_model=List[Item], status_code=200)
def read_items(skip: int = 0, limit: int = 10) -> List[Item]:
    return [Item(**item) for item in items_db[skip:skip+limit]]

@app.post('/items', response_model=Item, status_code=201)
def create_item(item: ItemCreate) -> Item:
    item_id = str(uuid.uuid4())
    new_item = ItemInDB(id=item_id, **item.dict())
    items_db.append(new_item)
    return Item(**new_item)

@app.get('/items/{item_id}', response_model=Item, status_code=200)
def read_item(item_id: int = Path(..., ge=1)) -> Item:
    item = get_item_by_id(item_id)
    return Item(**item)

@app.put('/items/{item_id}', response_model=Item, status_code=200)
def update_item(item_id: int = Path(..., ge=1), item: ItemUpdate = Body(...)) -> Item:
    item = get_item_by_id(item_id)
    for key, value in item.dict().items():
        if value is not None:
            item[key] = value
    return Item(**item)

@app.delete('/items/{item_id}', status_code=204)
def delete_item(item_id: int = Path(..., ge=1)) -> None:
    global items_db
    items_db = [item for item in items_db if item['id'] != str(item_id)]