from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime as dt, timedelta as td, timezone as tz
from backend.core.database import MongoAsyncClient
from backend.core.model.user import User, user_collection
from backend.core.model.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    ALGORITHM, 
    ACCESS_TOKEN_SECRET_KEY,
    access_token_collection
)
from backend.auth.providers.google import GoogleAuthProvider
import uuid
import os
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/access_token")

class AuthService:
    def __init__(self):
        self.db = MongoAsyncClient()
        self.google_provider = GoogleAuthProvider(
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
        )
        self.secret_key = ACCESS_TOKEN_SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def generate_token_id(self, user_id: str, timestamp: int) -> str:
        """生成唯一的令牌 ID"""
        return hashlib.sha256(f"{user_id}:{timestamp}".encode()).hexdigest()

    def create_access_token(self, data: dict, user_id: str):
        to_encode = data.copy()
        current_time = dt.now(tz.utc)
        expire = current_time + td(minutes=self.access_token_expire_minutes)
        
        # 添加令牌 ID 和創建時間
        token_id = self.generate_token_id(user_id, int(current_time.timestamp()))
        to_encode.update({
            "exp": expire,
            "jti": token_id,  # JWT ID
            "iat": current_time,  # Issued at
            "user_id": user_id
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, token_id

    async def store_token(self, token_id: str, user_id: str, expires_at: int):
        """將令牌信息存儲到數據庫"""
        token_info = {
            "token_id": token_id,
            "user_id": user_id,
            "created_at": int(dt.now(tz.utc).timestamp()),
            "expires_at": int(expires_at.timestamp()),
            "is_revoked": False
        }
        await self.db.insert_one(access_token_collection, token_info)

    async def find_valid_token(self, user_id: str) -> Optional[str]:
        """查找用戶的有效令牌"""
        current_time = int(dt.now(tz.utc).timestamp())
        
        # 查找未過期且未撤銷的令牌
        token_dict = await self.db.find_one(
            access_token_collection,
            {
                "user_id": user_id,
                "expires_at": {"$gt": current_time},
                "is_revoked": False
            }
        )
        
        if token_dict:
            return token_dict["token_id"]
        return None

    async def get_or_create_token(self, user_id: str) -> dict:
        """獲取現有令牌或創建新令牌"""
        # 先檢查是否有有效令牌
        existing_token_id = await self.find_valid_token(user_id)
        
        if existing_token_id:
            # 使用現有令牌
            return {
                "access_token": existing_token_id,
                "token_type": "bearer",
                "token_id": existing_token_id,
                "is_new": False
            }
        else:
            # 創建新令牌
            access_token, token_id = self.create_access_token(
                data={"sub": user_id}, user_id=user_id
            )
            
            # 存儲令牌到數據庫
            current_time = dt.now(tz.utc)
            expire = current_time + td(minutes=self.access_token_expire_minutes)
            await self.store_token(token_id, user_id, expire)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "token_id": token_id,
                "is_new": True
            }

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user_dict = await self.db.find_one(user_collection, {"email": email})
        if not user_dict:
            return None
        
        user = User(**user_dict)
        if not self.verify_password(password, user.hashed_pwd):
            return None
        return user

    async def authenticate_google_user(self, token: str) -> Optional[User]:
        google_user_info = await self.google_provider.verify_token(token)
        
        # 先檢查是否有現有用戶（通過 email 或 google_id）
        user_dict = await self.db.find_one(
            user_collection, 
            {"$or": [{"email": google_user_info.email}, {"google_id": google_user_info.id}]}
        )
        
        if user_dict:
            user = User(**user_dict)
            
            # 如果用戶沒有 google_id，更新它
            if not user.google_id:
                await self.db.update_one(
                    user_collection,
                    {"id": user.id},
                    {
                        "google_id": google_user_info.id,
                        "updated_at": int(dt.now(tz.utc).timestamp())
                    }
                )
                user.google_id = google_user_info.id
            
            return user
        else:
            # 創建新用戶
            new_user = User(
                id=str(uuid.uuid4()),
                google_id=google_user_info.id,
                email=google_user_info.email,
                hashed_pwd=self.get_password_hash(google_user_info.id),
                name=google_user_info.name,
                created_at=int(dt.now(tz.utc).timestamp()),
                updated_at=int(dt.now(tz.utc).timestamp()),
                is_active=True
            )
            await self.db.insert_one(user_collection, new_user.model_dump())
            return new_user

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("user_id")
            token_id: str = payload.get("jti")
            
            if user_id is None or token_id is None:
                raise credentials_exception
                
        except JWTError:
            raise credentials_exception
        
        user_dict = await self.db.find_one(user_collection, {"id": user_id})
        if user_dict is None:
            raise credentials_exception
        
        return User(**user_dict)

    async def get_current_active_user(self, current_user: Annotated[User, Depends(get_current_user)]) -> User:
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user