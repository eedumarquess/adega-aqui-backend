from fastapi import FastAPI
from routes.predicts import router_predict
from routes.items import router_items

app = FastAPI()

app.include_router(router_predict)
app.include_router(router_items)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)