import React from "react";
import { Button, HStack } from "@chakra-ui/react";
import { useGameActions } from "../state/useGameActions";

const ControlsPanel: React.FC = () => {
  const { income, coup } = useGameActions();

  return (
    <HStack spacing={4}>
      <Button onClick={income}>Income</Button>
      <Button onClick={() => coup("Bob")}>Coup Bob</Button>
    </HStack>
  );
};

export default ControlsPanel;
