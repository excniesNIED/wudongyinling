import { request } from '@/utils/request'

// 动态广场相关接口
export interface Post {
  id: number
  user_id: number
  user?: {
    id: number
    username: string
    nickname: string
    avatar?: string
  }
  post_type: 'text' | 'image' | 'video' | 'dance' | 'heritage'
  content: string
  media_url?: string
  likes_count: number
  comments_count: number
  shares_count: number
  is_public: boolean
  is_featured: boolean
  created_at: string
  updated_at: string
}

export interface PostCreate {
  post_type: 'text' | 'image' | 'video' | 'dance' | 'heritage'
  content: string
  media_url?: string
  is_public?: boolean
}

export interface PostComment {
  id: number
  post_id: number
  user_id: number
  user?: {
    id: number
    username: string
    nickname: string
    avatar?: string
  }
  content: string
  parent_id?: number
  created_at: string
}

export interface CommentCreate {
  content: string
  post_id: number
  parent_id?: number
}

// 非遗传承相关接口
export interface HeritageProject {
  id: number
  name: string
  category: string
  level: 'national' | 'provincial' | 'municipal' | 'county'
  description: string
  history: string
  techniques: string
  current_status: string
  protection_measures: string
  image_url?: string
  video_url?: string
  status: 'active' | 'inactive'
  created_at: string
  updated_at: string
}

export interface HeritageInheritor {
  id: number
  name: string
  gender: 'male' | 'female'
  birth_year: number
  hometown: string
  bio: string
  achievements: string
  inheritance_years: number
  teaching_experience: string
  representative_works: string
  contact_info: string
  avatar_url?: string
  status: 'active' | 'inactive'
  created_at: string
  updated_at: string
}

export interface HeritageProjectCreate {
  name: string
  description: string
  origin_location: string
  category: string
  level: string
  cover_image?: string
  video_url?: string
  history?: string
  characteristics?: string
  inheritor_id?: number
}

export interface InheritorCreate {
  name: string
  gender: 'male' | 'female'
  birth_year: number
  hometown: string
  specialty: string
  avatar?: string
  bio?: string
}

// 动态广场API
export const postApi = {
  // 获取动态列表
  getPosts: (params?: {
    page?: number
    page_size?: number
    post_type?: string
    user_role?: string
    is_public?: boolean
    is_featured?: boolean
  }) => {
    return request.get('/v1/social/posts', params)
  },

  // 创建动态
  createPost: (data: PostCreate) => {
    return request.post('/v1/social/posts', data)
  },

  // 获取动态详情
  getPost: (id: number) => {
    return request.get(`/v1/social/posts/${id}`)
  },

  // 更新动态
  updatePost: (id: number, data: Partial<PostCreate>) => {
    return request.put(`/v1/social/posts/${id}`, data)
  },

  // 删除动态
  deletePost: (id: number) => {
    return request.delete(`/v1/social/posts/${id}`)
  },

  // 获取动态评论
  getPostComments: (postId: number, params?: {
    page?: number
    page_size?: number
  }) => {
    return request.get(`/v1/social/posts/${postId}/comments`, params)
  },

  // 添加评论
  addComment: (postId: number, data: CommentCreate) => {
    return request.post(`/v1/social/posts/${postId}/comments`, data)
  },

  // 点赞动态
  likePost: (postId: number) => {
    return request.post(`/v1/social/posts/${postId}/like`)
  },

  // 取消点赞
  unlikePost: (postId: number) => {
    return request.delete(`/v1/social/posts/${postId}/like`)
  },

  // 分享动态
  sharePost: (postId: number) => {
    return request.post(`/v1/social/posts/${postId}/share`)
  },

  // 举报动态
  reportPost: (postId: number, data: { reason: string; description?: string }) => {
    return request.post(`/v1/social/posts/${postId}/report`, data)
  },

  // 获取用户动态
  getUserPosts: (userId: number, params?: {
    page?: number
    page_size?: number
  }) => {
    return request.get(`/v1/social/users/${userId}/posts`, params)
  },

  // 获取关注用户的动态
  getFollowingPosts: (params?: {
    page?: number
    page_size?: number
  }) => {
    return request.get('/v1/social/following/posts', params)
  },

  // 获取热门动态
  getTrendingPosts: (params?: {
    page?: number
    page_size?: number
    timeframe?: 'day' | 'week' | 'month'
  }) => {
    return request.get('/v1/social/posts/trending', params)
  },

  // 非遗传承相关接口
  // 获取非遗项目
  getProjects: (params?: {
    page?: number
    page_size?: number
    category?: string
    region?: string
  }) => {
    return request.get('/v1/social/heritage/projects', params)
  },

  // 获取项目详情
  getProject: (id: number) => {
    return request.get(`/v1/social/heritage/projects/${id}`)
  },

  // 创建非遗项目
  createProject: (data: HeritageProjectCreate) => {
    return request.post('/v1/social/heritage/projects', data)
  },

  // 更新非遗项目
  updateProject: (id: number, data: Partial<HeritageProjectCreate>) => {
    return request.put(`/v1/social/heritage/projects/${id}`, data)
  },

  // 删除非遗项目
  deleteProject: (id: number) => {
    return request.delete(`/v1/social/heritage/projects/${id}`)
  },

  // 获取传承人
  getInheritors: (params?: {
    page?: number
    page_size?: number
    project_id?: number
    region?: string
  }) => {
    return request.get('/v1/social/heritage/inheritors', params)
  },

  // 获取传承人详情
  getInheritor: (id: number) => {
    return request.get(`/v1/social/heritage/inheritors/${id}`)
  },

  // 创建传承人
  createInheritor: (data: InheritorCreate) => {
    return request.post('/v1/social/heritage/inheritors', data)
  },

  // 更新传承人
  updateInheritor: (id: number, data: Partial<InheritorCreate>) => {
    return request.put(`/v1/social/heritage/inheritors/${id}`, data)
  },

  // 删除传承人
  deleteInheritor: (id: number) => {
    return request.delete(`/v1/social/heritage/inheritors/${id}`)
  },

  // 加入非遗计划
  joinHeritageProject: (projectId: number, userId: number) => {
    return request.post(`/v1/social/heritage/projects/${projectId}/join`, { user_id: userId })
  },

  // 退出非遗计划
  leaveHeritageProject: (projectId: number, userId: number) => {
    return request.post(`/v1/social/heritage/projects/${projectId}/leave`, { user_id: userId })
  }
}

// 导出socialApi别名，保持与其他API模块的一致性
export const socialApi = postApi 