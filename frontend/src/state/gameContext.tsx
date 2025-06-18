import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

interface Player {
  name: string;
  credits: number;
  cards: string[];
  alive: boolean;
}

interface GameState {
  current_turn: string;
  players: Player[];
  last_action: any; // You can refine this later
  winner: string | null;
}

interface GameContextType {
  gameState: GameState | null;
  setGameState: React.Dispatch<React.SetStateAction<GameState | null>>;
}

export const GameContext = createContext<GameContextType | null>(null);

export const GameProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [gameState, setGameState] = useState<GameState | null>(null);

  useEffect(() => {
    console.log("📡 Starting game initialization...");

    axios.post("/game/start", {
      player_names: ["You", "Bob"]
    })
    .then(res => {
      console.log("🎯 Game data received:", res.data);
      setGameState(res.data);
    })
    .catch(err => {
      console.error("❌ Failed to start game:", err);
    });
  }, []);

  return (
    <GameContext.Provider value={{ gameState, setGameState }}>
      {children}
    </GameContext.Provider>
  );
};
