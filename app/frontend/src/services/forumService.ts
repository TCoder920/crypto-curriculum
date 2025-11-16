/** Forum service for API calls */
import { apiClient } from './api';

export interface ForumPost {
  id: number;
  module_id: number | null;
  user_id: number;
  parent_post_id: number | null;
  title: string | null;
  content: string;
  is_pinned: boolean;
  is_solved: boolean;
  upvotes: number;
  created_at: string;
  updated_at: string | null;
  author: {
    id: number;
    username: string | null;
    full_name: string | null;
    role: string;
  };
  reply_count: number;
  user_vote: 'upvote' | 'downvote' | null;
}

export interface ForumPostListResponse {
  posts: ForumPost[];
  total: number;
  limit: number;
  offset: number;
}

export interface ForumPostCreate {
  module_id?: number | null;
  title?: string | null;
  content: string;
  parent_post_id?: number | null;
}

export interface ForumPostUpdate {
  title?: string | null;
  content?: string | null;
}

export interface ForumVoteCreate {
  vote_type: 'upvote' | 'downvote';
}

export const forumService = {
  /** Get forum posts for a module */
  getModulePosts: async (
    moduleId: number,
    sort: 'recent' | 'popular' | 'unsolved' = 'recent',
    limit: number = 20,
    offset: number = 0
  ): Promise<ForumPostListResponse> => {
    const response = await apiClient.get(`/forums/modules/${moduleId}/posts`, {
      params: { sort, limit, offset },
    });
    return response.data;
  },

  /** Get a single forum post */
  getPost: async (postId: number): Promise<ForumPost> => {
    const response = await apiClient.get(`/forums/posts/${postId}`);
    return response.data;
  },

  /** Get replies to a post */
  getPostReplies: async (postId: number): Promise<ForumPost[]> => {
    const response = await apiClient.get(`/forums/posts/${postId}/replies`);
    return response.data;
  },

  /** Create a new forum post or reply */
  createPost: async (postData: ForumPostCreate): Promise<ForumPost> => {
    const response = await apiClient.post('/forums/posts', postData);
    return response.data;
  },

  /** Update a forum post */
  updatePost: async (postId: number, postData: ForumPostUpdate): Promise<ForumPost> => {
    const response = await apiClient.patch(`/forums/posts/${postId}`, postData);
    return response.data;
  },

  /** Vote on a forum post */
  votePost: async (postId: number, voteType: 'upvote' | 'downvote'): Promise<void> => {
    await apiClient.post(`/forums/posts/${postId}/vote`, { vote_type: voteType });
  },

  /** Mark a post as solved */
  markSolved: async (postId: number): Promise<ForumPost> => {
    const response = await apiClient.patch(`/forums/posts/${postId}/solve`);
    return response.data;
  },

  /** Pin/unpin a post (instructor/admin only) */
  pinPost: async (postId: number): Promise<ForumPost> => {
    const response = await apiClient.patch(`/forums/posts/${postId}/pin`);
    return response.data;
  },

  /** Search forum posts */
  searchPosts: async (
    query: string,
    moduleId?: number,
    limit: number = 20,
    offset: number = 0
  ): Promise<ForumPostListResponse> => {
    const response = await apiClient.get('/forums/search', {
      params: { q: query, module_id: moduleId, limit, offset },
    });
    return response.data;
  },
};

