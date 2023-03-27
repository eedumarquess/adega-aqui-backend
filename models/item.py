from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    stock: int
    price: float