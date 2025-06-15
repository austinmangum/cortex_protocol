from fastapi import FastAPI
from backend.app.api import game_routes

app = FastAPI(
    title="Cortex Protocol API",
    description="Backend for the game of deceit and action ",
    version="0.1.0"
)

app.include_router(game_routes.router, prefix="/game", tags=["Game"])