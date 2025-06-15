#this file defines the public API. its decided what endpoints exsist and what schemas each endpoint uses
from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import (
    StartGameRequest,
    GameStateResponse,
    ClaimActionRequest,
    BlockActionRequest,
    ChallengeActionRequest
)
from backend.app.core.game_state import GameStore

router = APIRouter()
store = GameStore()

@router.post("/start", response_model=GameStateResponse)
def start_game(payload: StartGameRequest):
    return store.start_new_game(payload)

@router.get("/state", response_model=GameStateResponse)
def get_game_state():
    return store.get_current_state()

@router.post("/action", response_model=GameStateResponse)
def claim_action(payload: ClaimActionRequest):
    try:
        store.claim_action(payload)
        return store.get_current_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/block", response_model=GameStateResponse)
def block_action(payload: BlockActionRequest):
    try:
        store.block_action(payload)
        return store.get_current_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/challenge", response_model=GameStateResponse)
def challenge_action(payload: ChallengeActionRequest):
    try:
        store.challenge_action(payload)
        return store.get_current_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/resolve", response_model=GameStateResponse)
def resolve_next():
    try:
        store.resolve_next()
        return store.get_current_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))