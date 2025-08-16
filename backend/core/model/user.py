from typing import Optional
from pydantic import BaseModel, EmailStr

user_collection = "users"

class User(BaseModel):
    id: str
    google_id: Optional[str] = None
    email: EmailStr
    hashed_pwd: str  # if login with google, then pwd default will be hashed google id
    name: str  # if login with google, then name default will be google name
    created_at: int
    updated_at: int
    is_active: bool = True

class UserInfo(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: int
    updated_at: int
    is_active: bool = True


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    pwd: str