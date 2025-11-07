import React from 'react'
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Grid,
  Typography,
} from '@mui/material'
import { useNavigate } from 'react-router-dom'
import { curriculumModules, learningTracks } from '../data/curriculum'

const trackLookup = learningTracks.reduce<Record<string, { title: string; color: string }>>(
  (acc, track) => {
    const colorMap: Record<string, string> = {
      user: '#3b82f6',
      analyst: '#6366f1',
      developer: '#14b8a6',
      architect: '#f97316',
    }
    acc[track.id] = { title: track.title, color: colorMap[track.id] || '#1976d2' }
    return acc
  },
  {},
)

export const ModulesListPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <Box className="min-h-screen bg-slate-50 py-6">
      <Container maxWidth="lg">
        <Box className="mb-8 text-center">
          <Typography variant="h3" className="font-bold mb-2">
            All Modules
          </Typography>
          <Typography color="text.secondary">
            Progress through the curriculum track-by-track. Select a module to review its lessons or
            jump directly into its assessment.
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {curriculumModules.map((module) => {
            const track = trackLookup[module.trackId]
            return (
              <Grid item xs={12} md={6} key={module.id}>
                <Card className="h-full rounded-3xl shadow-md">
                  <CardContent className="space-y-3">
                    <Box className="flex justify-between items-center">
                      <Chip
                        label={track?.title || 'Curriculum Module'}
                        sx={{ backgroundColor: track?.color, color: '#fff' }}
                      />
                      <Typography variant="subtitle2" color="text.secondary">
                        Module {module.id}
                      </Typography>
                    </Box>
                    <Typography variant="h5" className="font-semibold">
                      {module.title}
                    </Typography>
                    <Typography color="text.secondary">{module.summary}</Typography>
                    <Box className="grid gap-2">
                      {module.focus.map((item) => (
                        <Typography variant="body2" key={item}>
                          • {item}
                        </Typography>
                      ))}
                    </Box>
                    <Box className="flex flex-wrap gap-2 pt-2">
                      <Button
                        variant="outlined"
                        onClick={() => navigate(`/modules/${module.id}`)}
                      >
                        View Module
                      </Button>
                      <Button
                        variant="contained"
                        onClick={() => navigate(`/modules/${module.id}/assessments`)}
                      >
                        Take Assessment
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            )
          })}
        </Grid>
      </Container>
    </Box>
  )
}
