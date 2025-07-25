<script setup lang="ts">
import { ref } from 'vue'
import { StarFilled, ChatDotRound, Share, Promotion, Sunrise, Star, Trophy, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PageHeader from '@/components/common/PageHeader.vue'

// 当前激活的标签页
const activeTab = ref('feed')

// 标签选项
interface TabOption {
  name: string
  label: string
}

const tabOptions: TabOption[] = [
  { name: 'feed', label: '动态广场' },
  { name: 'challenge', label: '打卡挑战' },
  { name: 'heritage', label: '非遗传承' },
  { name: 'message', label: '私信聊天' }
]

// 动态广场数据
interface Post {
  id: number
  username: string
  avatar: string
  time: string
  location: string
  content: string
  image: string
  likes: number
  comments: number
}

const posts = ref<Post[]>([
  {
    id: 1,
    username: '张玉梅',
    avatar: '/images/zym.png',
    time: '1小时前',
    location: '济南',
    content: '今天学习了新的广场舞动作，虽然还不熟练，但很开心！坚持打卡第15天~',
    image: '/images/zym-2.png',
    likes: 24,
    comments: 8
  },
  {
    id: 2,
    username: '陈淑芬',
    avatar: '/images/csf.png',
    time: '2小时前',
    location: '青岛',
    content: '参加了社区的民族舞表演，虽然紧张但顺利完成，感谢平台的教学视频！',
    image: '/images/csf-2.png',
    likes: 36,
    comments: 12
  }
])

// 打卡挑战数据
interface Challenge {
  id: number
  title: string
  description: string
  participants: number
  timeLeft: string
  progress: number
  progressStatus?: string
  myProgress: string
  streakIcon: {
    name: string
    class: string
  }
  streakText: string
  status: {
    type: string
    text: string
  }
  actionText: string
}

const challenges = ref<Challenge[]>([
  {
    id: 1,
    title: '21天健身舞打卡',
    description: '连续21天每天练习健身舞15分钟，养成运动好习惯',
    participants: 1245,
    timeLeft: '剩余: 12天',
    progress: 45,
    myProgress: '9/21天',
    streakIcon: { name: 'Sunrise', class: 'text-danger' },
    streakText: '连续7天',
    status: { type: 'primary', text: '进行中' },
    actionText: '今日打卡'
  },
  {
    id: 2,
    title: '民族舞学习月',
    description: '学习4种民族舞基础动作，感受传统文化魅力',
    participants: 892,
    timeLeft: '剩余: 30天',
    progress: 20,
    myProgress: '1/4种',
    streakIcon: { name: 'Star', class: 'text-warning' },
    streakText: '新加入',
    status: { type: 'success', text: '新挑战' },
    actionText: '立即参加'
  },
  {
    id: 3,
    title: '7天广场舞入门',
    description: '7天掌握广场舞基本步伐，适合零基础学员',
    participants: 2156,
    timeLeft: '状态: 已完成',
    progress: 100,
    myProgress: '成绩: 优秀',
    streakIcon: { name: 'Trophy', class: 'text-warning' },
    streakText: '已获奖章',
    status: { type: 'info', text: '已完成' },
    actionText: '查看证书'
  },
  {
    id: 4,
    title: '交谊舞双周计划',
    description: '14天学会基础交谊舞，可与舞伴一起参加',
    participants: 563,
    timeLeft: '开始: 3天后',
    progress: 0,
    myProgress: '未开始',
    streakIcon: { name: 'Clock', class: 'text-info' },
    streakText: '即将开始',
    status: { type: 'warning', text: '即将开始' },
    actionText: '预约参加'
  }
])

// 非遗传承数据
interface HeritageDance {
  id: number
  title: string
  description: string
  image: string
}

const heritageDances = ref<HeritageDance[]>([
  {
    id: 1,
    title: '蒙古族安代舞',
    description: '国家级非物质文化遗产',
    image: '/images/安代舞图片.png'
  },
  {
    id: 2,
    title: '藏族锅庄舞',
    description: '国家级非物质文化遗产',
    image: '/images/藏族锅庄舞图片.png'
  },
  {
    id: 3,
    title: '傣族孔雀舞',
    description: '国家级非物质文化遗产',
    image: '/images/傣族孔雀舞图片.png'
  }
])

interface HeritageTeacher {
  id: number
  name: string
  title: string
  avatar: string
  description: string
}

const heritageTeachers = ref<HeritageTeacher[]>([
  {
    id: 1,
    name: '非遗传承人 - 张老师',
    title: '蒙古族安代舞传承人',
    avatar: '/images/非遗传承人1.png',
    description: '安代舞是蒙古族传统舞蹈，希望通过这个平台让更多老年人了解和传承这一文化遗产。'
  },
  {
    id: 2,
    name: '非遗传承人 - 李老师',
    title: '傣族孔雀舞传承人',
    avatar: '/images/非遗传承人2.png',
    description: '孔雀舞动作优美，适合老年人练习，既能锻炼身体又能感受傣族文化魅力。'
  }
])

// 聊天数据
interface Message {
  id: number
  content: string
  time: string
  isSender: boolean
}

interface Chat {
  id: string
  name: string
  avatar: string
  lastTime: string
  messages: Message[]
}

const chatList = ref<Chat[]>([
  {
    id: '1',
    name: '王德福',
    avatar: '/images/wdf.png',
    lastTime: '今天 15:28',
    messages: [
      {
        id: 1,
        content: '玉梅，您刚才的舞蹈视频我看了，跳得真好！',
        time: '今天 15:23',
        isSender: false
      },
      {
        id: 2,
        content: '谢谢夸奖！我跟着平台的课程练习了一个月了',
        time: '今天 15:25',
        isSender: true
      },
      {
        id: 3,
        content: '我也想学，能推荐一下适合初学者的课程吗？',
        time: '今天 15:26',
        isSender: false
      },
      {
        id: 4,
        content: '可以从"广场舞基础入门"开始，我当初就是学这个',
        time: '今天 15:28',
        isSender: true
      }
    ]
  },
  {
    id: '2',
    name: '舞蹈学习小组',
    avatar: '/images/hldg-group.png',
    lastTime: '昨天 10:45',
    messages: [
      {
        id: 1,
        content: '各位舞友们，明天下午3点社区有广场舞展示活动，有兴趣的可以来参加！',
        time: '昨天 10:45',
        isSender: false
      }
    ]
  },
  {
    id: '3',
    name: '陈淑芬',
    avatar: '/images/csf.png',
    lastTime: '3月12日',
    messages: [
      {
        id: 1,
        content: '玉梅姐，我看到你在平台上分享的舞蹈视频了，动作很标准！',
        time: '3月12日 09:30',
        isSender: false
      },
      {
        id: 2,
        content: '谢谢！多练习就会进步的，你也很棒！',
        time: '3月12日 10:15',
        isSender: true
      }
    ]
  }
])

const activeChat = ref('1')
const currentChat = ref(chatList.value[0])
const newMessage = ref('')

// 方法
const handleLike = (post: Post): void => {
  post.likes++
  ElMessage.success('点赞成功')
}

const handleComment = (post: Post): void => {
  ElMessage.info('评论功能开发中')
}

const handleShare = (post: Post): void => {
  ElMessage.info('分享功能开发中')
}

const selectChat = (chat: Chat): void => {
  currentChat.value = chat
  activeChat.value = chat.id
}

const sendMessage = (): void => {
  if (!newMessage.value.trim()) return
  
  currentChat.value.messages.push({
    id: Date.now(),
    content: newMessage.value,
    time: '刚刚',
    isSender: true
  })
  
  newMessage.value = ''
}
</script>

<template>
  <div class="social-platform">
    <PageHeader title="社交激励" subtitle="与舞友互动交流，共同进步" />
    
    <!-- 标签页 - 改用自定义样式取代el-tabs -->
    <div class="custom-tabs">
      <div class="tabs-container">
        <button 
          v-for="tab in tabOptions" 
          :key="tab.name"
          :class="['tab-button', { active: activeTab === tab.name }]"
          @click="activeTab = tab.name"
        >
          {{ tab.label }}
        </button>
      </div>
      
      <!-- 动态广场内容 -->
      <div v-show="activeTab === 'feed'" class="tab-content">
        <div class="social-cards">
          <ElCard v-for="post in posts" :key="post.id" class="social-card">
            <div class="d-flex">
              <ElAvatar :src="post.avatar" :size="50" class="me-3" />
              <div>
                <h5 class="mb-0">{{ post.username }}</h5>
                <p class="text-muted mb-0">{{ post.time }} · {{ post.location }}</p>
              </div>
            </div>
            <div class="post-content">
              <p>{{ post.content }}</p>
              <ElImage v-if="post.image" :src="post.image" class="post-image" fit="cover" />
            </div>
            <div class="post-actions">
              <ElButton text @click="handleLike(post)">
                <el-icon><StarFilled /></el-icon>
                点赞 ({{ post.likes }})
              </ElButton>
              <ElButton text @click="handleComment(post)">
                <el-icon><ChatDotRound /></el-icon>
                评论 ({{ post.comments }})
              </ElButton>
              <ElButton text @click="handleShare(post)">
                <el-icon><Share /></el-icon>
                分享
              </ElButton>
            </div>
          </ElCard>
          <div class="text-center mt-4">
            <ElButton type="primary" plain>加载更多</ElButton>
          </div>
        </div>
      </div>

      <!-- 打卡挑战内容 -->
      <div v-show="activeTab === 'challenge'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="12" :lg="12" v-for="challenge in challenges" :key="challenge.id">
            <ElCard class="challenge-card">
              <ElTag :type="challenge.status.type" class="challenge-badge">
                {{ challenge.status.text }}
              </ElTag>
              <h3>{{ challenge.title }}</h3>
              <p>{{ challenge.description }}</p>
              <div class="d-flex justify-content-between">
                <span>已参与: {{ challenge.participants }}人</span>
                <span>{{ challenge.timeLeft }}</span>
              </div>
              <ElProgress 
                :percentage="challenge.progress" 
                :status="challenge.progressStatus"
              />
              <div class="d-flex justify-content-between">
                <span>我的进度: {{ challenge.myProgress }}</span>
                <span>
                  <el-icon :class="challenge.streakIcon.class">
                    <component :is="challenge.streakIcon.name" />
                  </el-icon>
                  {{ challenge.streakText }}
                </span>
              </div>
              <ElButton type="primary" class="w-100 mt-3">
                {{ challenge.actionText }}
              </ElButton>
            </ElCard>
          </ElCol>
        </ElRow>
      </div>

      <!-- 非遗传承内容 -->
      <div v-show="activeTab === 'heritage'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="8" :lg="8" v-for="dance in heritageDances" :key="dance.id">
            <div class="heritage-card">
              <ElImage :src="dance.image" fit="cover" class="heritage-image" />
              <div class="heritage-overlay">
                <h4>{{ dance.title }}</h4>
                <p>{{ dance.description }}</p>
              </div>
            </div>
          </ElCol>
        </ElRow>

        <ElCard class="mt-4">
          <h3>非遗舞蹈学习社区</h3>
          <p>加入我们的非遗舞蹈学习小组，与传承人互动交流，学习传统舞蹈文化。</p>
          <ElRow :gutter="20" class="mt-4">
            <ElCol :xs="24" :sm="24" :md="12" v-for="teacher in heritageTeachers" :key="teacher.id">
              <div class="d-flex align-items-center mb-3">
                <ElAvatar :src="teacher.avatar" :size="60" class="me-3" />
                <div>
                  <h5 class="mb-0">{{ teacher.name }}</h5>
                  <p class="text-muted mb-0">{{ teacher.title }}</p>
                </div>
              </div>
              <p>{{ teacher.description }}</p>
              <ElButton type="primary">加入学习小组</ElButton>
            </ElCol>
          </ElRow>
        </ElCard>
      </div>

      <!-- 私信聊天内容 -->
      <div v-show="activeTab === 'message'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="24" :md="8">
            <ElCard>
              <template #header>
                <div class="card-header">
                  <span>我的消息</span>
                </div>
              </template>
              <ElMenu :default-active="activeChat">
                <ElMenuItem 
                  v-for="chat in chatList" 
                  :key="chat.id" 
                  :index="chat.id"
                  @click="selectChat(chat)"
                >
                  <div class="d-flex align-items-center">
                    <ElAvatar :src="chat.avatar" :size="50" class="me-3" />
                    <div>
                      <h6 class="mb-0">{{ chat.name }}</h6>
                      <small>{{ chat.lastTime }}</small>
                    </div>
                  </div>
                </ElMenuItem>
              </ElMenu>
            </ElCard>
          </ElCol>
          <ElCol :xs="24" :sm="24" :md="16">
            <ElCard v-if="currentChat">
              <template #header>
                <div class="d-flex align-items-center">
                  <ElAvatar :src="currentChat.avatar" :size="50" class="me-3" />
                  <div>
                    <h5 class="mb-0">与{{ currentChat.name }}的对话</h5>
                  </div>
                </div>
              </template>
              <div class="message-list">
                <div 
                  v-for="message in currentChat.messages" 
                  :key="message.id"
                  :class="['message-item', message.isSender ? 'message-sender' : 'message-receiver']"
                >
                  <p>{{ message.content }}</p>
                  <small>{{ message.time }}</small>
                </div>
              </div>
              <div class="mt-3">
                <ElInput
                  v-model="newMessage"
                  placeholder="输入消息..."
                  :suffix-icon="Promotion"
                  @keyup.enter="sendMessage"
                >
                  <template #append>
                    <ElButton @click="sendMessage">发送</ElButton>
                  </template>
                </ElInput>
              </div>
            </ElCard>
          </ElCol>
        </ElRow>
      </div>
    </div>
  </div>
</template>

<style scoped>
.social-platform {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 60px;
}

/* 自定义标签页样式，模仿HTML版本 */
.custom-tabs {
  margin-bottom: 40px;
}

.tabs-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.tab-button {
  padding: 12px 24px;
  background-color: #fff;
  color: var(--el-text-color-primary);
  border: none;
  border-radius: 50px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  min-width: 120px;
  text-align: center;
}

.tab-button.active {
  background-color: var(--el-color-primary);
  color: #fff;
}

.tab-content {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.social-card {
  margin-bottom: 20px;
}

.post-content {
  margin: 15px 0;
}

.post-image {
  width: 100%;
  max-height: 400px;
  border-radius: 10px;
  margin-bottom: 10px;
}

.post-actions {
  border-top: 1px solid var(--el-border-color-lighter);
  padding-top: 15px;
  display: flex;
  justify-content: flex-start;
  gap: 15px;
}

.challenge-card {
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}

.challenge-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  border-radius: 20px;
  padding: 5px 10px;
}

.heritage-card {
  position: relative;
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 20px;
  height: 250px;
}

.heritage-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.heritage-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  padding: 15px;
  color: white;
}

.message-list {
  max-height: 500px;
  overflow-y: auto;
  margin-bottom: 15px;
}

.message-item {
  padding: 10px 15px;
  border-radius: 10px;
  margin-bottom: 15px;
  max-width: 80%;
}

.message-sender {
  background-color: #e3f2fd;
  margin-left: auto;
}

.message-receiver {
  background-color: var(--el-fill-color-light);
  margin-right: auto;
}

/* 自定义工具类 */
.d-flex {
  display: flex;
}

.justify-content-between {
  justify-content: space-between;
}

.align-items-center {
  align-items: center;
}

.mb-0 {
  margin-bottom: 0 !important;
}

.mb-3 {
  margin-bottom: 1rem !important;
}

.me-3 {
  margin-right: 1rem !important;
}

.mt-3 {
  margin-top: 1rem !important;
}

.mt-4 {
  margin-top: 1.5rem !important;
}

.w-100 {
  width: 100% !important;
}

.text-center {
  text-align: center;
}

.text-muted {
  color: var(--el-text-color-secondary);
}

.text-danger {
  color: var(--el-color-danger);
}

.text-warning {
  color: var(--el-color-warning);
}

.text-info {
  color: var(--el-color-info);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 768px) {
  .post-image {
    max-height: 300px;
  }
  
  .heritage-card {
    height: 200px;
  }
  
  .tab-button {
    flex: 1;
    padding: 10px 15px;
    min-width: 100px;
  }
}

/* 调整聊天列表项的内边距和垂直对齐 */
.el-menu-item {
  padding-top: 0 !important; /* 移除内边距，让 flex 对齐控制 */
  padding-bottom: 0 !important;
  display: flex !important; /* 确保 el-menu-item 是 flex 容器 */
  align-items: center !important; /* 垂直居中其直接子元素 (.d-flex) */
}

/* 确保内部的 d-flex 容器也垂直居中 */
.el-menu-item .d-flex {
  width: 100%; /* 确保占据可用宽度 */
  align-items: center !important; /* 垂直居中头像和文本块 */
}

/* 移除包裹 h6 和 small 的 div 的额外间距 */
.el-menu-item .d-flex > div:last-child {
  padding: 0 !important;
  margin: 0 !important;
}

/* 移除聊天列表 h6 的所有间距和减小行高 */
.el-menu-item .d-flex > div:last-child h6 {
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.2; /* 减小行高 */
  display: block;
}

/* 移除聊天列表 small 的所有间距和减小行高 */
.el-menu-item .d-flex > div:last-child small {
  margin: 0 !important;
  padding: 0 !important;
  line-height: 1.2; /* 减小行高 */
  display: block;
}
</style>