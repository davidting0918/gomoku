from backend.core.database import MongoAsyncClient
from backend.core.model.game import game_collection, CreateGameRequest, Game, JoinGameRequest, GameType
import random
from datetime import datetime as dt, timezone as tz
from fastapi import HTTPException
from backend.game.providers.gomoku import Gomoku


class GameService:
    def __init__(self):
        self.db = MongoAsyncClient()
        self.gomoku = Gomoku()

    def create_game_id(self) -> str:
        return hex(int(dt.now(tz.utc).timestamp() * 1000))[2:]
    
    async def create_search_id(self) -> str:
        while True:
            search_id = str(random.randint(100000, 999999))
            if not await self.db.find_one(game_collection, {"search_id": search_id}):
                return search_id

    async def create_game(self, request: CreateGameRequest) -> Game:
        game = Game(
            id=self.create_game_id(),
            search_id=await self.create_search_id(),
            user_id=request.user_id,
            type=request.type,
            created_at=int(dt.now(tz.utc).timestamp()),
            updated_at=int(dt.now(tz.utc).timestamp()),
            is_active=True,
            can_join=True
        )

        if request.type == GameType.GOMOKU:
            game.data = {
                "p1_user_id": request.user_id,
                "p2_user_id": None,
                "p1_color": "black",
                "p2_color": "white",
                "board": self.gomoku.create_board()
            }

        await self.db.insert_one(game_collection, game.model_dump())
        return game
    
    async def join_game(self, request: JoinGameRequest) -> Game:
        game = await self.db.find_one(game_collection, {"search_id": request.search_id})
        if not game:
            raise HTTPException(status_code=404, detail=f"Game with search_id {request.search_id} not found")
        game = Game(**game)
        
        if not game.is_active or not game.can_join:
            raise HTTPException(status_code=400, detail="Game is not active or can't join")
        
        if game.type == GameType.GOMOKU:
            game.data["p2_user_id"] = request.user_id
            game.can_join = False
            await self.db.update_one(game_collection, {"id": game.id}, {"$set": game.model_dump()})

        game.updated_at = int(dt.now(tz.utc).timestamp())
        return game