import json
from typing import List
from fastapi import APIRouter, Request, Response, Depends
from handlers.autenticate import register, login, get_current_user
from models.user import User

router_auth = APIRouter(prefix="/auth")

@router_auth.post("/register")
async def send_register(request: Request):
    user_data = await request.json()
    user = User(email=user_data['email'], password=user_data['password'])
    response_body = register(user)
    response_body_json = json.dumps(response_body)
    return Response(content=response_body_json, media_type="application/json", status_code=201)

@router_auth.post("/login")
async def send_login(request: Request):
    user_data = await request.json()
    user = User(email=user_data['email'], password=user_data['password'])
    response_body = login(user)
    response_body_json = json.dumps(response_body)
    return Response(content=response_body_json, media_type="application/json", status_code=201)
