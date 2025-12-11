import { request } from '../utils/request'

// 健康记录接口
export interface HealthRecord {
  id: number
  user_id: number
  date: string
  height?: number
  weight?: number
  heart_rate?: number
  blood_pressure?: {
    systolic: number
    diastolic: number
  }
  blood_oxygen?: number
  body_fat?: number
  muscle_mass?: number
  sleep_hours?: number
  steps?: number
  exercise_duration?: number
  note?: string
  created_at?: string
  updated_at?: string
}

// 健康记录查询参数
export interface HealthRecordParams {
  skip?: number
  limit?: number
  user_id?: number
  start_date?: string
  end_date?: string
}

// 处方接口
export interface Prescription {
  id: number
  user_id: number
  title: string
  description?: string
  created_at: string
  expires_at?: string
  doctor_id?: number
  doctor_name?: string
  status: 'active' | 'completed' | 'expired'
  exercises: PrescriptionExercise[]
}

// 处方运动项目接口
export interface PrescriptionExercise {
  id: number
  prescription_id: number
  name: string
  description?: string
  duration?: number
  frequency?: string
  intensity?: string
  image_url?: string
  video_url?: string
  order?: number
}

// 健康目标接口
export interface HealthGoal {
  id: number
  user_id: number
  title: string
  target_value: number
  current_value: number
  unit: string
  category: 'weight' | 'steps' | 'exercise' | 'sleep' | 'other'
  start_date: string
  target_date: string
  status: 'active' | 'achieved' | 'failed'
}

/**
 * 健康相关API
 */
export const healthApi = {
  /**
   * 获取健康记录列表
   * @param params 查询参数
   */
  getHealthRecords(params?: HealthRecordParams) {
    return request.get<{ items: HealthRecord[], total: number }>('/v1/health', params)
  },
  
  /**
   * 获取健康记录详情
   * @param id 记录ID
   */
  getHealthRecordById(id: number) {
    return request.get<HealthRecord>(`/v1/health/${id}`)
  },
  
  /**
   * 创建健康记录
   * @param data 健康记录数据
   */
  createHealthRecord(data: Partial<HealthRecord>) {
    return request.post<HealthRecord>('/v1/health', data)
  },
  
  /**
   * 更新健康记录
   * @param id 记录ID
   * @param data 健康记录数据
   */
  updateHealthRecord(id: number, data: Partial<HealthRecord>) {
    return request.put<HealthRecord>(`/v1/health/${id}`, data)
  },
  
  /**
   * 删除健康记录
   * @param id 记录ID
   */
  deleteHealthRecord(id: number) {
    return request.delete(`/v1/health/${id}`)
  },
  
  /**
   * 获取健康统计数据
   * @param userId 用户ID
   * @param days 统计天数
   */
  getHealthStatistics(userId: number, days: number = 30) {
    return request.get(`/v1/health/statistics/${userId}`, { days })
  },
  
  /**
   * 获取处方列表
   * @param params 查询参数
   */
  getPrescriptions(params?: { skip?: number, limit?: number, user_id?: number, status?: string }) {
    return request.get<{ items: Prescription[], total: number }>('/v1/prescriptions', params)
  },
  
  /**
   * 获取处方详情
   * @param id 处方ID
   */
  getPrescriptionById(id: number) {
    return request.get<Prescription>(`/v1/prescriptions/${id}`)
  },
  
  /**
   * 创建处方
   * @param data 处方数据
   */
  createPrescription(data: Partial<Prescription>) {
    return request.post<Prescription>('/v1/prescriptions', data)
  },
  
  /**
   * 更新处方
   * @param id 处方ID
   * @param data 处方数据
   */
  updatePrescription(id: number, data: Partial<Prescription>) {
    return request.put<Prescription>(`/v1/prescriptions/${id}`, data)
  },
  
  /**
   * 删除处方
   * @param id 处方ID
   */
  deletePrescription(id: number) {
    return request.delete(`/v1/prescriptions/${id}`)
  },
  
  /**
   * 获取健康目标列表
   * @param userId 用户ID
   */
  getHealthGoals(userId?: number) {
    const params = userId ? { user_id: userId } : {}
    return request.get<HealthGoal[]>('/v1/health/goals', params)
  },
  
  /**
   * 创建健康目标
   * @param data 目标数据
   */
  createHealthGoal(data: Partial<HealthGoal>) {
    return request.post<HealthGoal>('/v1/health/goals', data)
  },
  
  /**
   * 更新健康目标
   * @param id 目标ID
   * @param data 目标数据
   */
  updateHealthGoal(id: number, data: Partial<HealthGoal>) {
    return request.put<HealthGoal>(`/v1/health/goals/${id}`, data)
  },
  
  /**
   * 删除健康目标
   * @param id 目标ID
   */
  deleteHealthGoal(id: number) {
    return request.delete(`/v1/health/goals/${id}`)
  }
} 