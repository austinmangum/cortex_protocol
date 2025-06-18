import React, { useContext } from "react";
import { VStack, Heading, Text, Spinner } from "@chakra-ui/react";
import TurnBanner from "./TurnBanner";
import OpponentView from "./OpponentView";
import PlayerView from "./PlayerView";
import { GameContext } from "../state/gameContext";

const GameBoard: React.FC = () => {
  const context = useContext(GameContext);

  if (!context) {
    return (
      <VStack spacing={4} p={4} align="center">
        <Heading size="md">Game context not available</Heading>
        <Text>Something went wrong. Please try again later.</Text>
      </VStack>
    );
  }

  const { gameState } = context;

  // Handle loading state
  if (!gameState) {
    return (
      <VStack spacing={4} p={4} align="center">
        <Spinner size="xl" />
        <Text>Loading game...</Text>
      </VStack>
    );
  }

  // Optionally, handle edge case where gameState fails to load players or required structure
  if (!gameState.players || gameState.players.length === 0) {
    return (
      <VStack spacing={4} p={4} align="center">
        <Heading size="md">Failed to load game data.</Heading>
        <Text>Please refresh or try again later.</Text>
      </VStack>
    );
  }

  return (
    <VStack spacing={4} p={4}>
      <TurnBanner />
      <OpponentView />
      <PlayerView />
    </VStack>
  );
};

export default GameBoard;
