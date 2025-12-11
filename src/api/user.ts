import { request } from '../utils/request'

// 用户数据接口
export interface UserData {
  id: number
  username: string
  email: string
  nickname?: string
  avatar?: string
  phone?: string
  role: 'admin' | 'teacher' | 'user'
  is_active: boolean
  created_at?: string
  [key: string]: any
}

// 分页结果接口
export interface PaginatedResult<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

// 用户查询参数
export interface UserQueryParams {
  skip?: number
  limit?: number
  search?: string
  role?: string
  is_active?: boolean
}

// 登录参数
export interface LoginParams {
  username: string
  password: string
}

// 注册参数
export interface RegisterParams {
  username: string
  email: string
  password: string
  role?: 'admin' | 'teacher' | 'user'
  is_active?: boolean
}

/**
 * 用户相关API
 */
export const userApi = {
  /**
   * 用户登录
   * @param data 登录参数
   */
  login(data: LoginParams) {
    return request.post<{token: string, user: UserData}>('/v1/auth/login', data)
  },

  /**
   * 管理员登录
   * @param data 登录参数
   */
  adminLogin(data: LoginParams) {
    return request.post<{token: string, user: UserData}>('/v1/auth/login', data)
  },

  /**
   * 用户注册
   * @param data 注册参数
   */
  register(data: RegisterParams) {
    return request.post<UserData>('/v1/auth/register', data)
  },

  /**
   * 退出登录
   */
  logout() {
    return request.post('/v1/auth/logout')
  },

  /**
   * 获取用户列表
   * @param params 查询参数
   */
  getUsers(params?: UserQueryParams) {
    return request.get<PaginatedResult<UserData>>('/v1/users', params)
  },

  /**
   * 获取用户详情
   * @param id 用户ID
   */
  getUserById(id: number) {
    return request.get<UserData>(`/v1/users/${id}`)
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser() {
    return request.get<UserData>('/v1/users/me')
  },

  /**
   * 创建用户
   * @param data 用户数据
   */
  createUser(data: RegisterParams) {
    return request.post<UserData>('/v1/users', data)
  },

  /**
   * 更新用户
   * @param id 用户ID
   * @param data 用户数据
   */
  updateUser(id: number, data: Partial<UserData>) {
    return request.put<UserData>(`/v1/users/${id}`, data)
  },

  /**
   * 删除用户
   * @param id 用户ID
   */
  deleteUser(id: number) {
    return request.delete(`/v1/users/${id}`)
  },

  /**
   * 修改用户密码
   * @param id 用户ID
   * @param data 密码数据
   */
  changePassword(id: number, data: { old_password: string, new_password: string }) {
    return request.put(`/v1/users/${id}/password`, data)
  },

  /**
   * 重置用户密码（管理员操作）
   * @param id 用户ID
   * @param data 新密码
   */
  resetPassword(id: number, data: { password: string }) {
    return request.put(`/v1/users/${id}/reset-password`, data)
  },

  /**
   * 上传用户头像
   * @param id 用户ID
   * @param formData 包含头像文件的FormData
   */
  uploadAvatar(id: number, formData: FormData) {
    return request.post<{avatar_url: string}>(`/v1/users/${id}/avatar`, formData)
  }
} 