import { request } from '../utils/request'

// 课程数据接口
export interface Course {
  id: number
  title: string
  description: string
  cover_url: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  duration: number
  instructor_id: number
  instructor_name?: string
  category?: string
  tags?: string[]
  video_url?: string
  enrolled_count?: number
  rating?: number
  created_at?: string
  updated_at?: string
  [key: string]: any
}

// 课程分类接口
export interface CourseCategory {
  id: number
  name: string
  code: string
  description?: string
  count?: number
}

// 课程难度接口
export interface CourseDifficulty {
  id: number
  name: string
  code: string
  description?: string
}

// 课程时长接口
export interface CourseDuration {
  id: number
  name: string
  min_minutes: number
  max_minutes: number
}

// 课程列表查询参数
export interface CourseParams {
  skip?: number
  limit?: number
  difficulty?: string
  keyword?: string
  instructor_id?: number
  min_duration?: number
  max_duration?: number
}

// 课程评论接口
export interface CourseComment {
  id: number
  course_id: number
  user_id: number
  user_name: string
  user_avatar?: string
  content: string
  rating?: number
  created_at: string
}

// 课程评论提交参数
export interface CourseCommentParams {
  content: string
  rating?: number
}

// 课程报名参数
export interface CourseEnrollParams {
  course_id: number
  user_id?: number
}

/**
 * 课程相关API
 */
export const courseApi = {
  /**
   * 获取课程列表
   * @param params 查询参数
   */
  getCourses(params?: CourseParams) {
    return request.get<{items: Course[], total: number}>('/v1/courses', params)
  },

  /**
   * 获取课程详情
   * @param id 课程ID
   */
  getCourseById(id: number) {
    return request.get<Course>(`/v1/courses/${id}`)
  },

  /**
   * 创建课程
   * @param data 课程数据
   */
  createCourse(data: Partial<Course>) {
    return request.post<Course>('/v1/courses', data)
  },

  /**
   * 更新课程
   * @param id 课程ID
   * @param data 课程数据
   */
  updateCourse(id: number, data: Partial<Course>) {
    return request.put<Course>(`/v1/courses/${id}`, data)
  },

  /**
   * 删除课程
   * @param id 课程ID
   */
  deleteCourse(id: number) {
    return request.delete(`/v1/courses/${id}`)
  },

  /**
   * 获取课程评论
   * @param courseId 课程ID
   */
  getCourseComments(courseId: number) {
    return request.get<CourseComment[]>(`/v1/courses/${courseId}/comments`)
  },

  /**
   * 提交课程评论
   * @param courseId 课程ID
   * @param data 评论数据
   */
  submitCourseComment(courseId: number, data: CourseCommentParams) {
    return request.post<CourseComment>(`/v1/courses/${courseId}/comments`, data)
  },

  /**
   * 报名课程
   * @param data 报名数据
   */
  enrollCourse(data: CourseEnrollParams) {
    return request.post<{success: boolean}>(`/v1/courses/${data.course_id}/enroll`, data)
  },

  /**
   * 获取用户已报名的课程
   * @param userId 用户ID，不传则获取当前登录用户
   */
  getUserCourses(userId?: number) {
    const url = userId ? `/v1/courses/user/${userId}` : '/v1/courses/user/me'
    return request.get<Course[]>(url)
  },

  /**
   * 获取课程推荐
   * @param limit 限制数量
   */
  getRecommendedCourses(limit: number = 5) {
    return request.get<Course[]>('/v1/courses/recommended', { limit })
  },

  /**
   * 获取热门课程
   * @param limit 限制数量
   */
  getPopularCourses(limit: number = 5) {
    return request.get<Course[]>('/v1/courses/popular', { limit })
  },

  /**
   * 更新课程封面
   * @param id 课程ID
   * @param formData 包含图片的FormData
   */
  updateCourseCover(id: number, formData: FormData) {
    return request.post<{cover_url: string}>(`/v1/courses/${id}/cover`, formData)
  },

  /**
   * 获取课程分类列表
   */
  getCourseCategories() {
    return request.get<CourseCategory[]>('/v1/courses/categories', undefined, {
      showError: false,
      retry: false,
      loading: false,
      headers: {}
    })
  },

  /**
   * 获取课程难度列表
   */
  getCourseDifficulties() {
    return request.get<CourseDifficulty[]>('/v1/courses/difficulties', undefined, {
      showError: false,
      retry: false,
      loading: false,
      headers: {}
    })
  },

  /**
   * 获取课程时长范围列表
   */
  getCourseDurations() {
    return request.get<CourseDuration[]>('/v1/courses/durations', undefined, {
      showError: false,
      retry: false,
      loading: false,
      headers: {}
    })
  }
} 