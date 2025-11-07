/** Homepage component with module list */
import React from "react";
import { Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { ModuleList } from "../components/modules/ModuleList";

export const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleModuleClick = (moduleId: number) => {
    navigate(`/modules/${moduleId}`);
  };

  return (
    <Box
      sx={{
        py: 4,
        px: { xs: 1, sm: 2, md: 3 },
        maxWidth: "1400px",
        mx: "auto",
        minHeight: "100vh",
        background: "transparent",
        width: "100%",
        overflowX: "hidden",
      }}
    >
      <ModuleList onModuleClick={handleModuleClick} />
    </Box>
  );
};

