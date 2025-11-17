import React, { Fragment, useEffect, useMemo, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import { FileOpen, UploadFile } from '@mui/icons-material';
import { AIChat } from '../components/ai/AIChat';
import { ConversationSidebar } from '../components/ai/ConversationSidebar';
import { documentService, type ReferenceDocument, isImageDocument } from '../services/documentService';

interface LocationState {
  initialQuery?: string;
  conversationId?: number;
}

const groupDocuments = (documents: ReferenceDocument[]) => {
  const standard = documents.filter((doc) => doc.category !== 'user-upload');
  const uploads = documents.filter((doc) => doc.category === 'user-upload');
  return { standard, uploads };
};

const ALLOWED_FILE_TYPES = ['pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'webp'];
const IMAGE_FILE_TYPES = ['jpg', 'jpeg', 'png', 'gif', 'webp'];
const TEXT_FILE_TYPES = ['pdf', 'docx', 'txt'];
const MAX_FILE_SIZE_MB = 10;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

export const AIAssistantPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const locationState = (location.state as LocationState) || {};
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [documents, setDocuments] = useState<ReferenceDocument[]>([]);
  const [isLoadingDocs, setIsLoadingDocs] = useState(false);
  const [docError, setDocError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(
    locationState.conversationId ?? null
  );

  const loadDocuments = async () => {
    setIsLoadingDocs(true);
    setDocError(null);
    try {
      const list = await documentService.listDocuments(true); // Force refresh
      setDocuments(list);
    } catch (error) {
      setDocError('Unable to load documents.');
    } finally {
      setIsLoadingDocs(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const validateFile = (file: File): string | null => {
    const extension = file.name.split('.').pop()?.toLowerCase();
    if (!extension || !ALLOWED_FILE_TYPES.includes(extension)) {
      return `File type not allowed. Allowed types: ${ALLOWED_FILE_TYPES.join(', ')}`;
    }
    if (file.size > MAX_FILE_SIZE_BYTES) {
      return `File size exceeds ${MAX_FILE_SIZE_MB}MB limit.`;
    }
    return null;
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file
    const validationError = validateFile(file);
    if (validationError) {
      setUploadError(validationError);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      return;
    }

    // Reset errors and start upload
    setUploadError(null);
    setIsUploading(true);
    setUploadProgress(0);

    try {
      await documentService.uploadDocument(
        file,
        undefined, // moduleId - can be added later
        undefined, // courseScope - can be added later
        (progress) => {
          setUploadProgress(progress);
        }
      );

      // Success - refresh document list
      await loadDocuments();
      setUploadProgress(0);
      
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Upload failed. Please try again.';
      setUploadError(errorMessage);
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const groupedDocs = useMemo(() => groupDocuments(documents), [documents]);

  const [attachedImages, setAttachedImages] = useState<number[]>([]);

  const renderDocumentCard = (doc: ReferenceDocument) => {
    const isImage = IMAGE_FILE_TYPES.includes(doc.type?.toLowerCase() || '');
    const isAttached = attachedImages.includes(doc.id);

    return (
      <div
        key={doc.id}
        className="rounded-2xl border border-white/30 bg-white/20 p-4 text-sm shadow-lg backdrop-blur-xl dark:border-slate-700 dark:bg-slate-800/60"
      >
        <p className="text-sm font-semibold text-slate-900 dark:text-white">{doc.title}</p>
        <p className="mt-1 text-[11px] uppercase tracking-wide text-slate-500">
          {doc.category === 'user-upload' ? 'User Upload' : doc.category}
        </p>
        <p className="mt-1 text-xs text-slate-500">Updated {new Date(doc.updated_at).toLocaleDateString()}</p>
        <div className="mt-3 flex gap-2">
          <button
            className="inline-flex items-center gap-2 rounded-full border border-slate-300/70 px-3 py-1 text-xs font-semibold text-slate-600 transition hover:bg-white/70 dark:border-slate-600 dark:text-slate-200"
            onClick={() => documentService.openDocumentInNewTab(doc.id)}
          >
            <FileOpen fontSize="inherit" /> View
          </button>
          {isImage && (
            <button
              className={`
                inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold transition
                ${
                  isAttached
                    ? 'border-blue-400 bg-blue-100 text-blue-700 dark:border-blue-600 dark:bg-blue-900/50 dark:text-blue-300'
                    : 'border-slate-300/70 text-slate-600 hover:bg-white/70 dark:border-slate-600 dark:text-slate-200'
                }
              `}
              onClick={() => {
                if (isAttached) {
                  setAttachedImages((ids) => ids.filter((id) => id !== doc.id));
                } else {
                  setAttachedImages((ids) => [...ids, doc.id]);
                }
              }}
            >
              {isAttached ? '✓ Attached' : '+ Attach'}
            </button>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="relative h-[calc(100vh-4rem)] w-full overflow-hidden px-4 pb-6 pt-2">
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-100/70 via-white to-blue-50 dark:from-slate-900 dark:via-slate-950 dark:to-blue-950" />
      <div className="mx-auto flex h-full max-w-6xl flex-col">
        <div className="mb-4 flex flex-col gap-2 rounded-3xl border border-white/50 bg-white/70 px-6 py-4 backdrop-blur-xl dark:border-slate-700 dark:bg-slate-900/60">
          <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">Learning workspace</p>
          <h1 className="text-2xl font-semibold text-slate-900 dark:text-white">AI Reference Studio</h1>
          <p className="text-sm text-slate-600 dark:text-slate-300">
            Collect study guides, attach module notes, and explore AI answers with inline citations.
          </p>
        </div>
        <div className="grid flex-1 grid-cols-1 gap-6 overflow-hidden md:grid-cols-3">
          <div className="flex flex-col rounded-3xl border border-white/40 bg-white/65 p-4 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-900/60">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">File storage</p>
              <button
                onClick={handleUploadClick}
                disabled={isUploading}
                className={`
                  inline-flex items-center gap-1 rounded-full border border-slate-200/80 px-3 py-1 text-xs font-semibold 
                  transition hover:bg-white/80 dark:border-slate-700 dark:text-slate-300
                  ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
                `}
              >
                <UploadFile fontSize="inherit" /> {isUploading ? 'Uploading...' : 'Upload'}
              </button>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.docx,.txt,.jpg,.jpeg,.png,.gif,.webp"
              onChange={handleFileSelect}
              className="hidden"
              disabled={isUploading}
            />
            {docError && <p className="mt-3 text-xs text-red-500">{docError}</p>}
            {uploadError && <p className="mt-3 text-xs text-red-500">{uploadError}</p>}
            {isUploading && (
              <div className="mt-3">
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <p className="mt-1 text-xs text-slate-500">{uploadProgress}%</p>
              </div>
            )}
            <div className="mt-4 max-h-[200px] overflow-y-auto pr-1">
              {isLoadingDocs ? (
                <p className="text-xs text-slate-500">Loading documents…</p>
              ) : (
                <TransitionGroup component={null}>
                  {[{ title: 'Standard Library', data: groupedDocs.standard }, { title: 'User Uploads', data: groupedDocs.uploads }].map(
                    (section) => (
                      <CSSTransition key={section.title} timeout={250} classNames="fade">
                        <Fragment>
                          <p className="mb-2 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
                            {section.title}
                          </p>
                          <div className="mb-4 space-y-3">
                            {section.data.length === 0 ? (
                              <p className="text-xs text-slate-400">No documents yet.</p>
                            ) : (
                              section.data.map(renderDocumentCard)
                            )}
                          </div>
                        </Fragment>
                      </CSSTransition>
                    ),
                  )}
                </TransitionGroup>
              )}
            </div>
            <div className="mt-6 border-t border-slate-200/50 pt-4 dark:border-slate-700">
              <div className="flex h-[400px] flex-col overflow-hidden">
                <ConversationSidebar
                  selectedConversationId={selectedConversationId}
                  onSelectConversation={(id) => {
                    setSelectedConversationId(id);
                  }}
                  onNewConversation={() => {
                    setSelectedConversationId(null);
                  }}
                />
              </div>
            </div>
          </div>
          <div className="md:col-span-2">
            <AIChat
              className="h-full"
              initialQuery={locationState.initialQuery}
              initialConversationIdProp={selectedConversationId}
              navigateTo={navigate}
              onConversationChange={(id) => {
                setSelectedConversationId(id);
              }}
              availableImages={documents.filter((doc) => isImageDocument(doc)).map((doc) => ({
                id: doc.id,
                title: doc.title,
                type: doc.type,
              }))}
              attachedImageIds={attachedImages}
              onAttachedImagesChange={setAttachedImages}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
