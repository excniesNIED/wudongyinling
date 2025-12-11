import { defineStore } from 'pinia'
import { request } from '../utils/request'
import { ElMessage } from 'element-plus'

// 定义接口
interface HealthRecord {
  id: number
  userId: number
  type: string
  value: number
  unit: string
  date: string
  notes?: string
  [key: string]: any
}

interface Prescription {
  id: number
  userId: number
  title: string
  description: string
  exercises: PrescriptionExercise[]
  status: 'active' | 'completed' | 'cancelled'
  startDate: string
  endDate?: string
  createdBy: number
  createdAt: string
  updatedAt: string
}

interface PrescriptionExercise {
  id: number
  name: string
  description: string
  duration: number
  frequency: string
  sets?: number
  reps?: number
  imageUrl?: string
  videoUrl?: string
}

interface HealthState {
  healthData: HealthRecord[]
  currentHealthRecord: HealthRecord | null
  prescriptions: Prescription[]
  currentPrescription: Prescription | null
  loading: boolean
  error: string | null
}

export const useHealthStore = defineStore('health', {
  state: (): HealthState => ({
    healthData: [],
    currentHealthRecord: null,
    prescriptions: [],
    currentPrescription: null,
    loading: false,
    error: null
  }),
  
  getters: {
    getLatestHealthData: (state) => {
      if (!state.healthData.length) return null
      return state.healthData.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0]
    },
    
    getHealthDataByType: (state) => (type: string) => {
      return state.healthData.filter(data => data.type === type)
    },
    
    getActivePrescriptions: (state) => {
      return state.prescriptions.filter(prescription => prescription.status === 'active')
    }
  },
  
  actions: {
    // 获取健康数据
    async fetchHealthData() {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<HealthRecord[]>('/v1/health')
        this.healthData = data
        return data
      } catch (error: any) {
        this.error = error.message || '获取健康数据失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取健康数据详情
    async fetchHealthRecordById(id: number) {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<HealthRecord>(`/v1/health/${id}`)
        this.currentHealthRecord = data
        return data
      } catch (error: any) {
        this.error = error.message || '获取健康记录详情失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 添加健康数据
    async addHealthRecord(record: Omit<HealthRecord, 'id'>) {
      try {
        this.loading = true
        this.error = null
        const data = await request.post<HealthRecord>('/v1/health', record)
        this.healthData.push(data)
        ElMessage.success('健康数据添加成功')
        return data
      } catch (error: any) {
        this.error = error.message || '添加健康数据失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 更新健康数据
    async updateHealthRecord(id: number, record: Partial<HealthRecord>) {
      try {
        this.loading = true
        this.error = null
        const data = await request.put<HealthRecord>(`/v1/health/${id}`, record)
        const index = this.healthData.findIndex(item => item.id === id)
        if (index !== -1) {
          this.healthData[index] = data
        }
        ElMessage.success('健康数据更新成功')
        return data
      } catch (error: any) {
        this.error = error.message || '更新健康数据失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取处方列表
    async fetchPrescriptions() {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Prescription[]>('/v1/prescriptions')
        this.prescriptions = data
        return data
      } catch (error: any) {
        this.error = error.message || '获取处方列表失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取处方详情
    async fetchPrescriptionById(id: number) {
      try {
        this.loading = true
        this.error = null
        const data = await request.get<Prescription>(`/v1/prescriptions/${id}`)
        this.currentPrescription = data
        return data
      } catch (error: any) {
        this.error = error.message || '获取处方详情失败'
        ElMessage.error(this.error as string)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 