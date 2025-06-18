#this file defines what is expected from input payloads and what the unified return format will be

from pydantic import BaseModel
from typing import List, Optional
from backend.app.engine.player import Player

class StartGameRequest(BaseModel):
    player_names: List[str]
    

class PlayerState(BaseModel):
    name: str
    credits: int
    cards: List[str]
    alive: bool

class ClaimActionRequest(BaseModel):
    player: str
    role: str
    target: Optional[str] = None

class BlockActionRequest(BaseModel):
    blocker: str
    blocking_role: str

class ChallengeActionRequest(BaseModel):
    challenger: str

class GameStateResponse(BaseModel):
    current_turn: str
    players: List[PlayerState]
    last_action: dict | None = None
    winner: str | None = None

    @classmethod
    def from_game(cls, game): #factory method that makes game engine more api friendly 
        return cls( #return a new gamestateresponce with the data in the paranthasis
            current_turn=game.get_current_player().name,
            players=[
                PlayerState(
                    name=p.name,
                    credits=p.credits,
                    cards=[c.role if not c.revealed else "❌" for c in p.cards],
                    alive=p.alive
                )
                for p in game.players
            ],
            last_action = game.action_chain[-1] if game.action_chain else None, # will pull full chain once we support UI history, rollback etc. 
            winner=getattr(game, "winner", None)
        )
