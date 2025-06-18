from fastapi import FastAPI, Request
from backend.app.api import game_routes


app = FastAPI(
    title="Cortex Protocol API",
    description="Backend for the game of deceit and action ",
    version="0.1.0"
)

# 🔍 Request Body Logger Middleware
@app.middleware("http")
async def log_request_body(request: Request, call_next):
    body = await request.body()
    print(f"🔍 Request Body: {body.decode()}")
    response = await call_next(request)
    return response

app.include_router(game_routes.router, prefix="/game", tags=["Game"])