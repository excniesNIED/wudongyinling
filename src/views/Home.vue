<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="container">
        <h1 class="hero-title">舞动青春，乐享银龄</h1>
        <p class="hero-subtitle">专为老年人设计的智能舞蹈学习平台，让舞蹈变得简单、健康、有趣！</p>
        <div class="d-flex justify-content-center gap-3">
          <el-button type="primary" size="large" @click="navigateTo('/coach')">开始学习</el-button>
          <el-button plain size="large" @click="scrollToFeatures">了解更多</el-button>
        </div>
      </div>
    </section>
<br />
    <!-- 特色功能 -->
    <section id="features" class="py-5">
      <div class="container">
        <h2 class="section-title">我们的特色服务</h2>
        <div class="features-grid">
          <div class="feature-card" @click="navigateTo('/coach')">
            <div class="feature-icon">👨‍🏫</div>
            <h3 class="feature-title">AI 教练</h3>
            <p class="feature-desc">智能舞蹈教学与动作纠正，让您在家也能享受专业指导</p>
          </div>
          <div class="feature-card" @click="navigateTo('/health')">
            <div class="feature-icon">❤️</div>
            <h3 class="feature-title">健康管理</h3>
            <p class="feature-desc">根据您的身体状况，为您定制专属运动方案，实时监测健康数据</p>
          </div>
          <div class="feature-card" @click="navigateTo('/social')">
            <div class="feature-icon">🎉</div>
            <h3 class="feature-title">社交激励</h3>
            <p class="feature-desc">结交志同道合的朋友，共同参与舞蹈挑战，传承非遗文化</p>
          </div>
        </div>
      </div>
    </section>
<br/>
    <!-- 热门课程 -->
    <section class="py-5 bg-light">
      <div class="container">
        <h2 class="section-title">热门舞蹈课程</h2>
        <p class="section-subtitle">选择您感兴趣的舞蹈开始学习</p>

        <div class="row">
          <div class="col-md-3" v-for="course in courses" :key="course.id">
            <div class="course-card">
              <img :src="course.cover_url" :alt="course.title" class="course-img">
              <div class="p-3">
                <h4 class="course-title">{{ course.title }}</h4>
                <p class="course-duration"><i class="far fa-clock"></i> {{ course.duration }} · {{ course.difficulty }}</p>
                <el-button type="primary" class="w-100" @click="navigateTo('/dance-courses')">开始学习</el-button>
              </div>
            </div>
          </div>
        </div>

        <div class="text-center mt-4">
          <el-button type="primary" size="large" @click="navigateTo('/dance-courses')">浏览更多课程</el-button>
        </div>
      </div>
    </section>

    <!-- 用户评价 -->
    <section class="py-5">
      <div class="container">
        <h2 class="section-title">用户评价</h2>
        <p class="section-subtitle">听听大家怎么说</p>

        <div class="row">
          <div class="col-md-4" v-for="review in reviews" :key="review.id">
            <div class="feature-card">
              <div class="d-flex align-items-center mb-3">
                <img :src="review.avatar" :alt="review.name" class="rounded-circle me-3" width="60">
                <div>
                  <h5 class="mb-0">{{ review.name }}</h5>
                  <div class="text-warning">
                    <i class="fas fa-star" v-for="n in review.stars" :key="n"></i>
                    <i class="fas fa-star-half-alt" v-if="review.halfStar"></i>
                  </div>
                </div>
              </div>
              <p>{{ review.content }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const router = useRouter()

// 课程数据
const courses = ref([])

const fetchCourses = async () => {
  try {
    courses.value = await request.get('/courses', { params: { skip: 0, limit: 4 } })
  } catch (error) {
    ElMessage.error('获取热门课程失败')
  }
}

onMounted(() => {
  fetchCourses()
})

// 用户评价数据
const reviews = ref([
  {
    id: 1,
    name: '张玉梅',
    avatar: '/images/zym.png',
    stars: 5,
    halfStar: false,
    content: '"这个平台的AI教练太神奇了，能指出我跳舞时的小毛病，现在我跳得越来越好了！"'
  },
  {
    id: 2,
    name: '王德福',
    avatar: '/images/wdf.png',
    stars: 5,
    halfStar: false,
    content: '"健康管理功能很实用，能监测我的血压和心率，跳舞时更安心了。"'
  },
  {
    id: 3,
    name: '陈淑芬',
    avatar: '/images/csf.png',
    stars: 4,
    halfStar: true,
    content: '"在社交平台认识了很多舞友，大家一起打卡互相鼓励，跳舞更有动力了！"'
  }
])

// 导航方法
const navigateTo = (path) => {
  router.push(path)
}

// 滚动到特色部分
const scrollToFeatures = () => {
  document.getElementById('features').scrollIntoView({ 
    behavior: 'smooth' 
  })
}
</script>

<style scoped>
.hero-section {
  position: relative;
  width: 100%;
  padding-top: 100%; /* 1:1 Aspect Ratio */
  background: #8e99f3 url('/background.png') center/cover no-repeat;
  aspect-ratio: 1/1; /* 现代浏览器支持 */
  z-index: 1;
}

/* 添加遮罩层 */
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2); /* 40%的黑色遮罩 */
  z-index: 1;
}

.hero-section .container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 1200px;
  padding: 0 20px;
  color: white;
  text-align: center;
  z-index: 2; /* 确保文字在遮罩层之上 */
}

.hero-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3); /* 减小文字阴影，因为已经有遮罩 */
  letter-spacing: 0.05em;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 30px;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.2); /* 减小文字阴影，因为已经有遮罩 */
  line-height: 1.4;
}

.btn-primary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  font-size: 18px;
  padding: 10px 25px;
}

.btn-primary:hover {
  background-color: #e05a2b;
  border-color: #e05a2b;
}

.btn-outline-light {
  color: white;
  border-color: white;
  font-size: 18px;
  padding: 10px 25px;
}

.btn-outline-primary {
  color: var(--primary-color);
  border-color: var(--primary-color);
  font-size: 18px;
  padding: 10px 25px;
}

.btn-outline-primary:hover {
  background-color: var(--primary-color);
  color: white;
}

.section-title {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 30px;
  text-align: center;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #666;
  text-align: center;
  margin-bottom: 40px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.feature-card {
  background-color: var(--white);
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

.feature-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.feature-title {
  font-size: 24px;
  margin-bottom: 15px;
  color: var(--primary-color);
}

.feature-desc {
  font-size: 18px;
  color: #666;
}

.bg-light {
  background-color: #f8f9fa;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
}

.col-md-3, .col-md-4 {
  position: relative;
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
}

.col-md-3 {
  flex: 0 0 25%;
  max-width: 25%;
}

.col-md-4 {
  flex: 0 0 33.333333%;
  max-width: 33.333333%;
}

.course-card {
  border-radius: 15px;
  overflow: hidden;
  box-shadow: var(--shadow);
  margin-bottom: 25px;
  transition: transform 0.3s;
  background-color: var(--white);
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

.course-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.course-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 10px 0;
}

.course-duration {
  color: #777;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.gap-3 {
  gap: 1rem;
}

.d-flex {
  display: flex;
}

.justify-content-center {
  justify-content: center;
}

.align-items-center {
  align-items: center;
}

.mb-3 {
  margin-bottom: 1rem;
}

.mb-0 {
  margin-bottom: 0;
}

.me-3 {
  margin-right: 1rem;
}

.mt-4 {
  margin-top: 1.5rem;
}

.p-3 {
  padding: 1rem;
}

.w-100 {
  width: 100%;
}

.text-center {
  text-align: center;
}

.text-warning {
  color: #ffc107;
}

.rounded-circle {
  border-radius: 50%;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
  }

  .hero-subtitle {
    font-size: 1.2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  }

  .section-title {
    font-size: 1.8rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .col-md-3, .col-md-4 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

:deep(.el-button--primary) {
  background-color: #daa01b;
  border-color: #daa01b;
  font-size: 18px;
  padding: 10px 25px;
  height: auto;
  line-height: 1.5;
}

:deep(.el-button--primary:hover) {
  background-color: #ff8a65;
  border-color: #ff8a65;
}

:deep(.el-button--primary.is-plain) {
  color: #daa01b;
  background-color: transparent;
  border-color: #daa01b;
}

:deep(.el-button--primary.is-plain:hover) {
  background-color: #daa01b;
  color: white;
  border-color: #daa01b;
}

:deep(.el-button.is-plain) {
  color: white;
  background-color: transparent;
  border-color: white;
  font-size: 18px;
  padding: 10px 25px;
  height: auto;
  line-height: 1.5;
}

:deep(.el-button.is-plain:hover) {
  background-color: rgba(255, 255, 255, 0.2);
}

/* 删除这些不再需要的样式 */
.btn-primary,
.btn-primary:hover,
.btn-outline-light,
.btn-outline-primary,
.btn-outline-primary:hover {
  display: none;
}
</style> 