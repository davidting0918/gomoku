from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv("backend/.env")

ACCESS_TOKEN_EXPIRE_MINUTES = 120
ALGORITHM = "HS256"
ACCESS_TOKEN_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

class GoogleAuthRequest(BaseModel):
    token: str

class GoogleUserInfo(BaseModel):
    id: str
    email: str
    name: str
    picture: str

class EmailAuthRequest(BaseModel):
    email: str
    pwd: str