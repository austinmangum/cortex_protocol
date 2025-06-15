#this file hold a live instance of the game engine and is the bridge between the api calls and the actual game. 
#it also provides public methods needed to interact with the engine without exposing the engine directly so we can sanitise/check inputs

from backend.app.engine.game import Game
from backend.app.models.schemas import StartGameRequest, GameStateResponse

class GameStore:
    def __init__(self):
        self.game = None

    def start_new_game(self, data: StartGameRequest) -> GameStateResponse:
        self.game = Game(data.player_names, data.roles)
        return self.get_current_state()

    def get_current_state(self) -> GameStateResponse:
        if not self.game:
            raise Exception("No game in progress")
        return GameStateResponse.from_game(self.game)
    
    def claim_action(self, data):
        if not self.game:
            raise Exception("No game in progress")
        if data.player != self.game.get_current_player().name:
            raise Exception(f"It is not {data.player}'s turn")
        self.game.claim_action(data.role, data.target)

    def block_action(self, data):
        if not self.game:
            raise Exception("No game in progress")
        self.game.block(data.blocker, data.blocking_role)

    def challenge_action(self, data):
        if not self.game:
            raise Exception("No game in progress")
        return self.game.challenge(data.challenger)

    def resolve_next(self):
        if not self.game:
            raise Exception("No game in progress")
        self.game.resolve_next_action()
