import { defineStore } from 'pinia'
import { ElMessage } from 'element-plus'
import { request } from '../utils/request'
import { Course, CourseProgress } from '../api/course'

interface DanceState {
  courses: Course[]
  currentCourse: Course | null
  favorites: number[]
  progress: Record<number, number>
  loading: boolean
  error: string | null
}

export const useDanceStore = defineStore('dance', {
  state: (): DanceState => ({
    courses: [],
    currentCourse: null,
    favorites: [],
    progress: {},
    loading: false,
    error: null
  }),
  
  getters: {
    getCourseById: (state) => (id: number) => {
      return state.courses.find(course => course.id === id)
    },
    getFavoriteCourses: (state) => {
      return state.courses.filter(course => state.favorites.includes(course.id))
    },
    getCourseProgress: (state) => (courseId: number) => {
      return state.progress[courseId] || 0
    }
  },
  
  actions: {
    // 获取所有课程
    async fetchCourses() {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Course[]>('/v1/courses')
        this.courses = data
        return data
      } catch (error: any) {
        this.error = error.message || '获取课程失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取课程详情
    async fetchCourseById(id: number) {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Course>(`/v1/courses/${id}`)
        this.currentCourse = data
        // 更新课程列表中的对应项
        const index = this.courses.findIndex(c => c.id === id)
        if (index !== -1) {
          this.courses[index] = data
        }
        return data
      } catch (error: any) {
        this.error = error.message || '获取课程详情失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取收藏的课程
    async fetchFavorites() {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Course[]>('/v1/courses/favorites')
        this.favorites = data.map(course => course.id)
        return data
      } catch (error: any) {
        this.error = error.message || '获取收藏课程失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 收藏/取消收藏课程
    async toggleFavorite(courseId: number) {
      try {
        const isFavorite = this.favorites.includes(courseId)
        if (isFavorite) {
          await request.delete<{ success: boolean }>(`/v1/courses/${courseId}/favorite`)
          this.favorites = this.favorites.filter(id => id !== courseId)
          ElMessage.success('已取消收藏')
        } else {
          await request.post<{ success: boolean }>(`/v1/courses/${courseId}/favorite`)
          this.favorites.push(courseId)
          ElMessage.success('已收藏课程')
        }
        return !isFavorite
      } catch (error: any) {
        ElMessage.error(error.message || '操作失败')
        throw error
      }
    },
    
    // 更新课程进度
    async updateProgress(courseId: number, progress: number) {
      try {
        await request.post<CourseProgress>(`/v1/courses/${courseId}/progress`, { progress })
        this.progress[courseId] = progress
        return progress
      } catch (error: any) {
        ElMessage.error(error.message || '更新进度失败')
        throw error
      }
    },
    
    // 获取课程进度
    async fetchProgress() {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<CourseProgress[]>('/v1/courses/progress')
        this.progress = data.reduce((acc, item) => {
          acc[item.courseId] = item.progress
          return acc
        }, {} as Record<number, number>)
        return data
      } catch (error: any) {
        this.error = error.message || '获取进度失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 