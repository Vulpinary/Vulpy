from typing import Optional

from pydantic import BaseModel, EmailStr
from app.schemas.category import CategorySchema

class SupplierSchema(BaseModel):
    id: Optional[int] = None
    name: str
    seller_id: int
    email: Optional[str] = None
    phone: str
    address: str
    category: CategorySchema

    class Config:
        orm_mode = True
        from_attributes = True


class SupplierCreate(BaseModel):
    name: str
    seller_id: int
    email: Optional[str] = None
    phone: str
    address: str
    category_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class SupplierUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    category_id: int | None = None
    class Config:
        orm_mode = True
        from_attributes = True
