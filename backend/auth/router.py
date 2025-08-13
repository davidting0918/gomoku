from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from backend.core.model.auth import GoogleAuthRequest, EmailAuthRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google/login")
async def validate_google_login_route(request: GoogleAuthRequest):
    pass


@router.post("/email/login")
async def validate_email_login_route(request: EmailAuthRequest):
    pass

@router.post("/access_token")
async def get_access_token_route(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    pass
