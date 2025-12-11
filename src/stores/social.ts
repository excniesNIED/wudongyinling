import { defineStore } from 'pinia'
import { request } from '../utils/request'
import { ElMessage } from 'element-plus'

// 定义接口
interface Feed {
  id: number
  userId: number
  content: string
  images?: string[]
  video?: string
  likes: number
  commentCount: number
  isLiked: boolean
  createdAt: string
  updatedAt: string
  user: {
    id: number
    username: string
    nickname: string
    avatar?: string
  }
  [key: string]: any
}

interface Comment {
  id: number
  feedId: number
  userId: number
  content: string
  createdAt: string
  user: {
    id: number
    username: string
    nickname: string
    avatar?: string
  }
}

interface FeedParams {
  page?: number
  limit?: number
  userId?: number
  keyword?: string
  [key: string]: any
}

interface SocialState {
  feeds: Feed[]
  currentFeed: Feed | null
  comments: Record<number, Comment[]>
  loading: boolean
  error: string | null
}

export const useSocialStore = defineStore('social', {
  state: (): SocialState => ({
    feeds: [],
    currentFeed: null,
    comments: {},
    loading: false,
    error: null
  }),
  
  getters: {
    getFeedById: (state) => (id: number) => {
      return state.feeds.find(feed => feed.id === id)
    },
    
    getCommentsByFeedId: (state) => (feedId: number) => {
      return state.comments[feedId] || []
    }
  },
  
  actions: {
    // 获取动态列表
    async fetchFeeds(params: FeedParams = {}) {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Feed[]>('/v1/social/feeds', params)
        this.feeds = data
        return data
      } catch (error: any) {
        this.error = error.message || '获取动态失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取动态详情
    async fetchFeedById(id: number) {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Feed>(`/v1/social/feeds/${id}`)
        this.currentFeed = data
        // 更新列表中的动态
        const index = this.feeds.findIndex(feed => feed.id === id)
        if (index !== -1) {
          this.feeds[index] = data
        }
        return data
      } catch (error: any) {
        this.error = error.message || '获取动态详情失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 发布动态
    async createFeed(feed: Omit<Feed, 'id' | 'likes' | 'commentCount' | 'isLiked' | 'createdAt' | 'updatedAt' | 'user'>) {
      try {
        this.loading = true
        this.error = null
        const data = await request.post<Feed>('/v1/social/feeds', feed)
        this.feeds.unshift(data)
        ElMessage.success('发布成功')
        return data
      } catch (error: any) {
        this.error = error.message || '发布动态失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 点赞/取消点赞
    async toggleLike(feedId: number) {
      try {
        const feed = this.getFeedById(feedId)
        if (!feed) return false
        
        const isLiked = feed.isLiked
        const data = await request.post<{ likes: number }>(`/v1/social/feeds/${feedId}/like`, { action: isLiked ? 'unlike' : 'like' })
        
        // 更新动态
        const index = this.feeds.findIndex(f => f.id === feedId)
        if (index !== -1) {
          this.feeds[index] = { ...this.feeds[index], isLiked: !isLiked, likes: data.likes }
        }
        
        // 如果当前查看的是该动态，也更新currentFeed
        if (this.currentFeed?.id === feedId) {
          this.currentFeed = { ...this.currentFeed, isLiked: !isLiked, likes: data.likes }
        }
        
        return !isLiked
      } catch (error: any) {
        ElMessage.error(error.message || '操作失败')
        throw error
      }
    },
    
    // 获取评论
    async fetchComments(feedId: number) {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Comment[]>(`/v1/social/feeds/${feedId}/comments`)
        this.comments = { ...this.comments, [feedId]: data }
        return data
      } catch (error: any) {
        this.error = error.message || '获取评论失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 发表评论
    async postComment(feedId: number, content: string) {
      try {
        this.loading = true
        this.error = null
        const data = await request.post<Comment>(`/v1/social/feeds/${feedId}/comments`, { content })
        
        // 更新评论列表
        if (!this.comments[feedId]) {
          this.comments[feedId] = []
        }
        this.comments[feedId].push(data)
        
        // 更新动态中的评论计数
        const feedIndex = this.feeds.findIndex(f => f.id === feedId)
        if (feedIndex !== -1) {
          this.feeds[feedIndex].commentCount = (this.feeds[feedIndex].commentCount || 0) + 1
        }
        
        // 如果当前查看的是该动态，也更新currentFeed
        if (this.currentFeed?.id === feedId) {
          this.currentFeed.commentCount = (this.currentFeed.commentCount || 0) + 1
        }
        
        ElMessage.success('评论成功')
        return data
      } catch (error: any) {
        this.error = error.message || '发表评论失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 