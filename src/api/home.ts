import { request } from '../utils/request'
import { Course } from './course'

// 轮播图接口
export interface Banner {
  id: number
  image: string
  title: string
  subtitle?: string
  link?: string
  sort_order?: number
}

// 新闻接口
export interface News {
  id: number
  title: string
  summary: string
  content?: string
  cover_image?: string
  publish_date: string
  view_count?: number
  author?: string
  tags?: string[]
}

// 首页信息接口
export interface HomeInfo {
  banners: Banner[]
  popularCourses: Course[]
  latestNews: News[]
  featuredEvents: any[]
  stats: {
    userCount: number
    courseCount: number
    completionRate: number
  }
}

/**
 * 首页相关API
 * 注意：request.ts已设置baseURL为/api/v1，因此路径需要以/v1开头
 */
export const homeApi = {
  /**
   * 获取首页数据
   */
  getHomeInfo() {
    return request.get<HomeInfo>('/v1/home')
  },
  
  /**
   * 获取轮播图列表
   */
  getBanners() {
    return request.get<Banner[]>('/v1/home/banners')
  },
  
  /**
   * 获取推荐课程
   * @param limit 限制数量
   */
  getRecommendedCourses(limit: number = 6) {
    return request.get<Course[]>('/v1/courses/recommended', { limit })
  },
  
  /**
   * 获取最新新闻
   * @param limit 限制数量
   */
  getLatestNews(limit: number = 3) {
    return request.get<News[]>('/v1/home/news/latest', { limit })
  },
  
  /**
   * 获取首页统计数据
   */
  getHomeStats() {
    return request.get<HomeInfo['stats']>('/v1/home/stats')
  }
} 