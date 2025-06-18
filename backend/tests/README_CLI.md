# 🧪 Cortex Protocol – CLI Test Runner

This CLI tool lets you simulate a full game of **Cortex Protocol** using your current backend engine. It's perfect for testing game mechanics (claims, blocks, challenges, coups, etc.) before building the web frontend.

---

## 🚀 How to Run

1. **Navigate to the backend folder**:

   ```bash
   cd backend/cli
   ```

2. **Run the CLI game**:

   ```bash
   python game_runner.py
   ```

   Make sure you're using Python 3.8+.

---

## 🎮 Game Flow Overview

The game starts by asking for **player names** (minimum 2):

```
Enter player names, comma-separated: Alice, Bob, Charlie
```

Each round, the current player is prompted with:

```
🎮 Alice's turn
Credits: 2
Cards: 🕶️ CEO, 🕶️ Black Hat

Actions:
1. Claim a role
2. Income (gain 1 credit)
3. Coup (pay 7 credits to eliminate a card)
```

---

## 🧠 Actions & Phases

### 1️⃣ Claim a Role

- Choose a role to claim and an optional target (for actions like steal or assassinate)
- Example:
  ```
  Claim a role: CEO
  Target player (or leave blank): 
  ```

### 2️⃣ Income

- Automatically gives the player +1 credit
- Cannot be blocked or challenged

### 3️⃣ Coup

- Costs 7 credits
- Prompts you to choose another player to lose a card
- Cannot be blocked or challenged

---

## 🛡️ Blocking Phase

After a claim, players are asked:

```
Anyone want to block? Enter name or leave blank:
```

- The blocker must specify their role (e.g., Firewall to block Steal)
- Blocks can be challenged

---

## ⚔️ Challenge Phase

After a claim or block, players are asked:

```
Anyone want to challenge the last action or block? Enter name or leave blank:
```

- If the challenge succeeds, the bluffing player loses a card
- If the challenge fails, the challenger loses a card and the original action proceeds

---

## 🔁 Turn Resolution

After claim/block/challenge phases are completed:

- The game auto-resolves the action using `resolve_next_action()`
- It determines if the action succeeded, was blocked, or if a challenge changed the outcome

---

## 🏆 Endgame

When only one player remains alive:

```
🏆 Alice wins the game!
```

The game ends, and the CLI exits.

---

## 🔔 Event Logging

During the game, structured events are printed:

```
🔔 EVENT: action_claimed - player: Alice, role: CEO, target: None
🔔 EVENT: action_blocked - player: Bob, role: Firewall
🔔 EVENT: challenge_resolved - result: Bob failed the challenge and lost a card.
🔔 EVENT: action_resolved - outcome: Alice gains 3 credits by claiming Tax.
```

These events simulate how a frontend might listen for real-time game state changes.

---

## 🔧 Developer Tips

- You can modify `card_definitions.py` to test custom roles and abilities
- You can change `game_runner.py` to skip human input and simulate bots
- Look into `game.action_chain` for debugging the full history of events

---

## 🧩 Coming Next

Want to:
- Log the game to a file?
- Simulate random players?
- Connect to a frontend via WebSocket?

Let us know in the issues or keep building!
