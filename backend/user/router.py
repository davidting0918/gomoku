from fastapi import APIRouter, HTTPException
from backend.core.model.user import CreateUserRequest
from backend.user.service import UserService
router = APIRouter(
    prefix="/user",
    tags=["user"]
)

user_service = UserService()


# create user
@router.post("/create")
async def create_user(request: CreateUserRequest) -> dict:
    try:
        user_info = await user_service.create_user(request)
        return {
            "status": 1,
            "data": user_info.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/info")
async def get_user_info(user_id: str) -> dict:
    try:
        user_info = await user_service.get_user_info(user_id)
        return {
            "status": 1,
            "data": user_info.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))