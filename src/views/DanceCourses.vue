<template>
  <div class="dance-courses">
    <h1 class="page-title">舞蹈课程</h1>
    <p class="section-subtitle">探索多样化舞蹈课程，享受舞动乐趣</p>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input 
        v-model="searchQuery" 
        placeholder="搜索舞蹈课程..." 
        class="search-input"
        :prefix-icon="Search"
      >
        <template #append>
          <el-button @click="handleSearch">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 分类筛选 -->
    <div class="course-tabs">
      <div class="tabs-container">
        <div 
          v-for="(category, index) in categories" 
          :key="index"
          :class="['tab-button', activeCategory === category.value ? 'active' : '']"
          @click="activeCategory = category.value"
        >
          {{ category.label }}
        </div>
      </div>
    </div>

    <!-- 课程列表 -->
    <div class="courses-container" v-show="!showVideoPlayer">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="course in filteredCourses" :key="course.id">
          <el-card class="course-card" shadow="hover" @click="showCourseDetails(course)">
            <el-image :src="course.cover_url" fit="cover" class="course-thumbnail" />
            <div class="course-info">
              <h3 class="course-title">{{ course.title }}</h3>
              <div class="course-meta">
                <span>
                  {{ course.rating }} <el-icon><Star /></el-icon>
                </span>
                <span>{{ course.duration }} 分钟</span>
              </div>
              <el-tag 
                :type="getDifficultyType(course.difficulty)" 
                size="small" 
                class="difficulty-tag"
              >
                {{ course.difficulty }}
              </el-tag>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 视频播放区域 -->
    <div v-show="showVideoPlayer" class="video-player-section">
      <el-card>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="24" :md="16">
            <div class="video-player">
              <el-image v-if="currentCourse" :src="currentCourse.video_url" fit="cover" class="player-image" />
            </div>
          </el-col>
          <el-col :xs="24" :sm="24" :md="8">
            <div class="video-details">
              <h2>{{ currentCourse?.title }}</h2>
              <p>难度：<el-tag :type="getDifficultyType(currentCourse?.difficulty)">{{ currentCourse?.difficulty }}</el-tag></p>
              <p>时长：{{ currentCourse?.duration }}</p>
              <el-divider />
              <p>{{ currentCourse?.description }}</p>
              
              <div class="video-actions">
                <el-button :icon="Star" text>收藏</el-button>
                <el-button :icon="Share" text>分享</el-button>
                <el-button :icon="Back" text @click="goBackToList">返回列表</el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>

    <!-- 聊天助手按钮 -->
    <div class="ai-assistant-btn" @click="openAIChat">
      <el-icon><Microphone /></el-icon>
    </div>

    <!-- AI 对话界面 -->
    <el-dialog
      v-model="showAIChat"
      title="舞蹈智能评价助手"
      width="500px"
      custom-class="ai-chat-dialog"
    >
      <div class="chat-messages">
        <div class="message ai-message">
          您好！我是您的AI舞蹈助手，请上传您的舞蹈视频，我可以帮您分析舞蹈动作并提供改进建议。
        </div>
        <div class="message user-message">
          <el-image src="/images/deepseek.png" class="message-video" />
          <br>我这段舞蹈练习效果怎么样?
        </div>
        <div class="message ai-message">
          <p><strong>1.节奏与协调性</strong><br>
          问题:易出现抢拍或慢拍，手脚动作不同步。<br>
          建议:用手机节拍器辅助练习，先分解动作跟节奏，熟练后再连贯。</p>
          
          <p><strong>2.动作幅度与重心</strong><br>
          问题:因担心摔倒而动作拘谨，重心偏移不稳。<br>
          建议:穿防滑鞋，手扶椅子练习伸展动作，逐步增加幅度。</p>
          
          <p><strong>3.体态与呼吸</strong><br>
          问题:含胸驼背或憋气跳舞。<br>
          建议:保持挺胸收腹，每4拍深呼吸一次，可对镜练习。</p>
          
          <p><strong>4.表情管理</strong><br>
          问题:过于紧张导致表情僵硬。<br>
          建议:想象舞蹈场景(如草原、节日)，自然流露情绪。</p>
        </div>
      </div>
      <div class="chat-input">
        <el-input v-model="chatMessage" placeholder="输入消息..." @keyup.enter="sendChatMessage">
          <template #append>
            <el-button type="primary" @click="sendChatMessage">发送</el-button>
          </template>
        </el-input>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Star, Share, Back, Microphone } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

// 搜索和分类状态
const searchQuery = ref('')
const activeCategory = ref('all')

// 视频播放状态
const showVideoPlayer = ref(false)
const currentCourse = ref(null)

// 聊天界面状态
const showAIChat = ref(false)
const chatMessage = ref('')

// 课程数据
const courses = ref([])

const fetchCourses = async () => {
  try {
    courses.value = await request.get('/api/v1/courses', { params: { skip: 0, limit: 100 } })
  } catch (error) {
    ElMessage.error('获取课程列表失败')
  }
}

onMounted(() => {
  fetchCourses()
})

// 分类数据
const categories = [
  { value: 'all', label: '全部课程' },
  { value: 'square', label: '广场舞' },
  { value: 'taichi', label: '太极' },
  { value: 'folk', label: '民族舞' },
  { value: 'social', label: '交谊舞' },
  { value: 'fitness', label: '健身操' }
]

// 根据搜索和分类过滤课程
const filteredCourses = computed(() => {
  let result = courses.value

  // 按分类筛选
  if (activeCategory.value !== 'all') {
    result = result.filter(course => course.category === activeCategory.value)
  }

  // 按搜索关键词筛选
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(course => 
      course.title.toLowerCase().includes(query) || 
      course.description.toLowerCase().includes(query)
    )
  }

  return result
})

// 获取难度标签的样式类型 (根据英文难度值)
const getDifficultyType = (difficulty) => {
  if (!difficulty) return '';
  // difficulty values: beginner, intermediate, advanced
  switch (difficulty) {
    case 'beginner':
      return 'success';
    case 'intermediate':
      return 'warning';
    case 'advanced':
      return 'danger';
    default:
      return 'info';
  }
}

// 显示课程详情和视频
const showCourseDetails = (course) => {
  currentCourse.value = course
  showVideoPlayer.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 返回课程列表
const goBackToList = () => {
  showVideoPlayer.value = false
}

// 搜索处理
const handleSearch = () => {
  ElMessage.success('搜索: ' + searchQuery.value)
}

// 打开AI聊天助手
const openAIChat = () => {
  showAIChat.value = true
}

// 发送聊天消息
const sendChatMessage = () => {
  if (!chatMessage.value.trim()) return
  
  // 这里只是模拟聊天，实际应用需要连接后端API
  ElMessage.success('消息已发送')
  chatMessage.value = ''
}
</script>

<style scoped>
.dance-courses {
  padding: 20px;
  position: relative;
}

.page-title {
  font-size: 32px;
  text-align: center;
  margin: 40px 0;
  color: var(--primary-color);
}

.section-subtitle {
  text-align: center;
  margin-bottom: 30px;
  color: #666;
}

.search-bar {
  max-width: 600px;
  margin: 0 auto 30px;
}

.course-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.tabs-container {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.tab-button {
  padding: 12px 24px;
  background-color: #fff;
  color: var(--text-color);
  border: none;
  border-radius: 50px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.tab-button:hover {
  background-color: #f5f5f5;
  transform: translateY(-2px);
}

.tab-button.active {
  background-color: var(--primary-color);
  color: white;
}

.course-card {
  margin-bottom: 30px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.course-thumbnail {
  width: 100%;
  height: 180px;
  border-radius: 8px 8px 0 0;
}

.course-info {
  padding: 15px 0 5px;
}

.course-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  color: #777;
  margin-bottom: 8px;
}

.difficulty-tag {
  margin-top: 5px;
}

.video-player-section {
  margin: 30px 0;
}

.video-player {
  width: 100%;
  aspect-ratio: 16/9;
  background-color: #000;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.player-image {
  width: 100%;
  height: 100%;
}

.video-details {
  padding: 10px;
}

.video-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.ai-assistant-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 100;
}

.ai-assistant-btn:hover {
  transform: scale(1.1);
}

.chat-messages {
  max-height: 350px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.message {
  max-width: 80%;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 15px;
}

.ai-message {
  background-color: #f4f4f5;
  align-self: flex-start;
  margin-right: auto;
}

.user-message {
  background-color: #ecf5ff;
  align-self: flex-end;
  margin-left: auto;
  text-align: right;
}

.message-video {
  max-width: 100%;
  border-radius: 8px;
  margin-bottom: 10px;
}

.ai-chat-dialog :deep(.el-dialog__body) {
  padding-top: 0;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 28px;
  }
  
  .course-tabs {
    overflow-x: auto;
    padding-bottom: 10px;
  }
  
  .course-thumbnail {
    height: 150px;
  }
  
  .ai-assistant-btn {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .video-player {
    margin-bottom: 20px;
  }
  
  .video-details {
    padding: 0 15px;
  }
}

@media (max-width: 576px) {
  .search-bar {
    max-width: 100%;
  }
  
  .course-tabs {
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 15px;
  }
  
  .tabs-container {
    display: inline-flex;
    padding: 5px 0;
    min-width: 100%;
    justify-content: flex-start;
  }
  
  .tab-button {
    flex: 0 0 auto;
  }
}
</style> 