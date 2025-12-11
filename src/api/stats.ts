import { request } from '../utils/request'

// 仪表盘统计数据接口
export interface DashboardStats {
  totalUsers: number
  totalCourses: number
  totalChallenges: number
  totalHealthRecords: number
  activeUsers: number
  coursesByDifficulty: {
    [key: string]: number
  }
}

// 用户统计数据接口
export interface UserStats {
  total: number
  active: number
  byRole: {
    admin: number
    teacher: number
    user: number
  }
  registrationTrend: {
    date: string
    count: number
  }[]
}

// 课程统计数据接口
export interface CourseStats {
  popular: {
    id: number
    title: string
    enrollments: number
  }[]
  categories: {
    category: string
    count: number
  }[]
  completions: {
    date: string
    count: number
  }[]
}

// 挑战统计数据接口
export interface ChallengeStats {
  active: number
  completed: number
  participation: {
    date: string
    count: number
  }[]
  popular: {
    id: number
    title: string
    participants: number
  }[]
}

// 健康数据统计接口
export interface HealthStats {
  averageHeartRate: number
  averageBloodPressure: {
    systolic: number
    diastolic: number
  }
  averageWeight: number
  exerciseDuration: number
  trend: {
    date: string
    heartRate?: number
    bloodPressure?: {
      systolic: number
      diastolic: number
    }
    weight?: number
    exerciseDuration?: number
  }[]
}

/**
 * 统计数据API
 */
export const statsApi = {
  /**
   * 获取仪表盘统计数据
   */
  getDashboardStats() {
    return request.get<DashboardStats>('/v1/stats/dashboard')
  },

  /**
   * 获取用户统计数据
   */
  getUserStats() {
    return request.get<UserStats>('/v1/stats/users')
  },

  /**
   * 获取课程统计数据
   */
  getCourseStats() {
    return request.get<CourseStats>('/v1/stats/courses')
  },

  /**
   * 获取挑战统计数据
   */
  getChallengeStats() {
    return request.get<ChallengeStats>('/v1/stats/challenges')
  },
  
  /**
   * 获取指定用户的健康统计数据
   * @param userId 用户ID
   * @param days 统计天数
   */
  getUserHealthStats(userId: number, days: number = 30) {
    return request.get<HealthStats>(`/v1/stats/user/${userId}`, { days })
  },
  
  /**
   * 获取指定用户的活动统计数据
   * @param userId 用户ID
   */
  getUserActivityStats(userId: number) {
    return request.get<any>(`/v1/stats/user/${userId}/activity`)
  }
} 