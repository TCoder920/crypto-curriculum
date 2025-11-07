/** Progress tracking page */
import React, { useState, useEffect } from "react";
import { Box, Typography, CircularProgress, Alert, Card, CardContent, LinearProgress, Chip } from "@mui/material";
import { CheckCircle, School, TrendingUp } from "@mui/icons-material";
import { progressService } from "../services/progressService";
import type { Progress } from "../types/progress";

export const ProgressPage: React.FC = () => {
  const [progress, setProgress] = useState<Progress[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await progressService.getProgress();
      setProgress(response.progress);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to load progress");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "400px" }}>
        <CircularProgress sx={{ color: "white" }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ py: 4, px: 2 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  const completedCount = progress.filter((p) => p.status === "completed").length;
  const inProgressCount = progress.filter((p) => p.status === "in_progress").length;

  return (
    <Box
      sx={{
        py: 4,
        px: { xs: 1, sm: 2, md: 3 },
        maxWidth: "1400px",
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
        My Progress
      </Typography>

      {/* Summary Cards */}
      <Box sx={{ display: "flex", gap: 2, mb: 4, flexWrap: "wrap" }}>
        <Card
          sx={{
            background: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            flex: 1,
            minWidth: 200,
          }}
        >
          <CardContent>
            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
              <CheckCircle sx={{ color: "#4caf50", fontSize: 40 }} />
              <Box>
                <Typography variant="h4" sx={{ color: "white", fontWeight: 700 }}>
                  {completedCount}
                </Typography>
                <Typography variant="body2" sx={{ color: "rgba(255, 255, 255, 0.7)" }}>
                  Completed Modules
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card
          sx={{
            background: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            flex: 1,
            minWidth: 200,
          }}
        >
          <CardContent>
            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
              <TrendingUp sx={{ color: "#64b5f6", fontSize: 40 }} />
              <Box>
                <Typography variant="h4" sx={{ color: "white", fontWeight: 700 }}>
                  {inProgressCount}
                </Typography>
                <Typography variant="body2" sx={{ color: "rgba(255, 255, 255, 0.7)" }}>
                  In Progress
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Progress List */}
      {progress.length === 0 ? (
        <Card
          sx={{
            background: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            p: 4,
            textAlign: "center",
          }}
        >
          <Typography variant="body1" sx={{ color: "rgba(255, 255, 255, 0.7)" }}>
            No progress tracked yet. Start a module to begin tracking your progress!
          </Typography>
        </Card>
      ) : (
        <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
          {progress.map((p) => (
            <Card
              key={p.id}
              sx={{
                background: "rgba(255, 255, 255, 0.05)",
                backdropFilter: "blur(20px)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
              }}
            >
              <CardContent>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 2 }}>
                  <Typography variant="h6" sx={{ color: "white", fontWeight: 600 }}>
                    Module {p.module_id}
                  </Typography>
                  <Chip
                    label={p.status === "completed" ? "Completed" : p.status === "in_progress" ? "In Progress" : "Not Started"}
                    color={p.status === "completed" ? "success" : p.status === "in_progress" ? "primary" : "default"}
                    sx={{
                      background:
                        p.status === "completed"
                          ? "rgba(76, 175, 80, 0.2)"
                          : p.status === "in_progress"
                          ? "rgba(100, 181, 246, 0.2)"
                          : "rgba(255, 255, 255, 0.1)",
                      color:
                        p.status === "completed"
                          ? "#4caf50"
                          : p.status === "in_progress"
                          ? "#64b5f6"
                          : "rgba(255, 255, 255, 0.7)",
                      textTransform: "capitalize",
                    }}
                  />
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={p.completion_percentage}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    background: "rgba(255, 255, 255, 0.1)",
                    "& .MuiLinearProgress-bar": {
                      background:
                        p.status === "completed"
                          ? "linear-gradient(90deg, #4caf50 0%, #66bb6a 100%)"
                          : "linear-gradient(90deg, #64b5f6 0%, #90caf9 100%)",
                    },
                  }}
                />
                <Typography variant="body2" sx={{ color: "rgba(255, 255, 255, 0.7)", mt: 1 }}>
                  {p.completion_percentage.toFixed(0)}% Complete
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>
      )}
    </Box>
  );
};

