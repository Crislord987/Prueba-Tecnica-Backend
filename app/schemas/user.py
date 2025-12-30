from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

#Esquemas para creacion x

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")


class UserResponse(UserBase):
    id: int
    created_at: datetime
    #Convercion a dict
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    #Info en payload
    email: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
