import React, { useContext } from "react";
import { Text } from "@chakra-ui/react";
import { GameContext } from "../state/gameContext";

const TurnBanner: React.FC = () => {
  const { gameState } = useContext(GameContext);

  return (
    <Text fontSize="xl" fontWeight="bold">
      Current Turn: {gameState?.current_turn ?? "Loading..."}
    </Text>
  );
};

export default TurnBanner;
