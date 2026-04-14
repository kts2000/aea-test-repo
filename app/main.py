from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, validator
from app.models import Item, ItemCreate, ItemUpdate
from typing import List, Optional
import random
import string

app = FastAPI()

items = []

# Helper function to generate unique id
def generate_unique_id() -> int:
    return len(items) + 1

# Helper function to find item by id
def get_item_by_id(id: int) -> Optional[Item]:
    return next((item for item in items if item.id == id), None)

# Helper function to find index of item by id
def get_item_index_by_id(id: int) -> Optional[int]:
    return next((index for index, item in enumerate(items) if item.id == id), None)

@app.post(
    "/items",
    response_model=Item,
    status_code=201,
)
def create_item(item_create: ItemCreate) -> Item:
    item = Item(**item_create.dict(), id=generate_unique_id())
    items.append(item)
    return item

@app.get(
    "/items",
    response_model=List[Item],
)
def read_items() -> List[Item]:
    return items

@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True,
)
def read_item(item_id: int = Path(..., ge=1)) -> Item:
    item = get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True,
)
def update_item(item_id: int = Path(..., ge=1), item_update: ItemUpdate = ...) -> Item:
    item = get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item_update_data = item_update.dict(exclude_unset=True)
    for key, value in item_update_data.items():
        setattr(item, key, value)

    return item

@app.delete(
    "/items/{item_id}",
    status_code=204,
)
def delete_item(item_id: int = Path(..., ge=1)) -> None:
    item_index = get_item_index_by_id(item_id)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")

    items.pop(item_index)
    return None
