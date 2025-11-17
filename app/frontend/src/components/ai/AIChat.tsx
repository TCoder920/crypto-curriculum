import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import clsx from 'clsx';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Edit, ErrorOutline, Send, StopCircle, Image as ImageIcon } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { TokenFadeTyper } from './TokenFadeTyper';
import { aiService, type AIMessagePayload, type ConversationRecord } from '../../services/aiService';
import { documentService } from '../../services/documentService';

const TOKEN_LIMIT = 4000;
const DEFAULT_MODEL = 'learning-assistant-v1';

export interface AIChatProps {
  initialQuery?: string;
  initialConversation?: ChatBubble[];
  initialConversationIdProp?: number | null;
  navigateTo?: (path: string) => void;
  className?: string;
  onConversationChange?: (conversationId: number | null) => void;
  availableImages?: Array<{ id: number; title: string; type?: string }>;
  attachedImageIds?: number[];
  onAttachedImagesChange?: (ids: number[]) => void;
}

interface ChatBubble {
  id: string;
  sender: 'user' | 'ai' | 'system' | 'error';
  text: string;
  createdAt: string;
  isStreaming?: boolean;
}

const countTokens = (text: string): number => {
  if (!text) return 0;
  return Math.ceil(text.trim().split(/\s+/).length * 1.3);
};

export const AIChat: React.FC<AIChatProps> = ({
  initialQuery,
  initialConversation,
  initialConversationIdProp,
  navigateTo,
  className,
  onConversationChange,
  availableImages = [],
  attachedImageIds: externalAttachedImageIds = [],
  onAttachedImagesChange,
}) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<ChatBubble[]>(initialConversation ?? []);
  const [inputValue, setInputValue] = useState(initialQuery ?? '');
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isStopping, setIsStopping] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(initialConversationIdProp ?? null);
  const [collapseThreshold, setCollapseThreshold] = useState({ chars: 1200, tokens: 300 });
  const [internalAttachedImageIds, setInternalAttachedImageIds] = useState<number[]>([]);
  const [uploadingImages, setUploadingImages] = useState<Map<number, boolean>>(new Map());
  const [uploadedImagePreviews, setUploadedImagePreviews] = useState<Map<number, { name: string; url: string }>>(new Map());
  const imageInputRef = useRef<HTMLInputElement | null>(null);
  
  // Use external attached images if callback provided (controlled), otherwise use internal state (uncontrolled)
  const attachedImageIds = onAttachedImagesChange ? externalAttachedImageIds : internalAttachedImageIds;
  const setAttachedImageIds = onAttachedImagesChange || setInternalAttachedImageIds;
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const listRef = useRef<HTMLDivElement | null>(null);
  const abortStreamingRef = useRef<AbortController | null>(null);
  const aiPlaceholderIdRef = useRef<string | null>(null);
  const conversationIdRef = useRef<number | null>(conversationId);

  const tokenUsage = useMemo(() => {
    const totalTokens = messages.reduce((acc, message) => acc + countTokens(message.text), 0);
    const percentUsed = (totalTokens / TOKEN_LIMIT) * 100;
    let statusColor = 'bg-emerald-400';
    if (percentUsed > 95) statusColor = 'bg-red-500';
    else if (percentUsed > 80) statusColor = 'bg-amber-400';
    return { totalTokens, percentUsed, statusColor };
  }, [messages]);

  const adjustTextareaHeight = useCallback(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 240)}px`;
    }
  }, []);

  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue, adjustTextareaHeight]);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    const updateThreshold = () => {
      if (window.innerWidth < 640) {
        setCollapseThreshold({ chars: 800, tokens: 180 });
      } else if (window.innerWidth < 1024) {
        setCollapseThreshold({ chars: 1200, tokens: 260 });
      } else {
        setCollapseThreshold({ chars: 1600, tokens: 360 });
      }
    };
    updateThreshold();
    window.addEventListener('resize', updateThreshold);
    return () => window.removeEventListener('resize', updateThreshold);
  }, []);

  const hasMessages = messages.length > 0 || isProcessing;

  useEffect(() => {
    conversationIdRef.current = conversationId;
  }, [conversationId]);

  const mapConversationMessages = useCallback((record: ConversationRecord): ChatBubble[] => {
    return record.messages.flatMap((entry) => {
      const responseText =
        entry.response ??
        (entry as unknown as { assistant_response?: string | null }).assistant_response ??
        '';
      const bubbles: ChatBubble[] = [
        {
          id: `${entry.id}-user`,
          sender: 'user',
          text: entry.message,
          createdAt: entry.created_at,
        },
      ];
      if (responseText) {
        bubbles.push({
          id: `${entry.id}-ai`,
          sender: 'ai',
          text: responseText,
          createdAt: entry.created_at,
        });
      }
      return bubbles;
    });
  }, []);

  const refreshConversation = useCallback(
    async (id: number) => {
      try {
        const record = await aiService.getConversation(id);
        const resolvedId = record.conversation_id ?? (record as unknown as { id?: number }).id ?? id;
        setConversationId(resolvedId);
        conversationIdRef.current = resolvedId;
        setMessages(mapConversationMessages(record));
        onConversationChange?.(resolvedId);
      } catch (err) {
        console.warn('Unable to load conversation', err);
        setError('Unable to load the requested conversation.');
      }
    },
    [mapConversationMessages],
  );

  useEffect(() => {
    if (initialConversationIdProp !== null && initialConversationIdProp !== undefined) {
      if (initialConversationIdProp !== conversationIdRef.current) {
      refreshConversation(initialConversationIdProp);
      }
      return;
    }
    if (conversationIdRef.current) return;
    const loadLatest = async () => {
      try {
        const latest = await aiService.getLatestConversation();
        if (latest) {
          const resolvedId = latest.conversation_id ?? (latest as unknown as { id?: number }).id ?? null;
          conversationIdRef.current = resolvedId;
          setConversationId(resolvedId);
          setMessages(mapConversationMessages(latest));
        }
      } catch (err) {
        console.warn('Unable to load latest conversation', err);
      }
    };
    void loadLatest();
  }, [initialConversationIdProp, refreshConversation, mapConversationMessages]);

  const handleStopResponse = () => {
    if (!abortStreamingRef.current) return;
    setIsStopping(true);
    abortStreamingRef.current.abort();
    setTimeout(() => {
      setIsStopping(false);
      setIsProcessing(false);
    }, 200);
  };

  const handleNewChat = () => {
    abortStreamingRef.current?.abort();
    setMessages([]);
    setConversationId(null);
    conversationIdRef.current = null;
    setInputValue('');
    setError(null);
    onConversationChange?.(null);
  };

  const buildHistory = useCallback(
    (currentMessages: ChatBubble[]): AIMessagePayload[] =>
      currentMessages.map((message) => ({
        role: message.sender === 'user' ? 'user' : 'assistant',
        content: message.text,
      })),
    [],
  );

  const finalizeStreamingMessage = useCallback((content: string) => {
    const placeholderId = aiPlaceholderIdRef.current;
    if (!placeholderId) return;
    setMessages((prev) =>
      prev.map((message) =>
        message.id === placeholderId
          ? {
              ...message,
              text: content,
              isStreaming: false,
            }
          : message,
      ),
    );
    aiPlaceholderIdRef.current = null;
  }, []);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;
    const trimmed = inputValue.trim();
    const newUserMessage: ChatBubble = {
      id: `${Date.now()}-user`,
      sender: 'user',
      text: trimmed,
      createdAt: new Date().toISOString(),
    };

    const placeholderId = `${Date.now()}-ai`;
    aiPlaceholderIdRef.current = placeholderId;
    const placeholderMessage: ChatBubble = {
      id: placeholderId,
      sender: 'ai',
      text: '',
      createdAt: new Date().toISOString(),
      isStreaming: true,
    };

    setMessages((prev) => [...prev, newUserMessage, placeholderMessage]);
    setInputValue('');
    setIsProcessing(true);
    setError(null);

    const abortController = new AbortController();
    abortStreamingRef.current = abortController;

    await aiService.getStreamingAIResponse({
      prompt: trimmed,
      messageHistory: buildHistory([...messages, newUserMessage]),
      model: DEFAULT_MODEL,
      conversationId,
      abortController,
      imageDocumentIds: attachedImageIds.length > 0 ? attachedImageIds : undefined,
      onChunk: (content) => {
        setMessages((prev) =>
          prev.map((message) =>
            message.id === placeholderId
              ? {
                  ...message,
                  text: message.text + content,
                  isStreaming: true,
                }
              : message,
          ),
        );
      },
      onError: (message) => {
        setError(message);
        setIsProcessing(false);
        finalizeStreamingMessage('');
      },
      onComplete: (finalText) => {
        finalizeStreamingMessage(finalText || placeholderMessage.text);
        setIsProcessing(false);
        abortStreamingRef.current = null;
        // Clear attached images and previews after sending
        setAttachedImageIds([]);
        setUploadedImagePreviews((prev) => {
          prev.forEach((preview) => URL.revokeObjectURL(preview.url));
          return new Map();
        });
        const activeConversationId = conversationIdRef.current;
        if (activeConversationId) {
          void refreshConversation(activeConversationId);
        }
      },
      onNewConversationId: (nextId) => {
        setConversationId(nextId);
        conversationIdRef.current = nextId;
        onConversationChange?.(nextId);
      },
    });
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleImageUploadClick = () => {
    imageInputRef.current?.click();
  };

  const handleImageSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const imageFiles = Array.from(files).filter((file) => {
      const ext = file.name.split('.').pop()?.toLowerCase();
      return ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext || '');
    });

    if (imageFiles.length === 0) {
      setError('Please select image files (jpg, png, gif, webp)');
      return;
    }

    // Upload each image
    for (const file of imageFiles) {
      const tempId = Date.now() + Math.random(); // Temporary ID for preview
      setUploadingImages((prev) => new Map(prev).set(tempId, true));
      
      // Create preview URL
      const previewUrl = URL.createObjectURL(file);
      setUploadedImagePreviews((prev) => new Map(prev).set(tempId, { name: file.name, url: previewUrl }));

      try {
        const uploadedDoc = await documentService.uploadDocument(file);
        // Replace temp ID with real document ID
        setUploadingImages((prev) => {
          const newMap = new Map(prev);
          newMap.delete(tempId);
          newMap.set(uploadedDoc.id, false);
          return newMap;
        });
        setUploadedImagePreviews((prev) => {
          const newMap = new Map(prev);
          const preview = newMap.get(tempId);
          if (preview) {
            newMap.delete(tempId);
            newMap.set(uploadedDoc.id, preview);
          }
          return newMap;
        });
        
        // Add to attached images
        setAttachedImageIds((ids) => [...ids, uploadedDoc.id]);
        
        // Revoke preview URL after a delay
        setTimeout(() => URL.revokeObjectURL(previewUrl), 1000);
      } catch (error: any) {
        setError(error.response?.data?.detail || error.message || 'Failed to upload image');
        setUploadingImages((prev) => {
          const newMap = new Map(prev);
          newMap.delete(tempId);
          return newMap;
        });
        setUploadedImagePreviews((prev) => {
          const newMap = new Map(prev);
          newMap.delete(tempId);
          return newMap;
        });
      }
    }

    // Reset file input
    if (imageInputRef.current) {
      imageInputRef.current.value = '';
    }
  };

  const isMessageCollapsible = useCallback(
    (message: ChatBubble) => message.sender === 'ai' && (message.text.length > collapseThreshold.chars || countTokens(message.text) > collapseThreshold.tokens),
    [collapseThreshold],
  );

  const [collapsedMessages, setCollapsedMessages] = useState<Record<string, boolean>>({});

  const toggleMessageCollapse = (messageId: string) => {
    setCollapsedMessages((prev) => ({
      ...prev,
      [messageId]: !prev[messageId],
    }));
  };

  const cleanMessageText = (text: string) => text?.trim() ?? '';

  const contextWarning = tokenUsage.percentUsed > 80;

  const messageComponents = useMemo(
    () => ({
      a: ({ href, children, ...rest }: React.AnchorHTMLAttributes<HTMLAnchorElement>) => {
        const isInternal = href?.startsWith('/');
        const handleClick = (event: React.MouseEvent<HTMLAnchorElement>) => {
          if (isInternal && navigateTo) {
            event.preventDefault();
            navigateTo(href as string);
          }
        };
        return (
          <a
            {...rest}
            href={href}
            target={isInternal ? undefined : '_blank'}
            rel={isInternal ? undefined : 'noreferrer'}
            onClick={handleClick}
        className="text-indigo-600 underline underline-offset-2 dark:text-indigo-300"
          >
            {children}
          </a>
        );
      },
    }),
    [navigateTo],
  );

  return (
    <div className={clsx('flex h-full flex-col rounded-3xl border border-white/20 bg-white/70 shadow-2xl backdrop-blur-xl dark:border-slate-700 dark:bg-slate-900/60', className)}>
      <div className="flex items-center justify-between border-b border-white/40 px-4 py-3 dark:border-slate-700/70">
        <div className="flex w-full items-center justify-end gap-3">
          <button
            className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-200/70 text-slate-600 transition-colors hover:border-slate-300 hover:bg-white/80 dark:border-slate-600 dark:text-slate-200"
            onClick={handleNewChat}
            title="Start a new chat"
            aria-label="Start a new chat"
          >
            <Edit fontSize="small" />
          </button>
          <div className="w-28">
            <div className="flex items-center justify-between text-[10px] font-medium text-slate-500">
              <span>Context</span>
              <span>{Math.min(tokenUsage.percentUsed, 100).toFixed(0)}%</span>
            </div>
            <div className="mt-1 h-2 rounded-full bg-slate-200/70 dark:bg-slate-700">
              <div
                className={clsx('h-full rounded-full transition-all duration-300', tokenUsage.statusColor)}
                style={{ width: `${Math.min(tokenUsage.percentUsed, 100)}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 bg-red-50 px-4 py-2 text-sm text-red-700 dark:bg-red-900/40 dark:text-red-200">
          <ErrorOutline fontSize="small" />
          <span>{error}</span>
        </div>
      )}

      {contextWarning && (
        <div className="bg-amber-50 px-4 py-2 text-xs text-amber-700 dark:bg-amber-900/40 dark:text-amber-200">
          You are approaching the context window limit. Consider starting a new conversation to avoid truncation.
        </div>
      )}

      <div className="flex-1 overflow-hidden">
        <div ref={listRef} className="flex h-full flex-col gap-4 overflow-y-auto px-4 py-6">
          {!hasMessages ? (
            <div className="flex h-full w-full items-center justify-center">
              <div className="w-full max-w-lg rounded-3xl border border-dashed border-slate-200/80 bg-white/80 px-8 py-8 text-center shadow-inner dark:border-slate-700 dark:bg-slate-800/70">
                <p className="text-base font-medium text-slate-800 dark:text-white">Start a fresh study thread</p>
                <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
                  Attach a reference on the left or ask a question here to get inline citations and summaries.
                </p>
                <div className="mt-4 text-xs uppercase tracking-wider text-slate-400 dark:text-slate-500">
                  No messages yet
                </div>
              </div>
            </div>
          ) : (
            messages.map((message) => {
              const collapsible = isMessageCollapsible(message);
              const collapsed = collapsible && collapsedMessages[message.id];
              return (
                <div
                  key={message.id}
                  className={clsx('flex', message.sender === 'user' ? 'justify-end' : 'justify-start')}
                >
                  <div
                    className={clsx(
                      'max-w-[85%] rounded-3xl px-4 py-3 text-sm shadow-lg transition-colors',
                      message.sender === 'user'
                        ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white'
                        : 'bg-slate-100/80 text-slate-900 dark:bg-slate-800/80 dark:text-slate-50',
                    )}
                  >
                    {message.sender === 'ai' ? (
                      <TokenFadeTyper
                        text={collapsed ? `${cleanMessageText(message.text).slice(0, 400)}…` : cleanMessageText(message.text)}
                        isStreaming={message.isStreaming}
                        components={messageComponents}
                      />
                    ) : (
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.text}</ReactMarkdown>
                    )}
                    {collapsible && (
                      <button
                        className="mt-3 text-xs font-semibold text-indigo-500"
                        onClick={() => toggleMessageCollapse(message.id)}
                      >
                        {collapsed ? 'Show full message' : 'Collapse response'}
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      <div className="border-t border-white/40 px-4 py-4 dark:border-slate-700/70">
        <div className="mx-auto flex max-w-3xl flex-col gap-3">
          {(attachedImageIds.length > 0 || uploadedImagePreviews.size > 0) && (
            <div className="flex flex-col gap-2 rounded-2xl border border-blue-200/50 bg-blue-50/50 p-3 dark:border-blue-800 dark:bg-blue-950/30">
              <p className="text-xs font-semibold text-slate-600 dark:text-slate-300">Attached images:</p>
              <div className="flex flex-wrap gap-2">
                {Array.from(uploadedImagePreviews.entries()).map(([imageId, preview]) => {
                  const isUploading = uploadingImages.get(imageId);
                  return (
                    <div
                      key={imageId}
                      className="group relative inline-flex items-center gap-2 rounded-lg border border-blue-200 bg-white p-2 text-xs dark:border-blue-700 dark:bg-slate-800"
                    >
                      {isUploading ? (
                        <div className="flex items-center gap-2">
                          <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-500 border-t-transparent" />
                          <span className="text-slate-500">Uploading...</span>
                        </div>
                      ) : (
                        <>
                          <img
                            src={preview.url}
                            alt={preview.name}
                            className="h-8 w-8 rounded object-cover"
                          />
                          <span className="max-w-[120px] truncate text-slate-700 dark:text-slate-200">{preview.name}</span>
                          <button
                            onClick={() => {
                              setAttachedImageIds((ids) => ids.filter((id) => id !== imageId));
                              setUploadedImagePreviews((prev) => {
                                const newMap = new Map(prev);
                                const prevData = newMap.get(imageId);
                                if (prevData) URL.revokeObjectURL(prevData.url);
                                newMap.delete(imageId);
                                return newMap;
                              });
                            }}
                            className="text-slate-400 hover:text-red-500 dark:text-slate-500 dark:hover:text-red-400"
                            aria-label="Remove image"
                          >
                            ×
                          </button>
                        </>
                      )}
                    </div>
                  );
                })}
                {attachedImageIds
                  .filter((id) => !uploadedImagePreviews.has(id))
                  .map((imageId) => {
                    const image = availableImages.find((img) => img.id === imageId);
                    return (
                      <div
                        key={imageId}
                        className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white px-3 py-1 text-xs dark:border-blue-700 dark:bg-slate-800"
                      >
                        <span className="text-slate-700 dark:text-slate-200">{image?.title || `Image ${imageId}`}</span>
                        <button
                          onClick={() => setAttachedImageIds((ids) => ids.filter((id) => id !== imageId))}
                          className="text-slate-400 hover:text-red-500 dark:text-slate-500 dark:hover:text-red-400"
                          aria-label="Remove image"
                        >
                          ×
                        </button>
                      </div>
                    );
                  })}
              </div>
            </div>
          )}
          <div className="relative flex items-center gap-3 rounded-3xl border border-slate-200/80 bg-white/85 px-4 py-3 shadow-inner transition focus-within:border-blue-400 dark:border-slate-700 dark:bg-slate-800/70">
            <input
              ref={imageInputRef}
              type="file"
              accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
              multiple
              onChange={handleImageSelect}
              className="hidden"
              disabled={isProcessing}
            />
            <button
              onClick={handleImageUploadClick}
              disabled={isProcessing}
              className={clsx(
                'inline-flex h-10 w-10 items-center justify-center rounded-full transition',
                isProcessing
                  ? 'cursor-not-allowed opacity-50 text-slate-400'
                  : 'text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700'
              )}
              aria-label="Upload image"
              title="Upload image"
            >
              <ImageIcon fontSize="small" />
            </button>
            <textarea
              ref={textareaRef}
              className="max-h-48 w-full resize-none bg-transparent text-base leading-relaxed text-left text-slate-800 outline-none placeholder:text-slate-400 dark:text-white"
              placeholder="Type your question or prompt here..."
              value={inputValue}
              onChange={(event) => setInputValue(event.target.value)}
              onKeyDown={handleKeyPress}
              disabled={isProcessing}
              rows={1}
            />
            <div className="flex items-center gap-3">
              {isProcessing && (
                <button
                  onClick={handleStopResponse}
                  className="inline-flex items-center gap-1 rounded-full border border-red-100 px-3 py-1 text-xs font-semibold text-red-600 transition hover:bg-red-50"
                  disabled={isStopping}
                >
                  <StopCircle fontSize="small" /> Stop
                </button>
              )}
              <button
                onClick={handleSendMessage}
                disabled={isProcessing || !inputValue.trim()}
                className={clsx(
                  'inline-flex h-11 w-11 items-center justify-center rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg shadow-blue-500/30 transition',
                  (isProcessing || !inputValue.trim()) && 'cursor-not-allowed opacity-60',
                )}
                aria-label="Send message"
              >
                <Send fontSize="small" />
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};
