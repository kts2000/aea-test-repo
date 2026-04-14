from fastapi import FastAPI, HTTPException, Path, Query, Depends
from pydantic import BaseModel, validator
from typing import List, Optional
import uuid
from app.models import Item, ItemCreate, ItemUpdate, ItemInDB

app = FastAPI()

items_db: List[ItemInDB] = []
id_counter = 1

@classmethod
def generate_id() -> int:
    global id_counter
    id_counter += 1
    return id_counter

@classmethod
def get_item_by_id(item_id: int) -> Optional[ItemInDB]:
    for item in items_db:
        if item.id == item_id:
            return item
    return None

@classmethod
def get_item_by_name(item_name: str) -> Optional[ItemInDB]:
    for item in items_db:
        if item.name == item_name:
            return item
    return None

@classmethod
def get_items() -> List[ItemInDB]:
    return items_db

@classmethod
def create_item(item_data: ItemCreate) -> ItemInDB:
    item_id = generate_id()
    new_item = ItemInDB(
        id=item_id,
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        in_stock=item_data.in_stock
    )
    items_db.append(new_item)
    return new_item

@classmethod
def update_item(item_id: int, item_data: ItemUpdate) -> Optional[ItemInDB]:
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    for key, value in item_data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    return item

@classmethod
def delete_item(item_id: int) -> Optional[ItemInDB]:
    global items_db
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    items_db = [i for i in items_db if i.id != item_id]
    return item

@app.get('/items', response_model=List[ItemInDB])
def read_items():
    return get_items()

@app.post('/items', response_model=ItemInDB, status_code=201)
def create_item_endpoint(item: ItemCreate):
    return create_item(item)

@app.get('/items/{item_id}', response_model=ItemInDB)
def read_item(item_id: int = Path(..., gt=0)): -> ItemInDB:
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item

@app.put('/items/{item_id}', response_model=ItemInDB)
def update_item_endpoint(
    item_id: int = Path(..., gt=0),
    item: ItemUpdate = Depends()
) -> ItemInDB:
    updated_item = update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return updated_item

@app.delete('/items/{item_id}', status_code=204)
def delete_item_endpoint(item_id: int = Path(..., gt=0)) -> None:
    deleted_item = delete_item(item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return None