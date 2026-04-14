from fastapi import FastAPI, HTTPException, Body, Path, status
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from app.models import Item, ItemCreate, ItemUpdate

app = FastAPI()

items = []
item_id_generator = 1

@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    global item_id_generator
    new_item = Item(id=item_id_generator, **item.dict())
    items.append(new_item)
    item_id_generator += 1
    return new_item

@app.get('/items', response_model=List[Item])
async def read_items():
    return items

@app.get('/items/{item_id}', response_model=Item)
async def read_item(item_id: int = Path(..., ge=1)):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail='Item not found')

@app.put('/items/{item_id}', response_model=Item)
async def update_item(item_id: int = Path(..., ge=1), item: ItemUpdate):
    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            items[index] = Item(**{**existing_item.dict(), **item.dict()})
            return items[index]
    raise HTTPException(status_code=404, detail='Item not found')

@app.delete('/items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int = Path(..., ge=1)):
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return
    raise HTTPException(status_code=404, detail='Item not found')