#game runner used to allow tests to be ran on the backend via CLI instead of API. Used durring initial building og game logic
from backend.engine.game import Game
from backend.engine.card_definitions import ROLE_DEFINITIONS
import sys
import os
#BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.insert(0, BASE_DIR)
#print("PYTHON PATH:", sys.path)


def log_event(event_type: str, data: dict):
    print(f"\n🔔 EVENT: {event_type} - " + ", ".join(f"{k}: {v}" for k, v in data.items()))

def prompt_player_action(game: Game):
    current_player = game.get_current_player()
    print(f"\n🎮 {current_player.name}'s turn")
    print(f"Credits: {current_player.credits}")
    print(f"Cards: {current_player.cards}")

    print("\nAvailable actions:")
    print("[1] Claim a role")
    print("[2] Take Income (gain 1 credit)")
    print("[3] Coup (pay 7 credits to eliminate a card)")

    choice = input("Enter the number of your action: ")

    if choice == "1":
        print("\nAvailable roles to claim:")
        roles = list(ROLE_DEFINITIONS.keys())
        for i, role in enumerate(roles):
            print(f"[{i}] {role} - Action: {ROLE_DEFINITIONS[role].get('action', 'None')}")
        role_idx = int(input("Enter the number of the role to claim: "))
        role = roles[role_idx]

        alive_players = [p for p in game.players if p.alive and p.name != current_player.name]
        if alive_players:
            print("\nSelect a target (if applicable):")
            for i, player in enumerate(alive_players):
                print(f"[{i}] {player.name}")
            target_choice = input("Enter the number of the target player or leave blank: ").strip()
            target = alive_players[int(target_choice)].name if target_choice else None
        else:
            target = None

        game.claim_action(role, target)
        log_event("action_claimed", {"player": current_player.name, "role": role, "target": target or "None"})

    elif choice == "2":
        game.perform_income()
        log_event("income_taken", {"player": current_player.name, "credits": current_player.credits})

    elif choice == "3":
        alive_targets = [p for p in game.players if p.alive and p.name != current_player.name]
        if not alive_targets:
            print("❌ No valid targets to coup.")
            return

        print("\nWho do you want to coup?")
        for i, player in enumerate(alive_targets):
            print(f"[{i}] {player.name}")
        target_idx = int(input("Enter the number of the target: "))
        target = alive_targets[target_idx].name

        try:
            game.perform_coup(target)
            log_event("coup_performed", {"by": current_player.name, "target": target})
        except Exception as e:
            print(f"❌ Invalid coup: {e}")
            prompt_player_action(game)  # Retry
    else:
        print("❌ Invalid choice")
        prompt_player_action(game)

def prompt_block(game: Game):
    print("\nDoes anyone want to block the last action?")
    alive_players = [p for p in game.players if p.alive]
    for i, player in enumerate(alive_players):
        print(f"[{i}] {player.name}")
    blocker_choice = input("Enter the number of the blocker or leave blank: ").strip()

    if blocker_choice:
        blocker = alive_players[int(blocker_choice)]
        print("\nAvailable blocking roles:")
        roles = list(ROLE_DEFINITIONS.keys())
        for i, role in enumerate(roles):
            print(f"[{i}] {role}")
        role_choice = int(input("Enter the number of the blocking role: "))
        block_role = roles[role_choice]

        game.block(blocker.name, block_role)
        log_event("action_blocked", {"player": blocker.name, "role": block_role})

def prompt_challenge(game: Game):
    print("\nDoes anyone want to challenge the last action or block?")
    alive_players = [p for p in game.players if p.alive]
    for i, player in enumerate(alive_players):
        print(f"[{i}] {player.name}")
    challenge_choice = input("Enter the number of the challenger or leave blank: ").strip()

    if challenge_choice:
        challenger = alive_players[int(challenge_choice)]
        result = game.challenge(challenger.name)
        log_event("challenge_resolved", {"result": result})
        print(f"⚔️ Challenge Result: {result}")

def check_game_over(game: Game):
    alive_players = [p for p in game.players if p.alive]
    if len(alive_players) == 1:
        winner = alive_players[0]
        log_event("game_over", {"winner": winner.name})
        print(f"\n🏆 {winner.name} wins the game!")
        return True
    return False

def main():
    player_names = input("Enter player names, comma-separated: ").split(",")
    player_names = [name.strip() for name in player_names if name.strip()]
    if len(player_names) < 2:
        print("❌ Need at least 2 players to start.")
        return

    roles = list(ROLE_DEFINITIONS.keys())
    game = Game(player_names, roles)

    while True:
        print("\n====================")
        print(game)
        print("====================")

        prompt_player_action(game)

        if game.action_chain and game.action_chain[-1]["type"] == "claim":
            prompt_block(game)
            prompt_challenge(game)

        result = game.resolve_next_action()
        log_event("action_resolved", {"outcome": result})
        print(f"🧠 Resolution: {result}")

        if check_game_over(game):
            break

if __name__ == "__main__":
    main()