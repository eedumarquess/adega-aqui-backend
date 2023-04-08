import json
from fastapi import APIRouter, Response
from handlers.predict_beer_sales import predict_beer_sales

router = APIRouter()

@router.get("/beer_prediction")
async def send_beer_prediction():
    beer_prediction = predict_beer_sales()

    response_data = {"predicted_sales": beer_prediction[0]}
    response_body = json.dumps(response_data)

    return Response(content=response_body, media_type="application/json")
