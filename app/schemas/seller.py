from pydantic import BaseModel, Field, EmailStr, constr

class SellerCreate(BaseModel):
    username: constr(min_length=3, max_length=50) = Field(...)
    password: constr(min_length=8) = Field(...)
    name: constr(min_length=3, max_length=100) = Field(...)
    email: EmailStr = Field(..., min_length=3, max_length=100)

class SellerSchema(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    is_active: bool = True
    class Config:
        from_attributes = True

class SellerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class SellerAuth(BaseModel):
    username: constr(min_length=3, max_length=50) = Field(...)
    password: constr(min_length=8) = Field(...)

class Token(BaseModel):
    access_token: str
    token_type: str