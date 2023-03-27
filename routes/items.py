import json
from typing import List
from fastapi import APIRouter, Response
from handlers.items_stock import create_item, read_items, read_item, update_item, delete_item
from models.item import Item

router_items = APIRouter(prefix="/items")

@router_items.post("/", response_model=Item)
async def send_create_item():
  response_body = await create_item()
  response_body_json = json.dumps(response_body)

  return Response(content=response_body_json, media_type="application/json")

@router_items.get("/", response_model=List[Item])
async def send_read_items():
  response_body = await read_items()
  response_body_json = json.dumps(response_body)

  return Response(content=response_body_json, media_type="application/json")

@router_items.get("/{item_id}", response_model=Item)
async def send_read_item():
  response_body = await read_item()
  response_body_json = json.dumps(response_body)

  return Response(content=response_body_json, media_type="application/json")

@router_items.put("/{item_id}", response_model=Item)
async def send_update_item():
  response_body = await update_item()
  response_body_json = json.dumps(response_body)

  return Response(content=response_body_json, media_type="application/json")
@router_items.delete("/{item_id}")
async def send_delete_item():
  response_body = await delete_item()
  response_body_json = json.dumps(response_body)

  return Response(content=response_body_json, media_type="application/json")