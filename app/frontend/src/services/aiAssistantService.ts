/** AI Assistant service for API calls */
import { apiClient } from './api';

export interface ChatMessage {
  id: number;
  user_id: number;
  message: string;
  response: string | null;
  context: Record<string, any> | null;
  suggested_lessons: number[] | null;
  escalated: boolean;
  created_at: string;
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];
  total: number;
}

export interface ChatMessageCreate {
  message: string;
  context?: Record<string, any> | null;
}

export const aiAssistantService = {
  /** Send a message to the AI assistant */
  sendMessage: async (messageData: ChatMessageCreate): Promise<ChatMessage> => {
    const response = await apiClient.post('/ai-assistant/chat', messageData);
    return response.data;
  },

  /** Get chat history */
  getHistory: async (limit: number = 50): Promise<ChatHistoryResponse> => {
    const response = await apiClient.get('/ai-assistant/history', {
      params: { limit },
    });
    return response.data;
  },
};

