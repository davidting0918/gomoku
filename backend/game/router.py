from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from backend.core.model.game import CreateGameRequest, JoinGameRequest
from backend.core.model.user import User
from backend.game.service import GameService
from backend.auth.service import AuthService

router = APIRouter(
    prefix="/game",
    tags=["game"]
)

game_service = GameService()
auth_service = AuthService()

# Public endpoint - no JWT token required
@router.get("/list")
async def get_game_list() -> dict:
    """
    Get game list - public endpoint, no authentication required
    Anyone can view available games
    """
    try:
        games = await game_service.get_available_games()
        return {
            "status": 1,
            "data": games,
            "message": "Successfully retrieved game list"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Protected endpoint - JWT token required
@router.post("/create")
async def create_game(
    request: CreateGameRequest,
    current_user: Annotated[User, Depends(auth_service.get_current_active_user)]
) -> dict:
    """
    Create game - requires JWT authentication
    Only authenticated active users can create games
    """
    try:
        game = await game_service.create_game(request)
        return {
            "status": 1,
            "data": game.model_dump(),
            "message": f"Game created successfully by {current_user.name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/join")
async def join_game(
    request: JoinGameRequest,
    current_user: Annotated[User, Depends(auth_service.get_current_active_user)]
) -> dict:
    try:
        game = await game_service.join_game(request)
        return {
            "status": 1,
            "data": game.model_dump(),
            "message": f"Game joined successfully by {current_user.name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))