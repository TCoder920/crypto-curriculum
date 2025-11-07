/** User profile page */
import React from "react";
import { Box, Typography, Card, CardContent, Avatar, Chip } from "@mui/material";
import { useAuth } from "../contexts/AuthContext";

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <Box
      sx={{
        py: 4,
        px: { xs: 1, sm: 2, md: 3 },
        maxWidth: "800px",
        mx: "auto",
        width: "100%",
        overflowX: "hidden",
      }}
    >
      <Typography
        variant="h4"
        component="h1"
        sx={{
          fontWeight: 700,
          color: "white",
          mb: 4,
        }}
      >
        Profile
      </Typography>

      <Card
        sx={{
          background: "rgba(255, 255, 255, 0.05)",
          backdropFilter: "blur(20px)",
          border: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      >
        <CardContent sx={{ p: 4 }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 3, mb: 4 }}>
            <Avatar
              sx={{
                width: 80,
                height: 80,
                bgcolor: "primary.main",
                fontSize: "2rem",
              }}
            >
              {user?.full_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || "U"}
            </Avatar>
            <Box>
              <Typography variant="h5" sx={{ color: "white", fontWeight: 600, mb: 1 }}>
                {user?.full_name || user?.username || "User"}
              </Typography>
              <Typography variant="body1" sx={{ color: "rgba(255, 255, 255, 0.7)", mb: 1 }}>
                {user?.email}
              </Typography>
              <Chip
                label={user?.role || "student"}
                sx={{
                  background: "rgba(100, 181, 246, 0.2)",
                  color: "#64b5f6",
                  textTransform: "capitalize",
                }}
              />
            </Box>
          </Box>

          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <Box>
              <Typography variant="body2" sx={{ color: "rgba(255, 255, 255, 0.5)", mb: 0.5 }}>
                Username
              </Typography>
              <Typography variant="body1" sx={{ color: "white" }}>
                {user?.username || "Not set"}
              </Typography>
            </Box>

            <Box>
              <Typography variant="body2" sx={{ color: "rgba(255, 255, 255, 0.5)", mb: 0.5 }}>
                Full Name
              </Typography>
              <Typography variant="body1" sx={{ color: "white" }}>
                {user?.full_name || "Not set"}
              </Typography>
            </Box>

            <Box>
              <Typography variant="body2" sx={{ color: "rgba(255, 255, 255, 0.5)", mb: 0.5 }}>
                Role
              </Typography>
              <Typography variant="body1" sx={{ color: "white", textTransform: "capitalize" }}>
                {user?.role || "student"}
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

