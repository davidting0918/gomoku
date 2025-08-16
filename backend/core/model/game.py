from pydantic import BaseModel
from enum import Enum

game_collection = "games"

class GameType(Enum):
    GOMOKU = "gomoku"


class CreateGameRequest(BaseModel):
    user_id: str
    type: GameType

class JoinGameRequest(BaseModel):
    user_id: str
    search_id: str


class Game(BaseModel):
    id: str
    search_id: str  # 6 digits
    user_id: str
    type: GameType
    created_at: int
    updated_at: int
    is_active: bool = True
    can_join: bool = True
    data: dict = {}
