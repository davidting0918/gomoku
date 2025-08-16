from pydantic import BaseModel, ConfigDict
from enum import Enum

game_collection = "games"

class GameType(Enum):
    GOMOKU = "gomoku"


class CreateGameRequest(BaseModel):
    type: GameType

class JoinGameRequest(BaseModel):
    search_id: str


class Game(BaseModel):

    model_config = ConfigDict(use_enum_values=True)

    id: str
    search_id: str  # 6 digits
    user_id: str
    type: GameType
    created_at: int
    updated_at: int
    is_active: bool = True
    can_join: bool = True
    data: dict = {}
