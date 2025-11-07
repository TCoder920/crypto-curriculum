/** Home page */
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { motion } from 'framer-motion'
import {
  Button,
  Box,
  Typography,
  Card,
  CardContent,
  Container,
  Grid,
  Chip,
} from '@mui/material'
import { School, Assessment, TrendingUp, Logout } from '@mui/icons-material'
import {
  aiAssistantGuidance,
  assessmentStructure,
  learningTracks,
  platformStats,
} from '../data/curriculum'

const features = [
  {
    icon: <School sx={{ fontSize: 40, color: '#2563eb' }} />,
    title: 'Learn',
    description: '17 curated modules covering fundamentals, on-chain analysis, development, and architecture.',
  },
  {
    icon: <Assessment sx={{ fontSize: 40, color: '#7e22ce' }} />,
    title: 'Assess',
    description: '170+ questions blending multiple formats to validate both comprehension and application.',
  },
  {
    icon: <TrendingUp sx={{ fontSize: 40, color: '#059669' }} />,
    title: 'Track Progress',
    description: 'Follow your advancement through each learning track with clear milestones and pass marks.',
  },
]

export const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <Box className="min-h-screen bg-slate-950 text-white py-6">
      <Container maxWidth="lg" className="space-y-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <Card className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-white rounded-3xl">
            <CardContent className="p-8 space-y-4">
              <Box className="flex flex-wrap justify-between gap-4 items-center">
                <Box>
                  <Typography variant="overline" className="tracking-[0.3em]">
                    Crypto Curriculum Platform
                  </Typography>
                  <Typography variant="h3" className="font-bold mt-2">
                    Master Blockchain & Cryptocurrency
                  </Typography>
                  <Typography variant="subtitle1" className="opacity-80 mt-2">
                    A structured 4-track journey from curious user to architect-level builder, complete with guided AI support.
                  </Typography>
                  <Typography variant="body2" className="opacity-70 mt-2">
                    Welcome back, {user?.full_name || user?.email || 'learner'} • Role: {user?.role || 'student'}
                  </Typography>
                </Box>
                <Button variant="outlined" onClick={handleLogout} startIcon={<Logout />} sx={{ color: 'white', borderColor: 'white' }}>
                  Logout
                </Button>
              </Box>
              <Box className="flex flex-wrap gap-3 pt-2">
                <Button variant="contained" color="inherit" onClick={() => navigate('/modules')}>
                  Start Learning
                </Button>
                <Button variant="outlined" color="inherit" onClick={() => navigate('/assessments')}>
                  Assess Your Skills
                </Button>
              </Box>
            </CardContent>
          </Card>
        </motion.div>

        <Grid container spacing={3}>
          {platformStats.map((stat) => (
            <Grid item xs={12} md={3} key={stat.label}>
              <Card className="rounded-3xl h-full bg-slate-900 border border-slate-800">
                <CardContent className="text-center">
                  <Typography variant="h4" className="font-bold">
                    {stat.value}
                  </Typography>
                  <Typography variant="body2" className="opacity-70">
                    {stat.label}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Grid container spacing={3}>
          {features.map((feature) => (
            <Grid item xs={12} md={4} key={feature.title}>
              <Card className="rounded-3xl h-full bg-white/5 backdrop-blur border border-white/10">
                <CardContent className="space-y-2 text-center">
                  {feature.icon}
                  <Typography variant="h6">{feature.title}</Typography>
                  <Typography variant="body2" className="opacity-80">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Card className="rounded-3xl bg-white text-slate-900">
          <CardContent className="space-y-4">
            <Typography variant="h5" className="font-bold">
              Learning Tracks
            </Typography>
            <Grid container spacing={3}>
              {learningTracks.map((track) => (
                <Grid item xs={12} md={6} key={track.id}>
                  <Card className="rounded-2xl h-full border border-slate-200">
                    <CardContent className="space-y-2">
                      <Typography variant="overline" color="text.secondary">
                        {track.moduleRange}
                      </Typography>
                      <Typography variant="h6">{track.title}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {track.goal}
                      </Typography>
                      <Chip label={`${track.modules.length} modules`} color="primary" />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card className="rounded-3xl h-full bg-white text-slate-900">
              <CardContent className="space-y-3">
                <Typography variant="h6">Curriculum Structure</Typography>
                <Typography variant="body2">
                  17 modules organized into 4 progressive learning tracks. Complete each track to unlock the next layer of depth—from foundational literacy to architect-level builds.
                </Typography>
                <Box className="space-y-1">
                  {learningTracks.map((track) => (
                    <Typography variant="body2" key={track.id}>
                      • {track.title.replace('·', '•')} — {track.moduleRange}
                    </Typography>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card className="rounded-3xl h-full bg-gradient-to-br from-indigo-600 to-purple-600">
              <CardContent className="space-y-3">
                <Typography variant="h6">Assessment Structure</Typography>
                <Typography variant="body2">
                  Each module concludes with a {assessmentStructure.questionsPerModule}-question assessment. Score at least {assessmentStructure.passingScore} to move forward.
                </Typography>
                <Box className="space-y-1">
                  {assessmentStructure.mix.map((item) => (
                    <Typography key={item}>• {item}</Typography>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Card className="rounded-3xl bg-white text-slate-900">
          <CardContent className="space-y-4">
            <Typography variant="h5">AI Learning Assistant</Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle2">Recommended Tools</Typography>
                {aiAssistantGuidance.recommendedTools.map((tool) => (
                  <Typography key={tool}>• {tool}</Typography>
                ))}
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle2">Do / Don't</Typography>
                <Typography variant="body2" className="font-semibold">
                  Do
                </Typography>
                {aiAssistantGuidance.do.map((tip) => (
                  <Typography key={tip} variant="body2">
                    • {tip}
                  </Typography>
                ))}
                <Typography variant="body2" className="font-semibold mt-2">
                  Don’t
                </Typography>
                {aiAssistantGuidance.dont.map((tip) => (
                  <Typography key={tip} variant="body2">
                    • {tip}
                  </Typography>
                ))}
              </Grid>
              <Grid item xs={12} md={4}>
                <Typography variant="subtitle2">Ask Better Questions</Typography>
                {aiAssistantGuidance.questionTips.map((tip) => (
                  <Typography key={tip} variant="body2">
                    • {tip}
                  </Typography>
                ))}
                <Typography variant="subtitle2" className="mt-2">
                  Example Prompts
                </Typography>
                {Object.values(aiAssistantGuidance.promptExamples).map((prompt) => (
                  <Typography key={prompt} variant="caption" display="block" className="mt-1">
                    {prompt}
                  </Typography>
                ))}
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        <Card className="rounded-3xl bg-white/10 border border-white/20">
          <CardContent className="flex flex-wrap gap-3 justify-between items-center">
            <Typography variant="h6">Ready to continue?</Typography>
            <Box className="flex flex-wrap gap-2">
              <Button variant="contained" color="primary" onClick={() => navigate('/modules')}>
                Go to Modules
              </Button>
              <Button variant="outlined" color="inherit" onClick={() => navigate('/assessments')}>
                Go to Assessments
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  )
}
