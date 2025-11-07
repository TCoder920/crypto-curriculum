/** Settings page */
import React from "react";
import { Box, Typography, Card, CardContent, Switch, FormControlLabel, Divider } from "@mui/material";
import { useTheme } from "@mui/material/styles";

export const SettingsPage: React.FC = () => {
  const theme = useTheme();

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
        Settings
      </Typography>

      <Card
        sx={{
          background: "rgba(255, 255, 255, 0.05)",
          backdropFilter: "blur(20px)",
          border: "1px solid rgba(255, 255, 255, 0.1)",
        }}
      >
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h6" sx={{ color: "white", mb: 3, fontWeight: 600 }}>
            Appearance
          </Typography>

          <FormControlLabel
            control={<Switch defaultChecked={theme.palette.mode === "dark"} />}
            label="Dark Mode"
            sx={{
              color: "white",
              "& .MuiFormControlLabel-label": {
                color: "white",
              },
            }}
          />

          <Divider sx={{ my: 3, borderColor: "rgba(255, 255, 255, 0.1)" }} />

          <Typography variant="h6" sx={{ color: "white", mb: 3, fontWeight: 600 }}>
            Notifications
          </Typography>

          <FormControlLabel
            control={<Switch defaultChecked />}
            label="Email Notifications"
            sx={{
              color: "white",
              "& .MuiFormControlLabel-label": {
                color: "white",
              },
            }}
          />

          <FormControlLabel
            control={<Switch defaultChecked />}
            label="Module Completion Alerts"
            sx={{
              color: "white",
              "& .MuiFormControlLabel-label": {
                color: "white",
              },
            }}
          />
        </CardContent>
      </Card>
    </Box>
  );
};

