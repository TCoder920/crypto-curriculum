/** Module detail page with lessons */
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Box, Typography, CircularProgress, Alert, Button, List, ListItem, ListItemButton, ListItemText, Chip } from "@mui/material";
import { CheckCircle, ArrowBack } from "@mui/icons-material";
import { moduleService } from "../services/moduleService";
import { progressService } from "../services/progressService";
import { LessonViewer } from "../components/modules/LessonViewer";
import type { ModuleDetail, Lesson } from "../types/module";
import type { Progress } from "../types/progress";

export const ModulePage: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const navigate = useNavigate();
  const [module, setModule] = useState<ModuleDetail | null>(null);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    if (moduleId) {
      loadModule(parseInt(moduleId));
    }
  }, [moduleId]);

  const loadModule = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      const data = await moduleService.getModule(id);
      setModule(data);
      
      // Select first lesson by default
      if (data.lessons && data.lessons.length > 0) {
        setSelectedLesson(data.lessons[0]);
      }
      
      // Load progress (404 is expected if progress doesn't exist yet)
      try {
        const progressData = await progressService.getModuleProgress(id);
        setProgress(progressData);
      } catch (err: any) {
        // 404 means progress doesn't exist yet, that's okay
        if (err.response?.status === 404) {
          setProgress(null);
        } else {
          // Other errors might be worth logging but not blocking
          setProgress(null);
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to load module");
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteModule = async () => {
    if (!module) return;
    
    try {
      setCompleting(true);
      const updatedProgress = await progressService.completeModule(module.id);
      setProgress(updatedProgress);
      
      // Reload module to update lock status
      await loadModule(module.id);
      
      // Trigger a custom event to refresh module list on homepage
      window.dispatchEvent(new CustomEvent("moduleCompleted", { detail: { moduleId: module.id } }));
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to complete module");
    } finally {
      setCompleting(false);
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
      <Box sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate("/")}
          sx={{
            color: "white",
            borderColor: "rgba(255, 255, 255, 0.3)",
            "&:hover": {
              borderColor: "rgba(255, 255, 255, 0.5)",
              background: "rgba(255, 255, 255, 0.05)",
            },
          }}
          variant="outlined"
        >
          Back to Modules
        </Button>
      </Box>
    );
  }

  if (!module) {
    return null;
  }

  if (!module.can_access) {
    return (
      <Box sx={{ py: 4 }}>
        <Alert severity="warning" sx={{ mb: 3 }}>
          This module requires completion of prerequisite modules: {module.missing_prerequisites?.join(", ")}
        </Alert>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate("/")}
          sx={{
            color: "white",
            borderColor: "rgba(255, 255, 255, 0.3)",
            "&:hover": {
              borderColor: "rgba(255, 255, 255, 0.5)",
              background: "rgba(255, 255, 255, 0.05)",
            },
          }}
          variant="outlined"
        >
          Back to Modules
        </Button>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        py: 4,
        px: { xs: 1, sm: 2, md: 3 },
        minHeight: "100vh",
        background: "transparent",
        width: "100%",
        maxWidth: "100%",
        overflowX: "hidden",
      }}
    >

      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 2 }}>
        <Typography
          variant="h4"
          component="h1"
          sx={{
            fontWeight: 700,
            color: "white",
            flex: 1,
          }}
        >
          {module.title}
        </Typography>
        {progress?.status === "completed" ? (
          <Chip
            icon={<CheckCircle />}
            label="Completed"
            color="success"
            sx={{
              ml: 2,
              background: "rgba(76, 175, 80, 0.2)",
              color: "#4caf50",
              border: "1px solid rgba(76, 175, 80, 0.3)",
            }}
          />
        ) : (
          <Button
            variant="contained"
            startIcon={<CheckCircle />}
            onClick={handleCompleteModule}
            disabled={completing}
            sx={{
              ml: 2,
              background: "rgba(100, 181, 246, 0.2)",
              color: "#64b5f6",
              border: "1px solid rgba(100, 181, 246, 0.3)",
              "&:hover": {
                background: "rgba(100, 181, 246, 0.3)",
              },
            }}
          >
            {completing ? "Completing..." : "Mark as Complete"}
          </Button>
        )}
      </Box>

      {module.description && (
        <Typography
          variant="body1"
          sx={{
            color: "rgba(255, 255, 255, 0.7)",
            mb: 4,
            lineHeight: 1.8,
          }}
        >
          {module.description}
        </Typography>
      )}

      <Box
        sx={{
          display: "flex",
          gap: { xs: 2, md: 4 },
          flexDirection: { xs: "column", lg: "row" },
          width: "100%",
          maxWidth: "100%",
          overflowX: "hidden",
        }}
      >
        {/* Lesson List Sidebar */}
        <Box
          sx={{
            width: { xs: "100%", lg: 300 },
            minWidth: 0,
            maxWidth: { xs: "100%", lg: 300 },
            background: "rgba(255, 255, 255, 0.05)",
            backdropFilter: "blur(20px)",
            borderRadius: 3,
            border: "1px solid rgba(255, 255, 255, 0.1)",
            p: 2,
            height: "fit-content",
            maxHeight: "calc(100vh - 200px)",
            overflowY: "auto",
            overflowX: "hidden",
          }}
        >
          <Typography
            variant="h6"
            sx={{
              fontWeight: 600,
              color: "white",
              mb: 2,
            }}
          >
            Lessons
          </Typography>
          <List sx={{ p: 0 }}>
            {module.lessons.map((lesson) => (
              <ListItem key={lesson.id} disablePadding sx={{ mb: 1 }}>
                <ListItemButton
                  onClick={() => setSelectedLesson(lesson)}
                  selected={selectedLesson?.id === lesson.id}
                  sx={{
                    borderRadius: 2,
                    background: selectedLesson?.id === lesson.id ? "rgba(255, 255, 255, 0.1)" : "transparent",
                    "&:hover": {
                      background: "rgba(255, 255, 255, 0.05)",
                    },
                    "&.Mui-selected": {
                      background: "rgba(255, 255, 255, 0.1)",
                      "&:hover": {
                        background: "rgba(255, 255, 255, 0.15)",
                      },
                    },
                  }}
                >
                  <ListItemText
                    primary={lesson.title}
                    secondary={lesson.estimated_minutes ? `${lesson.estimated_minutes} min` : null}
                    primaryTypographyProps={{
                      sx: {
                        color: "white",
                        fontSize: "0.9rem",
                        fontWeight: selectedLesson?.id === lesson.id ? 600 : 400,
                      },
                    }}
                    secondaryTypographyProps={{
                      sx: {
                        color: "rgba(255, 255, 255, 0.5)",
                        fontSize: "0.75rem",
                      },
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>

        {/* Lesson Content */}
        <Box sx={{ flex: 1, minWidth: 0, maxWidth: "100%", overflowX: "hidden" }}>
          {selectedLesson ? (
            <LessonViewer lesson={selectedLesson} />
          ) : (
            <Box
              sx={{
                background: "rgba(255, 255, 255, 0.05)",
                backdropFilter: "blur(20px)",
                borderRadius: 3,
                border: "1px solid rgba(255, 255, 255, 0.1)",
                p: 4,
                textAlign: "center",
              }}
            >
              <Typography variant="body1" sx={{ color: "rgba(255, 255, 255, 0.7)" }}>
                Select a lesson to begin
              </Typography>
            </Box>
          )}
        </Box>
      </Box>
    </Box>
  );
};

