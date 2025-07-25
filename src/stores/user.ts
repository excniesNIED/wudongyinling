import { defineStore } from 'pinia'
import { request } from '../utils/request'
import { ElMessage } from 'element-plus'
import router from '../router'

// 定义接口
interface UserInfo {
  id: number
  username: string
  nickname?: string
  avatar?: string
  email?: string
  phone?: string
  [key: string]: any
}

interface UserState {
  token: string
  userInfo: UserInfo
  roles: string[]
  loading: boolean
  error: string | null
}

interface LoginCredentials {
  username: string
  password: string
  isAdmin?: boolean
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    roles: JSON.parse(localStorage.getItem('roles') || '[]'),
    loading: false,
    error: null
  }),
  
  getters: {
    isLoggedIn: (state): boolean => !!state.token,
    isAdmin: (state): boolean => state.roles.includes('admin'),
    username: (state): string => state.userInfo?.username || '',
    nickname: (state): string => state.userInfo?.nickname || state.userInfo?.username || ''
  },
  
  actions: {
    /**
     * 登录操作
     * @param credentials 登录凭证
     */
    async login(credentials: LoginCredentials) {
      try {
        this.loading = true
        this.error = null
        
        // 根据是否是管理员调用不同的登录接口
        const endpoint = credentials.isAdmin ? '/auth/admin/login' : '/auth/login'
        const data = await request.post(endpoint, credentials)
        
        // 保存登录信息
        this.setToken(data.token)
        this.setUserInfo(data.user)
        this.setRoles(data.roles || [])
        
        ElMessage.success('登录成功')
        
        // 登录成功后跳转
        if (credentials.isAdmin) {
          router.push('/admin')
        } else {
          router.push('/')
        }
        
        return data
      } catch (error: any) {
        this.error = error.message || '登录失败'
        ElMessage.error(this.error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 获取用户信息
     */
    async getUserInfo() {
      try {
        this.loading = true
        this.error = null
        
        // 判断是否是管理员
        const isAdmin = this.roles.includes('admin')
        const endpoint = isAdmin ? '/users/admin/me' : '/users/me'
        
        const data = await request.get(endpoint)
        this.setUserInfo(data)
        
        // 更新角色信息
        if (data.roles) {
          this.setRoles(data.roles)
        }
        
        return data
      } catch (error: any) {
        this.error = error.message || '获取用户信息失败'
        ElMessage.error(this.error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 管理员登录
     */
    async adminLogin(credentials: Omit<LoginCredentials, 'isAdmin'>) {
      return this.login({
        ...credentials,
        isAdmin: true
      })
    },
    
    /**
     * 退出登录
     */
    async logout() {
      try {
        const isAdmin = this.roles.includes('admin')
        const endpoint = isAdmin ? '/auth/admin/logout' : '/auth/logout'
        
        await request.post(endpoint)
        ElMessage.success('已退出登录')
      } catch (error) {
        console.error('退出登录失败', error)
      } finally {
        this.resetState()
        
        // 根据当前路径判断跳转目标
        if (router.currentRoute.value.path.startsWith('/admin')) {
          router.push('/admin/login')
        } else {
          router.push('/login')
        }
      }
    },
    
    /**
     * 重置状态
     */
    resetState() {
      this.token = ''
      this.userInfo = {} as UserInfo
      this.roles = []
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('roles')
    },
    
    /**
     * 设置token
     */
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    /**
     * 设置用户信息
     */
    setUserInfo(userInfo: UserInfo) {
      this.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    
    /**
     * 设置角色
     */
    setRoles(roles: string[]) {
      this.roles = roles
      localStorage.setItem('roles', JSON.stringify(roles))
    },
    
    /**
     * 更新用户信息
     */
    async updateUserInfo(userData: Partial<UserInfo>) {
      try {
        this.loading = true
        this.error = null
        
        const isAdmin = this.roles.includes('admin')
        const endpoint = isAdmin ? `/users/admin/${this.userInfo.id}` : '/users/me'
        
        const data = await request.put(endpoint, userData)
        this.setUserInfo({ ...this.userInfo, ...data })
        
        ElMessage.success('用户信息更新成功')
        return data
      } catch (error: any) {
        this.error = error.message || '更新用户信息失败'
        ElMessage.error(this.error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 检查是否有权限
     */
    hasPermission(requiredRole: string): boolean {
      if (!this.token) return false
      if (requiredRole === 'admin') return this.roles.includes('admin')
      return true
    }
  }
}) 