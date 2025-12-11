<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElTimeline, ElTimelineItem, ElCard, ElRow, ElCol, ElDivider, ElSkeleton } from 'element-plus'
import { Location, Phone, Message, Clock } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
// 修改导入方式
import { aboutApi, type TeamMember, type Milestone, type Partner } from '@/api/about'

// 加载状态
const loading = ref({
  team: true,
  milestones: true,
  partners: true
})

// 团队成员
const teamMembers = ref<TeamMember[]>([])
// 默认数据，用于加载失败时的备用数据
const defaultTeamMembers: TeamMember[] = [
  {
    id: '1',
    name: '张明',
    title: '创始人 & CEO',
    avatar: '/images/zym.png',
    description: '北京舞蹈学院毕业，拥有20年舞蹈教学经验，致力于推广适合老年人的舞蹈教育。'
  },
  {
    id: '2',
    name: '李芳',
    title: '首席健康顾问',
    avatar: '/images/lf.png',
    description: '资深康复医师，专注老年人运动康复与健康管理，中国老年医学会会员。'
  },
  {
    id: '3',
    name: '王科',
    title: '技术总监',
    avatar: '/images/wk.png',
    description: '人工智能与计算机视觉专家，负责平台舞蹈动作识别与纠正系统的研发。'
  },
  {
    id: '4',
    name: '刘婷',
    title: '舞蹈课程总监',
    avatar: '/images/lt.png',
    description: '国家一级舞蹈编导，专注民族舞蹈教学与研究，负责平台舞蹈课程设计。'
  }
]

// 合作伙伴
const partners = ref<Partner[]>([])
// 默认数据，用于加载失败时的备用数据
const defaultPartners: Partner[] = [
  { id: '1', name: '中国老年保健协会', logo: '/images/partners/partner1.png' },
  { id: '2', name: '北京舞蹈学院', logo: '/images/partners/partner2.png' },
  { id: '3', name: '国家非物质文化遗产保护中心', logo: '/images/partners/partner3.png' },
  { id: '4', name: '中国社区健康促进会', logo: '/images/partners/partner4.png' },
  { id: '5', name: '智能科技研究院', logo: '/images/partners/partner5.png' }
]

// 联系方式数据
const contactInfo = ref([
  {
    icon: 'Location',
    title: '地址',
    content: '北京市海淀区中关村南大街5号'
  },
  {
    icon: 'Phone',
    title: '电话',
    content: '400-123-4567'
  },
  {
    icon: 'Message',
    title: '邮箱',
    content: 'info@wudongylng.com'
  },
  {
    icon: 'Clock',
    title: '客服时间',
    content: '周一至周日 9:00-21:00'
  }
])

// 获取团队成员数据
const fetchTeamMembers = async () => {
  loading.value.team = true
  try {
    const { data } = await aboutApi.getTeamMembers()
    if (data && data.length) {
      teamMembers.value = data
    } else {
      teamMembers.value = defaultTeamMembers
    }
  } catch (error) {
    // 静默处理错误，使用本地默认数据
    teamMembers.value = defaultTeamMembers
  } finally {
    loading.value.team = false
  }
}

// 获取合作伙伴数据（可选，失败时使用本地数据）
const fetchPartners = async () => {
  loading.value.partners = true
  try {
    const { data } = await aboutApi.getPartners()
    if (data && data.length) {
      partners.value = data
    } else {
      partners.value = defaultPartners
    }
  } catch (error) {
    // 静默处理错误，使用本地默认数据
    partners.value = defaultPartners
  } finally {
    loading.value.partners = false
  }
}

// 页面加载时尝试获取API数据（演示账号会自动静默失败并使用本地数据）
onMounted(() => {
  fetchTeamMembers()
  fetchPartners()
})
</script>

<template>
  <div class="about-page page-with-nav">
    <h1 class="page-title">关于舞动银龄</h1>

    <!-- 公司介绍 -->
    <ElCard class="about-section">
      <h2>我们的故事</h2>
      <p>"舞动银龄"成立于2023年，是一个专为老年人设计的舞蹈教学和智能纠错平台。我们的初衷是帮助老年人通过舞蹈保持身心健康，享受舞蹈带来的快乐，同时促进老年人之间的社交互动。</p>
      <p>我们团队由舞蹈教育专家、健康医疗专业人士、人工智能工程师和老年服务管理人员组成。我们共同努力，将传统舞蹈教学与现代科技相结合，创造一个友好、安全且有效的舞蹈学习环境。</p>
      <p>经过多年发展，"舞动银龄"已经服务了超过3万名老年用户，开设了200多门针对不同健康状况和舞蹈水平的课程，成为中国领先的老年舞蹈教育平台。</p>
    </ElCard>

    <!-- 使命和愿景 -->
    <ElRow :gutter="20" class="mission-vision">
      <ElCol :span="12">
        <ElCard class="mission">
          <h2>我们的使命</h2>
          <p>通过结合科技与艺术，为老年人提供安全、有效且愉悦的舞蹈学习体验，促进身心健康，丰富晚年生活，搭建社交平台，传承非物质文化遗产。</p>
        </ElCard>
      </ElCol>
      <ElCol :span="12">
        <ElCard class="vision">
          <h2>我们的愿景</h2>
          <p>成为中国最具影响力的老年舞蹈教育平台，服务百万老年用户，让每一位银发族群都能享受到适合自己的舞蹈教学资源，实现积极健康的老龄化生活方式。</p>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 核心团队 -->
    <ElCard class="team-section" v-loading="loading.team">
      <h2>核心团队</h2>
      <ElRow :gutter="20">
        <ElCol :span="6" v-for="member in teamMembers" :key="member.id">
          <div class="team-member">
            <el-avatar :src="member.avatar" :size="150" class="member-photo" />
            <h3 class="member-name">{{ member.name }}</h3>
            <p class="member-title">{{ member.title }}</p>
            <p class="member-bio">{{ member.description }}</p>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>

    <!-- 合作伙伴 -->
    <ElCard class="partners-section" v-loading="loading.partners">
      <h2>合作伙伴</h2>
      <div class="partners-logos">
        <el-image
          v-for="partner in partners"
          :key="partner.id"
          :src="partner.logo"
          :alt="partner.name"
          class="partner-logo"
          fit="contain"
        />
      </div>
    </ElCard>

    <!-- 联系我们 -->
    <ElCard class="contact-section">
      <h2>联系我们</h2>
      <ElRow :gutter="30">
        <ElCol :span="6" v-for="contact in contactInfo" :key="contact.title">
          <div class="contact-item">
            <div class="contact-icon">
              <el-icon :size="24">
                <component :is="contact.icon" />
              </el-icon>
            </div>
            <div class="contact-text">
              <h3>{{ contact.title }}</h3>
              <p>{{ contact.content }}</p>
            </div>
          </div>
        </ElCol>
      </ElRow>
    </ElCard>
  </div>
</template>

<style scoped>
.about {
  padding: 20px;
}

.page-title {
  font-size: 32px;
  text-align: center;
  margin: 40px 0;
  color: var(--el-color-primary);
}

.about-section {
  margin-bottom: 40px;
}

.about-section h2 {
  font-size: 28px;
  color: var(--el-color-primary);
  margin-bottom: 20px;
}

.about-section p {
  margin-bottom: 20px;
  font-size: 18px;
  line-height: 1.6;
}

.mission-vision {
  margin: 40px 0;
}

.mission h2,
.vision h2 {
  font-size: 28px;
  color: var(--el-color-primary);
  margin-bottom: 20px;
  text-align: center;
}

.team-section {
  margin-bottom: 40px;
}

.team-section h2 {
  font-size: 28px;
  color: var(--el-color-primary);
  margin-bottom: 30px;
  text-align: center;
}

.team-member {
  text-align: center;
  margin-bottom: 30px;
}

.member-photo {
  margin-bottom: 15px;
  border: 5px solid var(--el-border-color-lighter);
}

.member-name {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 5px;
}

.member-title {
  font-size: 18px;
  color: var(--el-color-primary);
  margin-bottom: 10px;
}

.member-bio {
  font-size: 16px;
  color: #666;
}

.partners-section {
  margin-bottom: 40px;
}

.partners-section h2 {
  font-size: 28px;
  color: var(--el-color-primary);
  margin-bottom: 30px;
  text-align: center;
}

.partners-logos {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 40px;
}

.partner-logo {
  width: 150px;
  height: 100px;
  object-fit: contain;
}

.contact-section h2 {
  font-size: 28px;
  color: var(--el-color-primary);
  margin-bottom: 30px;
  text-align: center;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}

.contact-icon {
  width: 50px;
  height: 50px;
  background-color: var(--el-color-primary);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.contact-text h3 {
  font-size: 20px;
  margin-bottom: 5px;
}

.contact-text p {
  color: #666;
}

/* 平板响应式 */
@media (max-width: 992px) {
  .about-page {
    padding: 20px 15px 100px 15px; /* 底部导航安全区域 */
  }

  .mission-vision :deep(.el-col) {
    max-width: 100%;
    flex: 0 0 100%;
    margin-bottom: 20px;
  }

  .team-section :deep(.el-col) {
    max-width: 50%;
    flex: 0 0 50%;
    margin-bottom: 20px;
  }

  .contact-section :deep(.el-col) {
    max-width: 50%;
    flex: 0 0 50%;
    margin-bottom: 20px;
  }
}

/* 手机响应式 */
@media (max-width: 768px) {
  .about-page {
    padding: 15px 10px 100px 10px;
  }

  .page-title {
    font-size: 24px;
    margin: 30px 0 20px;
  }

  .about-section h2,
  .mission h2,
  .vision h2,
  .team-section h2,
  .partners-section h2,
  .contact-section h2 {
    font-size: 20px;
    margin-bottom: 15px;
  }

  .about-section p {
    font-size: 15px;
    margin-bottom: 15px;
  }

  .team-section :deep(.el-col) {
    max-width: 100%;
    flex: 0 0 100%;
    margin-bottom: 25px;
  }

  .member-photo {
    width: 120px !important;
    height: 120px !important;
  }

  .member-name {
    font-size: 18px;
  }

  .member-title {
    font-size: 15px;
  }

  .member-bio {
    font-size: 14px;
  }

  .partners-logos {
    gap: 20px;
  }

  .partner-logo {
    width: 100px;
    height: 70px;
  }

  .contact-section :deep(.el-col) {
    max-width: 100%;
    flex: 0 0 100%;
    margin-bottom: 15px;
  }

  .contact-item {
    justify-content: center;
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }

  .contact-icon {
    margin: 0 auto;
  }

  .contact-text {
    text-align: center;
  }

  .contact-text h3 {
    font-size: 16px;
  }

  .contact-text p {
    font-size: 14px;
  }
}

/* 小屏手机响应式 */
@media (max-width: 576px) {
  .about-page {
    padding: 10px 8px 100px 8px;
  }

  .page-title {
    font-size: 22px;
    margin: 25px 0 15px;
  }

  .about-section,
  .mission-vision,
  .team-section,
  .partners-section,
  .contact-section {
    margin-bottom: 25px;
  }

  .about-section h2,
  .mission h2,
  .vision h2,
  .team-section h2,
  .partners-section h2,
  .contact-section h2 {
    font-size: 18px;
  }

  .about-section p {
    font-size: 14px;
    line-height: 1.5;
  }

  .member-photo {
    width: 100px !important;
    height: 100px !important;
    border-width: 3px;
  }

  .member-name {
    font-size: 16px;
  }

  .member-title {
    font-size: 14px;
  }

  .member-bio {
    font-size: 13px;
    line-height: 1.4;
  }

  .partner-logo {
    width: 80px;
    height: 55px;
  }

  .partners-logos {
    gap: 15px;
  }

  .contact-icon {
    width: 40px;
    height: 40px;
  }

  .contact-icon .el-icon {
    font-size: 18px !important;
  }

  .contact-text h3 {
    font-size: 15px;
  }

  .contact-text p {
    font-size: 13px;
  }
}
</style> 