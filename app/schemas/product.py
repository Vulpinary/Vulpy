from typing import Optional, List
from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    id: int
    name: str
    manufacturer: str
    price: float
    description: Optional[str] = None
    category_id: int

    class Config:
        orm_mode = True
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    manufacturer: str
    price: float
    description: Optional[str] = None
    category_id: int
    supplier_ids: List[int] = Field(default_factory=list)

class ProductUpdateSchema(BaseModel):
    name: str
    manufacturer: str
    price: float
    description: Optional[str] = None
    category_id: int

    class Config:
        orm_mode = True