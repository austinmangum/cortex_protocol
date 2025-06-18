# run "python -m uvicorn backend.app.main:app --reload" to sstart server locally
# then run "python tests/test_cortex_protocol_api.py" in the command line to test 

import requests

BASE_URL = "http://localhost:8000/game"

def print_result(label, response):
    print(f"\n--- {label} ---")
    print(response.json())

def test_game_flow():
    # Start the game
    res = requests.post(f"{BASE_URL}/start", json={
        "player_names": ["Alice", "Bob"],
        "roles": ["CEO", "Black Hat", "Firewall", "Assassin", "Replacer", "Ghost"]
    })
    print_result("Game Started", res)

    # === 1. CEO: Claim tax (unblocked, unchallenged) ===
    res = requests.post(f"{BASE_URL}/action", json={
        "player": "Alice",
        "role": "CEO",
        "action": "tax",
        "target": None
    })
    print_result("Alice claims CEO tax", res)

    res = requests.post(f"{BASE_URL}/resolve", json={})
    print_result("Resolve CEO tax", res)

    # === 2. Black Hat: Claim steal, blocked by Firewall ===
    res = requests.post(f"{BASE_URL}/action", json={
        "player": "Bob",
        "role": "Black Hat",
        "action": "steal",
        "target": "Alice"
    })
    print_result("Bob claims steal", res)

    res = requests.post(f"{BASE_URL}/block", json={
        "player": "Alice",
        "role": "Firewall",
        "action": "steal"
    })
    print_result("Alice blocks with Firewall", res)

    res = requests.post(f"{BASE_URL}/resolve", json={})
    print_result("Resolve steal (blocked)", res)

    # === 3. Assassin: Claim assassinate, challenged ===
    res = requests.post(f"{BASE_URL}/action", json={
        "player": "Alice",
        "role": "Assassin",
        "action": "assassinate",
        "target": "Bob"
    })
    print_result("Alice claims assassinate", res)

    res = requests.post(f"{BASE_URL}/challenge", json={
        "challenger": "Bob"
    })
    print_result("Bob challenges Assassin", res)

    res = requests.post(f"{BASE_URL}/resolve", json={})
    print_result("Resolve assassinate (challenged)", res)

    # === 4. Replacer: Swap, blocked, block is challenged and fails ===
    res = requests.post(f"{BASE_URL}/action", json={
        "player": "Bob",
        "role": "Replacer",
        "action": "swap",
        "target": "Alice"
    })
    print_result("Bob claims Replacer swap", res)

    res = requests.post(f"{BASE_URL}/block", json={
        "player": "Alice",
        "role": "Firewall",
        "action": "swap"
    })
    print_result("Alice blocks swap with Firewall", res)

    res = requests.post(f"{BASE_URL}/challenge", json={
        "challenger": "Bob"
    })
    print_result("Bob challenges block (fails)", res)

    res = requests.post(f"{BASE_URL}/resolve", json={})
    print_result("Resolve swap (block failed)", res)

    # === 5. Replacer: Swap, blocked, block is challenged and succeeds ===
    res = requests.post(f"{BASE_URL}/action", json={
        "player": "Bob",
        "role": "Replacer",
        "action": "swap",
        "target": "Alice"
    })
    print_result("Bob claims swap again", res)

    res = requests.post(f"{BASE_URL}/block", json={
        "player": "Alice",
        "role": "Ghost",  # Ghost does NOT block swap (invalid)
        "action": "swap"
    })
    print_result("Alice tries to block with Ghost", res)

    res = requests.post(f"{BASE_URL}/challenge", json={
        "challenger": "Bob"
    })
    print_result("Bob challenges block (succeeds)", res)

    res = requests.post(f"{BASE_URL}/resolve", json={})
    print_result("Resolve swap (block succeeded)", res)


if __name__ == "__main__":
    test_game_flow()
