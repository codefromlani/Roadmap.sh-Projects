from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str