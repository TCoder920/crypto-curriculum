/** Module list component */
import React, { useState, useEffect } from "react";
import { Box, Typography, Grid, TextField, Select, MenuItem, FormControl, InputLabel, CircularProgress, Alert } from "@mui/material";
import { motion } from "framer-motion";
import { ModuleCard } from "./ModuleCard";
import { moduleService } from "../../services/moduleService";
import type { Module, Track } from "../../types/module";

interface ModuleListProps {
  onModuleClick: (moduleId: number) => void;
}

export const ModuleList: React.FC<ModuleListProps> = ({ onModuleClick }) => {
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [trackFilter, setTrackFilter] = useState<Track | "">("");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    loadModules();
  }, [trackFilter]);

  // Refresh modules when a module is completed
  useEffect(() => {
    const handleModuleCompleted = () => {
      loadModules();
    };
    window.addEventListener("moduleCompleted", handleModuleCompleted);
    return () => window.removeEventListener("moduleCompleted", handleModuleCompleted);
  }, []);

  const loadModules = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await moduleService.getModules(
        trackFilter || undefined,
        1,
        100 // Get all modules for now
      );
      setModules(response.modules);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to load modules");
    } finally {
      setLoading(false);
    }
  };

  const filteredModules = modules.filter((module) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return (
      module.title.toLowerCase().includes(query) ||
      module.description?.toLowerCase().includes(query) ||
      module.track.toLowerCase().includes(query)
    );
  });

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "400px" }}>
        <CircularProgress sx={{ color: "white" }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ py: 4, width: "100%", maxWidth: "100%", overflowX: "hidden" }}>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          component="h1"
          sx={{
            fontWeight: 700,
            color: "white",
            mb: 3,
          }}
        >
          Curriculum Modules
        </Typography>

        <Box
          sx={{
            display: "flex",
            gap: 2,
            mb: 3,
            flexWrap: "wrap",
            width: "100%",
            maxWidth: "100%",
          }}
        >
          <TextField
            placeholder="Search modules..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{
              flex: 1,
              minWidth: 200,
              "& .MuiOutlinedInput-root": {
                background: "rgba(255, 255, 255, 0.05)",
                backdropFilter: "blur(20px)",
                color: "white",
                "& fieldset": {
                  borderColor: "rgba(255, 255, 255, 0.1)",
                },
                "&:hover fieldset": {
                  borderColor: "rgba(255, 255, 255, 0.2)",
                },
                "&.Mui-focused fieldset": {
                  borderColor: "rgba(255, 255, 255, 0.3)",
                },
              },
              "& .MuiInputBase-input::placeholder": {
                color: "rgba(255, 255, 255, 0.5)",
              },
            }}
          />

          <FormControl
            sx={{
              minWidth: 150,
              "& .MuiOutlinedInput-root": {
                background: "rgba(255, 255, 255, 0.05)",
                backdropFilter: "blur(20px)",
                color: "white",
                "& fieldset": {
                  borderColor: "rgba(255, 255, 255, 0.1)",
                },
                "&:hover fieldset": {
                  borderColor: "rgba(255, 255, 255, 0.2)",
                },
                "&.Mui-focused fieldset": {
                  borderColor: "rgba(255, 255, 255, 0.3)",
                },
              },
            }}
          >
            <InputLabel sx={{ color: "rgba(255, 255, 255, 0.7)" }}>Track</InputLabel>
            <Select
              value={trackFilter}
              onChange={(e) => setTrackFilter(e.target.value as Track | "")}
              label="Track"
              sx={{ color: "white" }}
            >
              <MenuItem value="">All Tracks</MenuItem>
              <MenuItem value="user">User</MenuItem>
              <MenuItem value="analyst">Analyst</MenuItem>
              <MenuItem value="developer">Developer</MenuItem>
              <MenuItem value="architect">Architect</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>

      {filteredModules.length === 0 ? (
        <Typography variant="body1" sx={{ color: "rgba(255, 255, 255, 0.7)", textAlign: "center", py: 4 }}>
          No modules found.
        </Typography>
      ) : (
        <Grid container spacing={3} sx={{ width: "100%", margin: 0 }}>
          {filteredModules.map((module, index) => (
            <Grid item xs={12} sm={6} md={4} key={module.id}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <ModuleCard module={module} onClick={() => onModuleClick(module.id)} />
              </motion.div>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

