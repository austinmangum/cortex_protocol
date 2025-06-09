from typing import Callable, Optional

# Each resolver should follow this signature:
# <action name>(game, actor: Player, target: Optional[Player]) -> str

def tax (game, actor, target=None): # Resolve CEO
    actor.credits += 3
    return f"{actor.name} gains 3 credits with CEO."

def steal (game, actor, target): # Resolve Black Hat
    if not target: #Encase target isn't passed
        return f"{actor.name} tried to steal but no target was selected"
    if target.credits < 2: #encase target has less than 2 credits
        actor.credits += target.credits
        target.credits = 0
    target.credits -= 2
    actor.credits += 2

def assassinate (game, actor, target): # Resolve Assissin
    if actor.credit < 3:
        return f"{actor.name} tried to assassinate but didn't have enough credits."
    if not target:
        return f"{actor.name} tried to assassinate but no target was specified."
    actor.credits -= 3
    target.lose_card()
    return f"{actor.name} pays 3 credits to assassinate {target.name}."
#right now, players switch the first non revealed card, eventaully want players to choose
def swap (game, actor, target): # Resolve Replcaer
    if not target:
        return f"{actor.name} tried to swap, but no target was specified."
    a_card = next((c for c in actor.cards if not c.revealed), None)
    t_card = next((c for c in target.cards if not c.revealed), None)
    if not a_card or not t_card:
        return f"{actor.name} could not complete the swap. One of the players has no hidden cards."
    a_card.role, t_card.role = t_card.role, a_card.role
    return f"{actor.name} swaps one card with {target.name}."





ROLE_DEFINITIONS = {
    "CEO": {
        "action": "tax",
        "blocks": []
    },
    "Black Hat": {
        "action": "steal",
        "blocks": []
        
    },
    "Firewall": {
        "action": None,
        "blocks": ["steal", "swap"]
    },
    "Assassin": {
        "action": "assassinate",
        "blocks": [],
        "cost": 3
    },
    "Replacer": {
        "action": "swap",
        "blocks": [],

    },
    "Ghost": {
        "action": None,
        "blocks": ["assassinate"]
    }
}
