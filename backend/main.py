from fastapi import FastAPI
from core.routers import router as game_router
import uvicorn

app = FastAPI()
app.include_router(game_router, prefix="/game")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
