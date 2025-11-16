/** AI Assistant page */
import React from 'react';
import { Container } from '@mui/material';
import { ChatInterface } from '../components/ai/ChatInterface';

export const AIAssistantPage: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <ChatInterface />
    </Container>
  );
};

