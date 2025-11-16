/** Forum page - displays forum board for a module */
import React from 'react';
import { useParams } from 'react-router-dom';
import { Container, Typography, Box } from '@mui/material';
import { ForumBoard } from '../components/forum/ForumBoard';

export const ForumPage: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();

  if (!moduleId) {
    return (
      <Container>
        <Typography variant="h4">Module not found</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <ForumBoard />
    </Container>
  );
};

