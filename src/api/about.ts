import { request } from '../utils/request'

// 团队成员接口
export interface TeamMember {
  id: number
  name: string
  position: string
  avatar?: string
  bio?: string
  contact?: {
    email?: string
    phone?: string
    social?: {
      [platform: string]: string
    }
  }
}

// 合作伙伴接口
export interface Partner {
  id: number
  name: string
  logo: string
  website?: string
  description?: string
}

// 企业荣誉接口
export interface Award {
  id: number
  title: string
  description?: string
  image?: string
  date: string
}

// 发展历程接口
export interface Milestone {
  id: number
  year: number | string
  title: string
  description: string
  image?: string
}

// 关于我们页面信息接口
export interface AboutInfo {
  company: {
    name: string
    logo: string
    introduction: string
    vision: string
    mission: string
    values: string[]
  }
  team: TeamMember[]
  partners: Partner[]
  awards: Award[]
  milestones: Milestone[]
}

/**
 * 关于我们页面API
 */
export const aboutApi = {
  /**
   * 获取关于我们页面信息
   */
  getAboutInfo() {
    return request.get<AboutInfo>('/v1/about')
  },
  
  /**
   * 获取团队成员列表
   */
  getTeamMembers() {
    return request.get<TeamMember[]>('/v1/about/team')
  },
  
  /**
   * 获取合作伙伴列表
   */
  getPartners() {
    return request.get<Partner[]>('/v1/about/partners')
  },
  
  /**
   * 获取企业荣誉列表
   */
  getAwards() {
    return request.get<Award[]>('/v1/about/awards')
  },
  
  /**
   * 获取发展历程
   */
  getMilestones() {
    return request.get<Milestone[]>('/v1/about/milestones')
  },
  
  /**
   * 提交联系表单
   * @param data 表单数据
   */
  submitContactForm(data: {
    name: string
    email: string
    subject?: string
    message: string
  }) {
    return request.post('/v1/contact', data)
  }
} 