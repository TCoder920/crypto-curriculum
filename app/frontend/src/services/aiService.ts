import { apiClient } from './api';

export interface AIMessagePayload {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface StreamingConfig {
  prompt: string;
  messageHistory: AIMessagePayload[];
  model: string;
  facilityType?: string;
  conversationId?: number | string | null;
  abortController: AbortController;
  onChunk: (text: string) => void;
  onError: (message: string) => void;
  onComplete: (finalText: string) => void;
  onNewConversationId?: (conversationId: number) => void;
  imageDocumentIds?: number[];
}

export interface ConversationMessage {
  id: number;
  user_id: number;
  message: string;
  response?: string | null;
  created_at: string;
  sender?: 'user' | 'assistant';
  context?: Record<string, unknown>;
}

export interface ConversationRecord {
  conversation_id: number;
  messages: ConversationMessage[];
  title?: string;
  last_message_at?: string | null;
  message_count?: number;
  created_at?: string;
}

export interface ConversationSummary {
  conversation_id: number;
  title: string | null;
  last_message_at: string | null;
  message_count: number;
  created_at: string;
}

interface ConversationListResponse {
  conversations: ConversationSummary[];
  total: number;
}

export const aiService = {
  async getConversation(conversationId: number): Promise<ConversationRecord> {
    const response = await apiClient.get(`/conversations/${conversationId}`);
    const data = response.data;
    return {
      ...data,
      conversation_id: data.conversation_id ?? data.id ?? conversationId,
    };
  },

  async getLatestConversation(): Promise<ConversationRecord | null> {
    const list = await apiClient.get<ConversationListResponse>('/conversations', {
      params: { limit: 1, offset: 0 },
    });
    const latest = list.data.conversations?.[0];
    if (!latest) {
      return null;
    }
    return this.getConversation(latest.conversation_id);
  },

  async getStreamingAIResponse({
    prompt,
    facilityType,
    messageHistory,
    model,
    conversationId,
    abortController,
    onChunk,
    onError,
    onComplete,
    onNewConversationId,
    imageDocumentIds,
  }: StreamingConfig): Promise<void> {
    const token = localStorage.getItem('access_token');
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${apiClient.defaults.baseURL}/chat/stream`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          message: prompt,
          conversation_id: conversationId,
          context: {
            message_history: messageHistory,
            model,
            facility_type: facilityType,
          },
          image_document_ids: imageDocumentIds && imageDocumentIds.length > 0 ? imageDocumentIds : undefined,
        }),
        signal: abortController.signal,
      });

      if (!response.ok || !response.body) {
        throw new Error('Streaming request failed');
      }

      const newConversationIdHeader = response.headers.get('X-Conversation-Id');
      if (newConversationIdHeader) {
        onNewConversationId?.(Number(newConversationIdHeader));
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let bufferedText = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        bufferedText += decoder.decode(value, { stream: true });
        const segments = bufferedText.split('\n');
        bufferedText = segments.pop() || '';

        for (const segment of segments) {
          const trimmed = segment.trim();
          if (!trimmed) continue;
          if (trimmed.startsWith('data: ')) {
            try {
              const payload = JSON.parse(trimmed.slice(6));
              if (payload.type === 'chunk' && payload.content) {
                onChunk(payload.content);
              } else if (payload.type === 'conversation_id' && payload.conversation_id) {
                onNewConversationId?.(payload.conversation_id);
              } else if (payload.type === 'error') {
                onError(payload.message || 'The AI assistant encountered an error.');
              }
            } catch (error) {
              console.warn('Unable to parse streaming payload', error);
            }
          }
        }
      }

      const remaining = bufferedText.trim();
      if (remaining) {
        onChunk(remaining);
      }

      onComplete(bufferedText ? bufferedText.trim() : '');
    } catch (error) {
      if ((error as Error).name === 'AbortError') {
        onError('Response stopped');
        return;
      }
      onError((error as Error).message || 'Unable to complete AI request');
    }
  },
};
