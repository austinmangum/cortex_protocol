import React, { useContext } from "react";
import { VStack, Box, Text } from "@chakra-ui/react";
import { GameContext } from "../state/gameContext";

const OpponentView: React.FC = () => {
  const context = useContext(GameContext);

  if (!context?.gameState) return null;

  const { gameState } = context;
  const opponents = gameState.players.filter(p => p.name !== "You");

  return (
    <VStack spacing={2} w="100%">
      {opponents.map((opponent, index) => (
        <Box key={index} borderWidth="1px" borderRadius="md" p={3} w="100%">
          <Text fontWeight="bold">{opponent.name}</Text>
          <Text>Credits: {opponent.credits}</Text>
          <Text>Cards: {opponent.cards.filter(() => false).length}</Text> {/* Hiding unrevealed cards */}
        </Box>
      ))}
    </VStack>
  );
};

export default OpponentView;
