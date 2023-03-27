from pydantic import BaseModel

class User(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "6108c37f37293412731d6f17",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "full_name": "John Doe",
                "disabled": False
            }
        }
        orm_mode = True
        exclude = ["password"]