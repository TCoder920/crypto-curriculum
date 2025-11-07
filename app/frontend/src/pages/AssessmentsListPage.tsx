import React from 'react'
import { Box, Button, Card, CardContent, Container, Grid, Typography } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import { assessmentStructure, curriculumModules, learningTracks } from '../data/curriculum'

const trackName = Object.fromEntries(learningTracks.map((track) => [track.id, track.title]))

export const AssessmentsListPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <Box className="min-h-screen bg-slate-900 py-6">
      <Container maxWidth="lg">
        <Box className="text-center text-white mb-6">
          <Typography variant="h3" className="font-bold">
            All Assessments
          </Typography>
          <Typography variant="body1" className="mt-2 opacity-80">
            Each module features a 10-question assessment blending multiple formats. Score at least
            {` ${assessmentStructure.passingScore}`} to advance.
          </Typography>
        </Box>

        <Box className="bg-white rounded-3xl p-4 mb-6">
          <Typography variant="h6">Assessment Format</Typography>
          <Grid container spacing={2} className="mt-1">
            {assessmentStructure.mix.map((item) => (
              <Grid item xs={12} md={6} key={item}>
                <Typography variant="body2">• {item}</Typography>
              </Grid>
            ))}
          </Grid>
          <Typography variant="body2" color="text.secondary" className="mt-3">
            Minimum passing score: {assessmentStructure.passingScore}. {assessmentStructure.totalQuestions}{' '}
            questions across all 17 modules.
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {curriculumModules.map((module) => (
            <Grid item xs={12} md={6} key={module.id}>
              <Card className="rounded-3xl h-full">
                <CardContent className="space-y-2">
                  <Typography variant="subtitle2" color="text.secondary">
                    {trackName[module.trackId]}
                  </Typography>
                  <Typography variant="h5" className="font-semibold">
                    Module {module.id}: {module.title}
                  </Typography>
                  <Typography variant="body2">{module.summary}</Typography>
                  <Box className="bg-slate-50 rounded-2xl p-3">
                    <Typography variant="subtitle2">Question Mix</Typography>
                    {assessmentStructure.mix.map((item) => (
                      <Typography key={item} variant="body2">
                        • {item}
                      </Typography>
                    ))}
                  </Box>
                  <Box className="flex justify-between items-center pt-1">
                    <Typography variant="body2" color="text.secondary">
                      10 tasks • 70% to pass
                    </Typography>
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
          ))}
        </Grid>
      </Container>
    </Box>
  )
}
