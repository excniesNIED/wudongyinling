import request from '@/utils/request'

// 所有管理端请求统一增加 /api/v1 前缀，确保与后端路由保持一致
const API_PREFIX = '/api/v1'

// 用户相关API
export const userApi = {
  login: (data) => request.post(`${API_PREFIX}/auth/login`, data),
  register: (data) => request.post(`${API_PREFIX}/auth/register`, data),
  getUsers: (params) => request.get(`${API_PREFIX}/users`, { params }),
  updateUser: (id, data) => request.put(`${API_PREFIX}/users/${id}`, data),
  deleteUser: (id) => request.delete(`${API_PREFIX}/users/${id}`)
}

// 课程相关API
export const courseApi = {
  getCourses: (params) => request.get(`${API_PREFIX}/courses`, { params }),
  createCourse: (data) => request.post(`${API_PREFIX}/courses`, data),
  updateCourse: (id, data) => request.put(`${API_PREFIX}/courses/${id}`, data),
  deleteCourse: (id) => request.delete(`${API_PREFIX}/courses/${id}`),
  // fileType 可为 'video' 或 'image'
  upload: (fileType, data) => request.post(`${API_PREFIX}/courses/upload/${fileType}`, data)
}

// 健康记录API
export const healthApi = {
  getRecords: (params) => request.get(`${API_PREFIX}/health`, { params }),
  createRecord: (data) => request.post(`${API_PREFIX}/health`, data),
  updateRecord: (id, data) => request.put(`${API_PREFIX}/health/${id}`, data),
  deleteRecord: (id) => request.delete(`${API_PREFIX}/health/${id}`),
  getRealtimeData: (userId) => `${API_PREFIX}/health/ws/${userId}` // WebSocket URL
}

// 运动处方API
export const prescriptionApi = {
  getPrescriptions: (params) => request.get(`${API_PREFIX}/prescriptions`, { params }),
  createPrescription: (data) => request.post(`${API_PREFIX}/prescriptions`, data),
  updatePrescription: (id, data) => request.put(`${API_PREFIX}/prescriptions/${id}`, data),
  deletePrescription: (id) => request.delete(`${API_PREFIX}/prescriptions/${id}`)
}

// 打卡挑战API
export const challengeApi = {
  getChallenges: (params) => request.get(`${API_PREFIX}/challenges`, { params }),
  createChallenge: (data) => request.post(`${API_PREFIX}/challenges`, data),
  updateChallenge: (id, data) => request.put(`${API_PREFIX}/challenges/${id}`, data),
  deleteChallenge: (id) => request.delete(`${API_PREFIX}/challenges/${id}`),
  getRecords: (challengeId, params) => request.get(`${API_PREFIX}/challenges/${challengeId}/records`, { params }),
  getChallenge: (challengeId) => request.get(`${API_PREFIX}/challenges/${challengeId}`),
  joinChallenge: (challengeId, userId) => request.post(`${API_PREFIX}/challenges/${challengeId}/join`, null, { params: { user_id: userId } }),
  checkIn: (challengeId, userId) => request.post(`${API_PREFIX}/challenges/${challengeId}/check-in`, null, { params: { user_id: userId } })
}

// AI分析API
export const aiApi = {
  analyzeVideo: (data) => request.post(`${API_PREFIX}/ai/analyze`, data),
  getFeedback: (videoUrl) => request.post(`${API_PREFIX}/ai/feedback`, { video_url: videoUrl }),
  compareVideos: (data) => request.post(`${API_PREFIX}/ai/compare`, data),
  
}

// 统计数据API
export const statsApi = {
  getDashboardStats: () => request.get(`${API_PREFIX}/stats/dashboard`),
  getUserStats: () => request.get(`${API_PREFIX}/stats/users`),
  getCourseStats: () => request.get(`${API_PREFIX}/stats/courses`),
  getChallengeStats: () => request.get(`${API_PREFIX}/stats/challenges`)
}