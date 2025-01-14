from typing import List
from pydantic import BaseModel, Field
from app.schemas.product import ProductSchema

class CategorySchema(BaseModel):
    id: int
    name: str
    products: List[ProductSchema]

    class Config:
        orm_mode = True
        from_attributes = True
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
