from backend.core.database import MongoAsyncClient
from backend.core.model.game import game_collection, CreateGameRequest, Game, JoinGameRequest, GameType, GomokuMoveRequest
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
        MAX_ATTEMPTS = 10
        for _ in range(MAX_ATTEMPTS):
            search_id = str(random.randint(100000, 999999))
            if not await self.db.find_one(game_collection, {"search_id": search_id}):
                return search_id
        raise HTTPException(status_code=500, detail="Unable to generate unique search_id after multiple attempts")

    async def get_game(self, game_id: str) -> Game:
        game = await self.db.find_one(game_collection, {"id": game_id})
        if not game:
            raise HTTPException(status_code=404, detail=f"Game with id {game_id} not found")
        return Game(**game)
    
    async def create_game(self, user_id: str, request: CreateGameRequest) -> Game:
        game = Game(
            id=self.create_game_id(),
            search_id=await self.create_search_id(),
            user_id=user_id,
            type=request.type,
            created_at=int(dt.now(tz.utc).timestamp()),
            updated_at=int(dt.now(tz.utc).timestamp()),
            is_active=True,
            can_join=True
        )

        if request.type == GameType.GOMOKU:
            game.data = {
                "p1_id": user_id,
                "p2_id": None,
                "p1_color": "black",
                "p2_color": "white",
                "board": self.gomoku.create_board(),
                "winner": None
            }

        await self.db.insert_one(game_collection, game.model_dump())
        return game
    
    async def join_game(self, user_id: str, request: JoinGameRequest) -> Game:
        game = await self.db.find_one(game_collection, {"search_id": request.search_id})
        if not game:
            raise HTTPException(status_code=404, detail=f"Game with search_id {request.search_id} not found")
        game = Game(**game)
        
        if not game.is_active or not game.can_join:
            raise HTTPException(status_code=400, detail="Game is not active or can't join")
        
        if game.type == GameType.GOMOKU.value:
            game.data["p2_id"] = user_id
            game.can_join = False
            await self.db.update_one(game_collection, {"id": game.id}, {"$set": game.model_dump()})

        game.updated_at = int(dt.now(tz.utc).timestamp())
        return game
    
    async def gomoku_move(self, user_id: str, game_id: str, request: GomokuMoveRequest) -> Game:
        game = await self.get_game(game_id)
        color = game.data['p1_color'] if user_id == game.data['p1_id'] else game.data['p2_color']
        board, is_win = self.gomoku.move(
            game.data["board"],
            color,
            request.x,
            request.y
        )
        game.data["board"] = board
        if is_win:
            game.data['winner'] = color
        game.updated_at = int(dt.now(tz.utc).timestamp())
        await self.db.update_one(game_collection, {"id": game.id}, {"$set": game.model_dump()})
        return game
    
    async def get_gomoku_status(self, user_id: str, game_id: str) -> dict:
        game = await self.get_game(game_id)

        if user_id != game.data["p1_id"] and user_id != game.data["p2_id"]:
            raise HTTPException(status_code=403, detail="You are not allowed to access this game")
        
        return game
    
    async def check_gomoku_win(self, user_id: str, game_id: str) -> str:
        game = await self.get_game(game_id)

        if user_id != game.data["p1_id"] and user_id != game.data["p2_id"]:
            raise HTTPException(status_code=403, detail="You are not allowed to access this game")
        
        win_color = self.gomoku.check_win(game.data["board"])
        return win_color
    
    async def settle_gomoku_game(self,):
        pass