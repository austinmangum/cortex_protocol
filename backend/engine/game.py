from typing import List, Optional
import random
from .player import Player, Card
from . import card_definitions
from .card_definitions import *


class Game:
    def __init__(self, player_names: List[str], roles: List[str]):
        self.action_chain = []
        self.players: List[Player] = [Player(name) for name in player_names]
        self.deck: List[Card] = [Card(role) for role in roles * 3]  # 3 of each role
        random.shuffle(self.deck)

        # Deal 2 cards to each player
        for player in self.players:
            for _ in range(2):
                player.add_card(self.deck.pop())

        self.current_turn = 0

    def register_action(self, action_type: str, player_name: str, role: Optional[str] = None, target_name: Optional[str] = None, meta=None):
        action = {
            "type": action_type,           # claim, block, challenge, etc.
            "player": player_name,
            "role": role,
            "target": target_name,
            #"meta": meta or {},
            "status": "pending"
        }
        self.action_chain.append(action)
        return action

    def get_last_action_of_type(self, action_type: str):
        for action in reversed(self.action_chain):
            if action["type"] == action_type:
                return action
        return None





    def get_current_player(self):
        return self.players[self.current_turn]

    def next_turn(self):
        alive_players = [p for p in self.players if p.alive] # gets a list of all alive players
        idx = alive_players.index(self.get_current_player()) # finds the location of the current player in the list
        self.current_turn = self.players.index(alive_players[(idx + 1) % len(alive_players)]) #moved turn to next alive player. Modulo to loop back to start

    def perform_income(self):
        player = self.get_current_player()
        player.credits += 1
        self.next_turn()

    def perform_coup(self, target_name: str):
        player = self.get_current_player()
        if player.credits < 7: #check to see if enough credits 
            raise Exception("Not enough credits to coup")
        player.credits -= 7 #remove credits from pool
        target = next(p for p in self.players if p.name == target_name and p.alive)
        if not target:
            raise Exception(f"Invalid target: {target_name} is not an active player")
        target.lose_card()
        self.next_turn()

    def claim_action(self, role: str, target_name: Optional[str] = None):
        player = self.get_current_player()
        return self.register_action("claim", player.name, role, target_name)
    
    def challenge(self, challenger_name: str):
        challenge_target = self.get_last_action_of_type("block") or self.get_last_action_of_type("claim")
        if not challenge_target:
            return "No claim or block to challenge."

        challenged_player = next((p for p in self.players if p.name == challenge_target["player"] and p.alive), None)
        if not challenged_player:
            return f"{challenge_target["player"]} in not alive or not a valid target"
        challenger = next((p for p in self.players if p.name == challenger_name), None)
        claimed_role = challenge_target["role"]

        if challenged_player.has_role(claimed_role):
            # Challenger loses
            challenged_player.lose_card(claimed_role)
            challenged_player.add_card(self.deck.pop())
            challenger.lose_card()
            challenge_target["status"] = "validated"
            return f"{challenger.name} failed the challenge. {challenged_player.name} shows {claimed_role}."
        else:
            # Actor loses
            challenged_player.lose_card()
            challenge_target["status"] = "failed"
            return f"{challenged_player.name} was bluffing. {challenger.name} wins the challenge."
            
    def block(self, blocker_name: str, blocking_role: str):
        return self.register_action("block", blocker_name, blocking_role, self.get_current_player().name)

    def resolve_next_action(self):
    # Find the last validated or unchallenged claim
        for i in range(len(self.action_chain)):
            action = self.action_chain[i]

            if action["type"] == "claim" and action.get("status") in (None, "pending", "validated"):
                actor_name = action["player"]
                actor = next((p for p in self.players if p.name == actor_name and p.alive), None)
                if not actor:
                    return f"{actor_name} is no longer alive."

                role = action["role"]
                target_name = action.get("target")
                target = next((p for p in self.players if p.name == target_name and p.alive), None) if target_name else None

                role_info = ROLE_DEFINITIONS.get(role)
                if not role_info:
                    return f"{role} is not a valid role."

                action_name = role_info.get("action")
                if not action_name:
                    return f"{role} has no associated action."

                # 🔍 Check for a block directly after this claim
                if i + 1 < len(self.action_chain):
                    maybe_block = self.action_chain[i + 1]
                    if maybe_block["type"] == "block" and maybe_block.get("target") == actor_name:
                        block_status = maybe_block.get("status")
                        blocking_role = maybe_block.get("role")
                        blocker_name = maybe_block.get("player")

                        blocker_info = ROLE_DEFINITIONS.get(blocking_role)
                        blocked_actions = blocker_info.get("blocks", []) if blocker_info else []

                        # Only block if it’s a valid blocker of this action
                        if action_name in blocked_actions:
                            if block_status in (None, "pending", "validated"):
                                action["status"] = "blocked"
                                self.next_turn()
                                return f"{actor_name}'s action was blocked by {blocker_name} using {blocking_role}."
                            elif block_status == "failed":
                                pass  # block failed, continue to resolve claim
                        else:
                            # Block exists but isn't valid for this action
                            return f"{blocking_role} cannot block action {action_name}. Invalid block."

                # ✅ No block or block failed — resolve claim
                resolver = getattr(card_definitions, action_name, None)
                if not callable(resolver):
                    return f"No resolver found for action: {action_name}"

                result = resolver(self, actor, target)
                action["status"] = "resolved"
                self.next_turn()
                return result

        return "No claim action ready to resolve."

    def __repr__(self):
        return "\n".join(str(player) for player in self.players)
