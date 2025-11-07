/** Module card component with Liquid Glass design */
import React from "react";
import { Card, CardContent, Typography, Box, Chip } from "@mui/material";
import { motion } from "framer-motion";
import { Lock as LockIcon } from "@mui/icons-material";
import type { Module } from "../../types/module";

interface ModuleCardProps {
  module: Module;
  onClick: () => void;
}

export const ModuleCard: React.FC<ModuleCardProps> = ({ module, onClick }) => {
  const isLocked = !module.can_access;

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.2 }}
    >
      <Card
        sx={{
          background: "rgba(255, 255, 255, 0.05)",
          backdropFilter: "blur(20px)",
          borderRadius: 3,
          border: "1px solid rgba(255, 255, 255, 0.1)",
          cursor: isLocked ? "not-allowed" : "pointer",
          opacity: isLocked ? 0.6 : 1,
          position: "relative",
          overflow: "hidden",
          width: "100%",
          maxWidth: "100%",
          height: "100%",
          "&::before": {
            content: '""',
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%)",
            pointerEvents: "none",
          },
          "&:hover": {
            background: "rgba(255, 255, 255, 0.08)",
            borderColor: "rgba(255, 255, 255, 0.2)",
          },
        }}
        onClick={isLocked ? undefined : onClick}
      >
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 2 }}>
            <Typography
              variant="h6"
              component="h3"
              sx={{
                fontWeight: 600,
                color: "white",
                flex: 1,
              }}
            >
              {module.title}
            </Typography>
            {isLocked && (
              <LockIcon
                sx={{
                  color: "rgba(255, 255, 255, 0.5)",
                  ml: 1,
                }}
              />
            )}
          </Box>

          {module.description && (
            <Typography
              variant="body2"
              sx={{
                color: "rgba(255, 255, 255, 0.7)",
                mb: 2,
                lineHeight: 1.6,
              }}
            >
              {module.description}
            </Typography>
          )}

          <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", alignItems: "center" }}>
            <Chip
              label={module.track}
              size="small"
              sx={{
                background: "rgba(255, 255, 255, 0.1)",
                color: "white",
                fontWeight: 500,
                textTransform: "capitalize",
              }}
            />
            <Chip
              label={`${module.duration_hours}h`}
              size="small"
              sx={{
                background: "rgba(255, 255, 255, 0.1)",
                color: "white",
              }}
            />
            {isLocked && module.missing_prerequisites && module.missing_prerequisites.length > 0 && (
              <Chip
                label={`Requires ${module.missing_prerequisites.length} prerequisite${module.missing_prerequisites.length > 1 ? "s" : ""}`}
                size="small"
                sx={{
                  background: "rgba(255, 193, 7, 0.2)",
                  color: "#ffc107",
                }}
              />
            )}
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

