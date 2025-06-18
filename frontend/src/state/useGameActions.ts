import { useContext } from "react";
import axios from "axios";
import { GameContext } from "./gameContext";

export const useGameActions = () => {
  const { setGameState } = useContext(GameContext);

  const income = async () => {
    const res = await axios.post("/game/income", { player: "You" });
    setGameState(res.data);
  };

  const coup = async (target: string) => {
    const res = await axios.post("/game/coup", { player: "You", target });
    setGameState(res.data);
  };

  return { income, coup };
};
