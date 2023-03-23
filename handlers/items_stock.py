from fastapi import APIRouter, Body, HTTPException
from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from typing import List
from bson import ObjectId

from common.database import db
from models.item_model import Item

async def create_item(item: Item = Body(...)) -> Item:
    collection: Collection = db["items"]
    result: InsertOneResult = collection.insert_one(item.dict())
    item.id = str(result.inserted_id)
    return item

async def read_items() -> List[Item]:
    collection: Collection = db["items"]
    items = [Item(**item) for item in collection.find()]
    return items

async def read_item(item_id: str) -> Item:
    collection: Collection = db["items"]
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return Item(**item)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

async def update_item(item_id: str, item: Item = Body(...)) -> Item:
    collection: Collection = db["items"]
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.modified_count == 1:
        item.id = item_id
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

async def delete_item(item_id: str):
    collection: Collection = db["items"]
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail="Item not found")
