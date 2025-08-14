from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv("backend/.env")

ACCESS_TOKEN_EXPIRE_MINUTES = 120
ALGORITHM = "HS256"
ACCESS_TOKEN_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

access_token_collection = "tokens"

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

# 新增：令牌信息模型
class TokenInfo(BaseModel):
    token_id: str
    user_id: str
    created_at: int
    expires_at: int
    is_revoked: bool = False

# 新增：令牌響應模型
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    token_id: str
    is_new: bool