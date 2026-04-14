from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import List, Optional
from app.models import Item, ItemCreate, ItemUpdate, ItemInDB

app = FastAPI()

items_db: List[ItemInDB] = []

@ app.get('/items', response_model=List[Item], status_code=200)
def get_items()
:
    return items_db

@ app.post('/items', response_model=Item, status_code=201)
def create_item(item: ItemCreate)
:
    # Check for duplicate item
    for exist_item in items_db:
        if exist_item.name == item.name:
            raise HTTPException(status_code=400, detail='Item with the same name already exists')

    item_id = len(items_db) + 1
    item_in_db = ItemInDB(id=item_id, **item.dict())
    items_db.append(item_in_db)

    return item_in_db

@ app.get('/items/{item_id}', response_model=Item, status_code=200)
def get_item(item_id: int = Path(..., ge=1))
:
    # Find item
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')

    return item

@ app.put('/items/{item_id}', response_model=Item, status_code=200)
def update_item(item_id: int = Path(..., ge=1), item: ItemUpdate)
:
    # Find item
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail='Item not found')

    # Update item
    item_in_db = ItemInDB(**items_db[item_index].dict())
    item_in_db.update(item.dict(exclude_unset=True))
    items_db[item_index] = item_in_db

    return item_in_db

@ app.delete('/items/{item_id}', status_code=204)
def delete_item(item_id: int = Path(..., ge=1))
:
    # Find item
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail='Item not found')

    # Delete item
    del items_db[item_index]
    return
