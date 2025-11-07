import React from 'react'
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Grid,
  Typography,
} from '@mui/material'
import { useNavigate, useParams } from 'react-router-dom'
import { curriculumModules, learningTracks } from '../data/curriculum'

export const ModulePage: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>()
  const navigate = useNavigate()
  const module = curriculumModules.find((item) => item.id === Number(moduleId))
  const track = learningTracks.find((item) => item.id === module?.trackId)

  if (!module) {
    return (
      <Box className="min-h-screen flex items-center justify-center p-4">
        <Alert severity="warning">Module not found. Please select a valid module.</Alert>
      </Box>
    )
  }

  return (
    <Box className="min-h-screen bg-gradient-to-b from-white to-slate-100 py-8">
      <Container maxWidth="md">
        <Button onClick={() => navigate('/modules')} className="mb-4">
          ← Back to modules
        </Button>

        <Card className="rounded-3xl shadow-lg mb-4">
          <CardContent className="space-y-4">
            <Box className="flex flex-wrap gap-2 items-center justify-between">
              {track && (
                <Chip
                  label={`${track.title} • ${track.moduleRange}`}
                  sx={{ backgroundColor: '#111827', color: '#fff' }}
                />
              )}
              <Typography color="text.secondary">Module {module.id}</Typography>
            </Box>
            <Typography variant="h4" className="font-bold">
              {module.title}
            </Typography>
            <Typography color="text.secondary">{module.summary}</Typography>
          </CardContent>
        </Card>

        <Grid container spacing={3}>
          <Grid item xs={12} md={7}>
            <Card className="rounded-3xl h-full">
              <CardContent className="space-y-3">
                <Typography variant="h6">Key Topics</Typography>
                {module.focus.map((topic) => (
                  <Typography key={topic}>• {topic}</Typography>
                ))}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={5}>
            <Card className="rounded-3xl h-full">
              <CardContent className="space-y-2">
                <Typography variant="h6">Next Steps</Typography>
                <Typography variant="body2">
                  Review the lessons for this module, then take the 10-question assessment to verify
                  mastery. A 70% score unlocks the next module in the track.
                </Typography>
                <Box className="flex flex-col gap-2 pt-2">
                  <Button variant="contained" onClick={() => navigate(`/modules/${module.id}/assessments`)}>
                    Start Assessment
                  </Button>
                  <Button variant="outlined" onClick={() => navigate('/assessments')}>
                    Browse All Assessments
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}
