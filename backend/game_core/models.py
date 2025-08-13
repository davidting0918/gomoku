from pydantic import BaseModel
from typing import List, Optional

BOARD_SIZE = 19

class Move(BaseModel):
    player: str
    x: int
    y: int

class Board(BaseModel):
    black: List[List[int]]
    white: List[List[int]]

class Game(BaseModel):
    board: Board
    winner: Optional[str]


