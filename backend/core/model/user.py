from pydantic import BaseModel

user_collection = "users"

class User(BaseModel):
    id: str
    google_id: str = None
    email: str
    hashed_pwd: str  # if login with google, then pwd default will be hashed google id
    name: str  # if login with google, then name default will be google name
    created_at: int
    updated_at: int
    is_active: bool = True

