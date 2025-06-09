from engine.game import Game
from backend.engine.card_definitions import ROLE_DEFINITIONS

def log_event(event_type: str, data: dict):
    print(f"\n🔔 EVENT: {event_type} - " + ", ".join(f"{k}: {v}" for k, v in data.items()))

def prompt_player_action(game: Game):
    current_player = game.get_current_player()
    print(f"\n🎮 {current_player.name}'s turn")
    print(f"Credits: {current_player.credits}")
    print(f"Cards: {current_player.cards}")

    print("\nActions:")
    print("1. Claim a role")
    print("2. Income (gain 1 credit)")
    print("3. Coup (pay 7 credits to eliminate a card)")

    choice = input("Choose an action: ")

    if choice == "1":
        print("\nAvailable roles:")
        for role in ROLE_DEFINITIONS:
            print(f"- {role} (action: {ROLE_DEFINITIONS[role].get('action')})")

        role = input("Claim a role: ")
        target = input("Target player (or leave blank): ").strip() or None
        game.claim_action(role, target)
        log_event("action_claimed", {"player": current_player.name, "role": role, "target": target or "None"})

    elif choice == "2":
        game.perform_income()
        log_event("income_taken", {"player": current_player.name, "credits": current_player.credits})

    elif choice == "3":
        target = input("Who do you want to coup? ")
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
    blocker_name = input("Anyone want to block? Enter name or leave blank: ").strip()
    if blocker_name:
        block_role = input(f"What role is {blocker_name} claiming to block with? ")
        game.block(blocker_name, block_role)
        log_event("action_blocked", {"player": blocker_name, "role": block_role})

def prompt_challenge(game: Game):
    challenger_name = input("Anyone want to challenge the last action or block? Enter name or leave blank: ").strip()
    if challenger_name:
        result = game.challenge(challenger_name)
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

        # If the last action was a claim, offer block/challenge
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