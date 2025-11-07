/** Lesson viewer component with Markdown rendering */
import React from "react";
import { Box, Typography, Chip } from "@mui/material";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";
import type { Lesson } from "../../types/module";

interface LessonViewerProps {
  lesson: Lesson;
}

export const LessonViewer: React.FC<LessonViewerProps> = ({ lesson }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Box
        sx={{
          background: "rgba(255, 255, 255, 0.05)",
          backdropFilter: "blur(20px)",
          borderRadius: 3,
          border: "1px solid rgba(255, 255, 255, 0.1)",
          p: { xs: 2, sm: 3, md: 4 },
          width: "100%",
          maxWidth: "100%",
          overflowX: "hidden",
          "& pre": {
            overflowX: "auto",
            maxWidth: "100%",
          },
          "& code": {
            wordBreak: "break-word",
            overflowWrap: "break-word",
          },
        }}
      >
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 3 }}>
          <Typography
            variant="h5"
            component="h2"
            sx={{
              fontWeight: 600,
              color: "white",
              flex: 1,
            }}
          >
            {lesson.title}
          </Typography>
          <Box sx={{ display: "flex", gap: 1, ml: 2 }}>
            <Chip
              label={lesson.lesson_type}
              size="small"
              sx={{
                background: "rgba(255, 255, 255, 0.1)",
                color: "white",
                textTransform: "capitalize",
              }}
            />
            {lesson.estimated_minutes && (
              <Chip
                label={`${lesson.estimated_minutes} min`}
                size="small"
                sx={{
                  background: "rgba(255, 255, 255, 0.1)",
                  color: "white",
                }}
              />
            )}
          </Box>
        </Box>

        <Box
          sx={{
            color: "rgba(255, 255, 255, 0.95)",
            lineHeight: 1.8,
            "& h1, & h2, & h3, & h4, & h5, & h6": {
              color: "rgba(255, 255, 255, 1)",
              fontWeight: 600,
              mt: 3,
              mb: 2,
            },
            "& h1": { fontSize: "2rem" },
            "& h2": { fontSize: "1.75rem" },
            "& h3": { fontSize: "1.5rem" },
            "& h4": { fontSize: "1.25rem" },
            "& p": {
              mb: 2,
            },
            "& ul, & ol": {
              mb: 2,
              pl: 3,
            },
            "& li": {
              mb: 1,
            },
            "& code": {
              background: "rgba(0, 0, 0, 0.3)",
              padding: "2px 6px",
              borderRadius: 2,
              fontSize: "0.9em",
              fontFamily: "monospace",
            },
            "& pre": {
              background: "rgba(0, 0, 0, 0.3)",
              padding: 2,
              borderRadius: 2,
              overflowX: "auto",
              mb: 2,
              "& code": {
                background: "transparent",
                padding: 0,
              },
            },
            "& blockquote": {
              borderLeft: "4px solid rgba(255, 255, 255, 0.3)",
              pl: 2,
              ml: 0,
              fontStyle: "italic",
              color: "rgba(255, 255, 255, 0.7)",
            },
            "& a": {
              color: "#64b5f6",
              textDecoration: "none",
              "&:hover": {
                textDecoration: "underline",
              },
            },
            "& img": {
              maxWidth: "100%",
              borderRadius: 2,
              mt: 2,
              mb: 2,
            },
            "& table": {
              width: "100%",
              maxWidth: "100%",
              borderCollapse: "collapse",
              mb: 2,
              overflowX: "auto",
              display: "block",
              "& thead, & tbody, & tr": {
                display: "table",
                width: "100%",
                tableLayout: "fixed",
              },
              "& th, & td": {
                border: "1px solid rgba(255, 255, 255, 0.1)",
                padding: 1,
                textAlign: "left",
                wordBreak: "break-word",
                overflowWrap: "break-word",
              },
              "& th": {
                background: "rgba(255, 255, 255, 0.05)",
                fontWeight: 600,
              },
            },
          }}
        >
          <ReactMarkdown>{lesson.content}</ReactMarkdown>
        </Box>

        {lesson.media_url && (
          <Box sx={{ mt: 3 }}>
            {lesson.lesson_type === "video" ? (
              <video
                src={lesson.media_url}
                controls
                style={{
                  width: "100%",
                  borderRadius: 8,
                  maxHeight: "500px",
                }}
              />
            ) : (
              <img
                src={lesson.media_url}
                alt={lesson.title}
                style={{
                  width: "100%",
                  borderRadius: 8,
                  maxHeight: "500px",
                  objectFit: "contain",
                }}
              />
            )}
          </Box>
        )}
      </Box>
    </motion.div>
  );
};

