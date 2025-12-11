import { request } from '../utils/request'

// AI分析结果接口
export interface AIAnalysisResult {
  id?: number
  score: number
  feedback: string
  keypoints?: any[]
  improvements: string[]
  video_url?: string
  created_at?: string
}

// AI教练建议接口
export interface AIAdvice {
  id?: number
  question: string
  answer: string
  created_at?: string
}

// 聊天消息接口
export interface ChatMessage {
  id?: number
  sender: 'user' | 'ai'
  content: string
  timestamp: string
}

// 聊天会话接口
export interface ChatSession {
  id: number
  title: string
  created_at: string
  last_message?: string
  last_message_time?: string
}

/**
 * AI教练相关API
 * 注意：所有路径需要以/v1开头以匹配后端路由
 */
export const aiCoachApi = {
  /**
   * 分析舞蹈视频
   * @param formData 包含视频文件的FormData
   */
  analyzeDance(formData: FormData) {
    return request.post<AIAnalysisResult>('/v1/ai-analysis/analyze', formData)
  },
  
  /**
   * 获取AI教练建议
   * @param question 用户问题
   */
  getAIAdvice(question: string) {
    return request.post<AIAdvice>('/v1/ai-analysis/coach-advice', { question })
  },
  
  /**
   * 获取分析历史记录
   * @param params 查询参数
   */
  getAnalysisHistory(params?: { skip?: number, limit?: number }) {
    return request.get<{ items: AIAnalysisResult[], total: number }>('/v1/ai-analysis/history', params)
  },
  
  /**
   * 获取特定分析结果详情
   * @param id 分析结果ID
   */
  getAnalysisById(id: number) {
    return request.get<AIAnalysisResult>(`/v1/ai-analysis/${id}`)
  },
  
  /**
   * 获取健康数据分析
   * @param userId 用户ID
   * @param days 统计天数
   */
  analyzeHealthData(userId: number, days: number = 30) {
    return request.post<any>(`/v1/ai-analysis/health/${userId}`, { days })
  },
  
  /**
   * 获取聊天会话列表
   */
  getChatSessions() {
    return request.get<ChatSession[]>('/v1/chat/sessions')
  },
  
  /**
   * 创建新的聊天会话
   */
  createChatSession(title: string = '新会话') {
    return request.post<ChatSession>('/v1/chat/sessions', { title })
  },
  
  /**
   * 获取会话消息
   * @param sessionId 会话ID
   */
  getChatMessages(sessionId: number) {
    return request.get<ChatMessage[]>(`/v1/chat/sessions/${sessionId}/messages`)
  },
  
  /**
   * 发送聊天消息
   * @param sessionId 会话ID
   * @param content 消息内容
   */
  sendChatMessage(sessionId: number, content: string) {
    return request.post<ChatMessage>(`/v1/chat/sessions/${sessionId}/messages`, { content })
  },
  
  /**
   * 删除聊天会话
   * @param sessionId 会话ID
   */
  deleteChatSession(sessionId: number) {
    return request.delete(`/v1/chat/sessions/${sessionId}`)
  }
} 