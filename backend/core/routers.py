from fastapi import APIRouter, HTTPException
from core.models import Move, Game
from core import services

router = APIRouter()

@router.get("/board", response_model=Game)
def get_board():
    return services.get_game_state()

@router.post("/move", response_model=Game)
def move_piece(move: Move):
    status = services.make_move(
        player=move.player,
        x=move.x,
        y=move.y
    )
    if not status:
        raise HTTPException(status_code=400, detail=f"Make move failed, {move.player, move.x, move.y}") 
    
    return services.get_game_state()

@router.post("/reset")
def reset():
    services.reset_game()
    return {"status": "reset"}