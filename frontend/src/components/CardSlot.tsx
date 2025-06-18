import React from "react";
import { Box, Text } from "@chakra-ui/react";

interface Props {
  role?: string;
  hidden?: boolean;
}

const CardSlot: React.FC<Props> = ({ role, hidden }) => {
  return (
    <Box border="1px solid" borderRadius="md" padding={2} width={20} textAlign="center">
      <Text>{hidden ? "🕶️" : role}</Text>
    </Box>
  );
};

export default CardSlot;
