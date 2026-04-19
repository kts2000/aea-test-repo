from fastapi import FastAPI, HTTPException, Path, Query, Depends, status
from app.models import Item, ItemCreate, ItemUpdate, Items
from typing import List, Optional
from uuid import uuid4, UUID

app = FastAPI()

# In-memory data store
items: List[Item] = []

# Helper function to get an item by ID
async def get_item_by_id(id: UUID) -> Optional[Item]:
    return next((item for item in items if item.id == id), None)

# Helper function to create a new item ID
async def create_new_item_id() -> UUID:
    return uuid4()

# GET /items
@app.get('/items', response_model=List[Item], status_code=status.HTTP_200_OK)
def read_items():
    return items

# POST /items
@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    new_item = Item(**item.dict(), id=create_new_item_id())
    items.append(new_item)
    return new_item

# GET /items/{id}
@app.get('/items/{id}', response_model=Item, status_code=status.HTTP_200_OK)
def read_item(id: UUID = Path(..., title='The ID of the item to get')):
    item = get_item_by_id(id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return item

# PUT /items/{id}
@app.put('/items/{id}', response_model=Item, status_code=status.HTTP_200_OK)
def update_item(id: UUID = Path(..., title='The ID of the item to update'), item: ItemUpdate):
    existing_item = get_item_by_id(id)
    if existing_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

    update_data = item.dict(exclude_unset=True)
    updated_item = Item(**existing_item.dict(), **update_data)
    items.remove(existing_item)
    items.append(updated_item)
    return updated_item

# DELETE /items/{id}
@app.delete('/items/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: UUID = Path(..., title='The ID of the item to delete')):
    existing_item = get_item_by_id(id)
    if existing_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    items.remove(existing_item)
    return None
