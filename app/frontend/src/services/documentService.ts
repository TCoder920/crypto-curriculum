import { apiClient } from './api';

export interface ReferenceDocument {
  id: number;
  title: string;
  category: 'standard' | 'user-upload' | 'policy' | string;
  updated_at: string;
  tags?: string[];
  owner?: string;
  type?: string;
  filename?: string;
}

const IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'];
const TEXT_EXTENSIONS = ['pdf', 'docx', 'txt', 'md', 'csv'];

export function isImageDocument(doc: ReferenceDocument): boolean {
  const ext = doc.type?.toLowerCase() || doc.filename?.split('.').pop()?.toLowerCase() || '';
  return IMAGE_EXTENSIONS.includes(ext);
}

export function isTextDocument(doc: ReferenceDocument): boolean {
  const ext = doc.type?.toLowerCase() || doc.filename?.split('.').pop()?.toLowerCase() || '';
  return TEXT_EXTENSIONS.includes(ext);
}

class DocumentService {
  private cache: ReferenceDocument[] | null = null;
  private lastFetchedAt: number | null = null;
  private readonly ttl = 1000 * 60 * 5; // five minutes

  async listDocuments(force = false): Promise<ReferenceDocument[]> {
    const now = Date.now();

    if (!force && this.cache && this.lastFetchedAt && now - this.lastFetchedAt < this.ttl) {
      return this.cache;
    }

    const response = await apiClient.get('/documents/list');
    this.cache = response.data?.documents ?? response.data ?? [];
    this.lastFetchedAt = now;
    return this.cache;
  }

  openDocumentInNewTab(documentId: number): void {
    const token = localStorage.getItem('access_token');
    const url = `${apiClient.defaults.baseURL}/documents/download/${documentId}` + (token ? `?token=${token}` : '');
    window.open(url, '_blank', 'noopener');
  }

  async uploadDocument(
    file: File,
    moduleId?: number,
    courseScope?: string,
    onProgress?: (progress: number) => void
  ): Promise<ReferenceDocument> {
    const formData = new FormData();
    formData.append('file', file);
    if (moduleId) formData.append('module_id', moduleId.toString());
    if (courseScope) formData.append('course_scope', courseScope);

    const response = await apiClient.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    });

    // Invalidate cache to force refresh on next list call
    this.cache = null;
    this.lastFetchedAt = null;

    return response.data;
  }
}

export const documentService = new DocumentService();
