/** Layout component that wraps protected routes with header */
import React from "react";
import { Box } from "@mui/material";
import { Header } from "./Header";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", minHeight: "100vh", width: "100%", overflowX: "hidden" }}>
      <Header />
      <Box component="main" sx={{ flex: 1, background: "transparent", width: "100%", overflowX: "hidden" }}>
        {children}
      </Box>
    </Box>
  );
};

