import React, { useContext } from "react";
import { VStack, Box, Text } from "@chakra-ui/react";
import { GameContext } from "../state/gameContext";

const PlayerView: React.FC = () => {
  const context = useContext(GameContext);

  if (!context?.gameState) return null;

  const { gameState } = context;
  const player = gameState.players.find(p => p.name === "You");

  if (!player) return null;

  return (
    <VStack spacing={2} w="100%" borderTop="1px solid #ccc" pt={4}>
      <Text fontSize="lg" fontWeight="bold">Your Info</Text>
      <Box borderWidth="1px" borderRadius="md" p={3} w="100%">
        <Text>Credits: {player.credits}</Text>
        <Text>Cards:</Text>
        {player.cards.map((card: string, idx: number) => (
          <Text key={idx}>- {card}</Text>
        ))}
      </Box>
    </VStack>
  );
};

export default PlayerView;
