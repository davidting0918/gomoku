from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime as dt, timedelta as td, timezone as tz
from backend.core.database import MongoAsyncClient
from backend.core.model.user import User, user_collection
from backend.core.model.auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, ACCESS_TOKEN_SECRET_KEY
from backend.auth.providers.google import GoogleAuthProvider
import uuid
import os

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

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = dt.now(tz.utc) + td(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

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
        
        user_dict = await self.db.find_one(user_collection, {"google_id": google_user_info.id})
        
        if not user_dict:
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
        
        return User(**user_dict)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
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