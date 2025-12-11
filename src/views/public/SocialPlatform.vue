<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  StarFilled, 
  ChatDotRound, 
  Share, 
  Promotion, 
  Sunrise, 
  Star, 
  Trophy, 
  Clock,
  Plus,
  MessageBox,
  Loading,
  Filter,
  Search,
  InfoFilled,
  Calendar,
  User,
  Picture,
  Camera,
  View,
  Minus
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageHeader from '@/components/common/PageHeader.vue'
import { postApi, type Post, type HeritageProject, type HeritageInheritor } from '@/api/social'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

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
const posts = ref<Post[]>([])
const postsLoading = ref(false)
const postsPagination = ref({
  page: 1,
  page_size: 10,
  total: 0
})

// 发布动态数据
const newPost = ref({
  content: '',
  post_type: 'text' as 'text' | 'image' | 'video' | 'dance' | 'heritage',
  media_url: '',
  is_public: true
})
const showCreatePost = ref(false)
const publishLoading = ref(false)
const showFilters = ref(false)

// 非遗传承数据
const heritageProjects = ref<HeritageProject[]>([])
const heritageInheritors = ref<HeritageInheritor[]>([])
const heritageLoading = ref(false)

// 挑战数据
const challenges = ref([
  {
    id: 1,
    title: '30天广场舞打卡挑战',
    description: '连续30天打卡广场舞练习',
    participants: 156,
    days: 30,
    currentDay: 15,
    status: 'ongoing'
  },
  {
    id: 2,
    title: '太极拳基础动作',
    description: '学习太极拳24式基础动作',
    participants: 89,
    days: 21,
    currentDay: 8,
    status: 'ongoing'
  }
])

// 过滤选项
const feedFilters = ref({
  post_type: '',
  user_role: '',
  is_featured: undefined as boolean | undefined
})

// 计算属性
const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    if (feedFilters.value.post_type && post.post_type !== feedFilters.value.post_type) {
      return false
    }
    if (feedFilters.value.is_featured !== undefined && post.is_featured !== feedFilters.value.is_featured) {
      return false
    }
    return true
  })
})

// 页面加载时尝试获取API数据（演示账号会自动静默失败并使用本地数据）
onMounted(() => {
  loadFeedData()
  loadHeritageData()
})

// 加载动态数据
const loadFeedData = async () => {
  postsLoading.value = true
  try {
    const response = await postApi.getPosts({
      page: postsPagination.value.page,
      page_size: postsPagination.value.page_size,
      ...feedFilters.value
    })
    
    if (response.code === 200) {
      posts.value = response.data.items || []
      postsPagination.value.total = response.data.total || 0
    }
  } catch (error) {
    // 静默处理错误（演示账号会自动使用本地数据）
    
    // 使用模拟数据
    posts.value = [
      {
        id: 1,
        user_id: 1,
        user: {
          id: 1,
          username: 'dancer_01',
          nickname: '舞蹈爱好者小李',
          avatar: '/images/default-avatar.png'
        },
        post_type: 'dance',
        content: '今天学习了傣族孔雀舞的基本动作，感觉非常优美！',
        media_url: '/images/傣族孔雀舞图片.png',
        likes_count: 25,
        comments_count: 8,
        shares_count: 3,
        is_public: true,
        is_featured: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 2,
        user_id: 2,
        user: {
          id: 2,
          username: 'elderly_teacher',
          nickname: '张老师',
          avatar: '/images/default-avatar.png'
        },
        post_type: 'heritage',
        content: '分享一段安代舞的历史背景，希望大家能了解这项美丽的非遗文化。',
        media_url: '/images/安代舞图片.png',
        likes_count: 42,
        comments_count: 15,
        shares_count: 7,
        is_public: true,
        is_featured: true,
        created_at: new Date(Date.now() - 3600000).toISOString(),
        updated_at: new Date(Date.now() - 3600000).toISOString()
      }
    ]
    postsPagination.value.total = 2
  } finally {
    postsLoading.value = false
  }
}

// 加载非遗数据
const loadHeritageData = async () => {
  heritageLoading.value = true
  try {
    const [projectsRes, inheritorsRes] = await Promise.all([
      postApi.getProjects({ page: 1, page_size: 6 }),
      postApi.getInheritors({ page: 1, page_size: 6 })
    ])
    
    heritageProjects.value = projectsRes.data || []
    heritageInheritors.value = inheritorsRes.data || []
  } catch (error) {
    // 静默处理错误（演示账号会自动使用本地数据）
    
    // 使用模拟数据
    heritageProjects.value = [
      {
        id: 1,
        name: '傣族孔雀舞',
        description: '傣族孔雀舞是傣族民间舞蹈的精华，是我国珍贵的民族艺术遗产之一。',
        origin_location: '云南西双版纳',
        category: 'dance',
        level: 'national',
        cover_image: '/images/傣族孔雀舞图片.png',
        video_url: '',
        history: '孔雀舞已有一千多年的历史，最初是模仿孔雀的各种优美姿态...',
        characteristics: '舞蹈动作轻盈、优美，手臂和手腕的变化丰富...',
        inheritor_id: 1,
        inheritor: {
          id: 1,
          name: '杨丽萍',
          gender: 'female',
          birth_year: 1958,
          hometown: '云南大理',
          specialty: '孔雀舞',
          is_active: true,
          created_at: '2024-01-01 00:00:00'
        },
        is_active: true,
        created_at: '2024-01-01 09:00:00'
      },
      {
        id: 2,
        name: '安代舞',
        description: '安代舞是蒙古族民间集体舞蹈，流传在内蒙古科尔沁草原等地区。',
        origin_location: '内蒙古通辽',
        category: 'dance',
        level: 'national',
        cover_image: '/images/安代舞图片.png',
        video_url: '',
        history: '安代舞起源于明末清初，最初是一种治病的萨满教舞蹈...',
        characteristics: '舞蹈节奏明快，动作简单易学，具有浓厚的生活气息...',
        inheritor_id: 2,
        inheritor: {
          id: 2,
          name: '包布和',
          gender: 'male',
          birth_year: 1960,
          hometown: '内蒙古通辽',
          specialty: '安代舞',
          is_active: true,
          created_at: '2024-01-01 00:00:00'
        },
        is_active: true,
        created_at: '2024-01-01 09:00:00'
      },
      {
        id: 3,
        name: '藏族锅庄舞',
        description: '锅庄舞是藏族的民间舞蹈，在节庆活动中表演，是藏族文化的重要组成部分。',
        origin_location: '西藏拉萨',
        category: 'dance',
        level: 'national',
        cover_image: '/images/藏族锅庄舞图片.png',
        video_url: '',
        history: '锅庄舞历史悠久，起源于古代藏族祭祀活动...',
        characteristics: '舞蹈队形变化丰富，男女分组对舞，动作优美大方...',
        inheritor_id: 3,
        inheritor: {
          id: 3,
          name: '次旺多吉',
          gender: 'male',
          birth_year: 1955,
          hometown: '西藏拉萨',
          specialty: '藏族锅庄舞',
          is_active: true,
          created_at: '2024-01-01 00:00:00'
        },
        is_active: true,
        created_at: '2024-01-01 09:00:00'
      }
    ]
    
    heritageInheritors.value = [
      {
        id: 1,
        name: '杨丽萍',
        gender: 'female',
        birth_year: 1958,
        hometown: '云南大理',
        specialty: '孔雀舞',
        avatar: '/images/非遗传承人1.png',
        bio: '著名舞蹈家，被誉为"孔雀公主"...',
        is_active: true,
        created_at: '2024-01-01 00:00:00'
      },
      {
        id: 2,
        name: '包布和',
        gender: 'male',
        birth_year: 1960,
        hometown: '内蒙古通辽',
        specialty: '安代舞',
        avatar: '/images/非遗传承人2.png',
        bio: '蒙古族安代舞传承人，从事安代舞教学30余年...',
        is_active: true,
        created_at: '2024-01-01 00:00:00'
      }
    ]
  } finally {
    heritageLoading.value = false
  }
}

// 发布动态
const publishPost = async () => {
  if (!newPost.value.content.trim()) {
    ElMessage.warning('请输入动态内容')
    return
  }

  try {
    publishLoading.value = true
    const response = await postApi.createPost({
      content: newPost.value.content.trim(),
      post_type: newPost.value.post_type,
      media_url: newPost.value.media_url || undefined,
      is_public: newPost.value.is_public
    })

    if (response.code === 200) {
      ElMessage.success('发布成功')
      showCreatePost.value = false
      newPost.value = {
        content: '',
        post_type: 'text',
        media_url: '',
        is_public: true
      }
      loadFeedData() // 重新加载动态列表
    } else {
      ElMessage.error(response.message || '发布失败')
    }
  } catch (error) {
    console.error('Failed to publish post:', error)
    ElMessage.error('发布失败')
  } finally {
    publishLoading.value = false
  }
}

// 点赞动态
const likePost = async (post: Post) => {
  try {
    const response = await postApi.likePost(post.id)
    if (response.code === 200) {
      // 更新本地数据
      const index = posts.value.findIndex(p => p.id === post.id)
      if (index !== -1) {
        posts.value[index].likes_count++
      }
    }
  } catch (error) {
    console.error('Failed to like post:', error)
    ElMessage.error('点赞失败')
  }
}

// 评论动态
const commentPost = async (post: Post) => {
  try {
    const { value: comment } = await ElMessageBox.prompt('请输入评论内容', '添加评论', {
      confirmButtonText: '发送',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputPlaceholder: '说点什么...'
    })

    if (comment && comment.trim()) {
      const response = await postApi.addComment(post.id, {
        content: comment.trim()
      })

      if (response.code === 200) {
        ElMessage.success('评论成功')
        // 更新本地数据
        const index = posts.value.findIndex(p => p.id === post.id)
        if (index !== -1) {
          posts.value[index].comments_count++
        }
      } else {
        ElMessage.error(response.message || '评论失败')
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to comment post:', error)
      ElMessage.error('评论失败')
    }
  }
}

// 分享动态
const sharePost = async (post: Post) => {
  try {
    // 创建分享链接
    const shareUrl = `${window.location.origin}/social/post/${post.id}`
    
    // 尝试使用 Web Share API
    if (navigator.share) {
      await navigator.share({
        title: '分享动态',
        text: post.content,
        url: shareUrl
      })
      ElMessage.success('分享成功')
    } else {
      // 如果不支持，则复制链接到剪贴板
      await navigator.clipboard.writeText(shareUrl)
      ElMessage.success('链接已复制到剪贴板')
    }
    
    // 更新分享计数（这里应该调用真实的API）
    const index = posts.value.findIndex(p => p.id === post.id)
    if (index !== -1) {
      posts.value[index].shares_count++
    }
  } catch (error) {
    console.error('Failed to share post:', error)
    ElMessage.error('分享失败')
  }
}

// 跳转到聊天页面
const goToChat = () => {
  router.push('/chat')
}

// 跳转到挑战详情
const goToChallengeDetail = (challengeId: number) => {
  router.push(`/challenge/${challengeId}`)
}

// 应用过滤器
const applyFilters = () => {
  postsPagination.value.page = 1
  loadFeedData()
}

// 重置过滤器
const resetFilters = () => {
  feedFilters.value = {
    post_type: '',
    user_role: '',
    is_featured: undefined
  }
  applyFilters()
}

// 格式化时间
const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 1) return '刚刚'
  if (diffMins < 60) return `${diffMins}分钟前`
  if (diffMins < 1440) return `${Math.floor(diffMins / 60)}小时前`
  
  return date.toLocaleDateString()
}

// 获取动态类型文本
const getPostTypeText = (type: string) => {
  switch (type) {
    case 'text':
      return '文字'
    case 'image':
      return '图片'
    case 'video':
      return '视频'
    case 'dance':
      return '舞蹈'
    case 'heritage':
      return '非遗'
    default:
      return '未知'
  }
}

// 获取动态类型颜色
const getPostTypeColor = (type: string) => {
  switch (type) {
    case 'text':
      return 'info'
    case 'image':
      return 'success'
    case 'video':
      return 'warning'
    case 'dance':
      return 'primary'
    case 'heritage':
      return 'danger'
    default:
      return 'info'
  }
}

// 默认头像
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

// 加入非遗计划
const joinHeritageProject = async (project: HeritageProject) => {
  if (!userStore.user?.id) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    await postApi.joinHeritageProject(project.id, userStore.user.id)
    ElMessage.success(`已加入${project.name}传承计划！群聊也已自动加入，快去和其他传承者交流吧！`)
    
    // 更新项目状态
    project.isJoined = true
    
    // 可以选择跳转到聊天室
    ElMessageBox.confirm('是否立即前往群聊与其他传承者交流？', '提示', {
      confirmButtonText: '前往群聊',
      cancelButtonText: '稍后再说',
      type: 'info'
    }).then(() => {
      // 跳转到聊天室
      router.push('/chat-room')
    }).catch(() => {
      // 用户选择稍后再说
    })
    
  } catch (error) {
    console.error('Failed to join heritage project:', error)
    ElMessage.error('加入计划失败，请稍后重试')
  }
}

// 退出非遗计划
const leaveHeritageProject = async (project: HeritageProject) => {
  if (!userStore.user?.id) {
    ElMessage.warning('请先登录')
    return
  }

  try {
    await ElMessageBox.confirm(`确定要退出${project.name}传承计划吗？退出后将无法访问相关群聊。`, '确认退出', {
      confirmButtonText: '确定退出',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await postApi.leaveHeritageProject(project.id, userStore.user.id)
    ElMessage.success('已退出传承计划')
    
    // 更新项目状态
    project.isJoined = false
    
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to leave heritage project:', error)
      ElMessage.error('退出计划失败，请稍后重试')
    }
  }
}

// 查看项目详情
const viewProjectDetail = (project: HeritageProject) => {
  ElMessage.info('项目详情页面开发中...')
  // TODO: 跳转到项目详情页
}
</script>

<template>
  <div class="social-platform page-with-nav">
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
      
      <!-- 动态广场筛选和操作栏 -->
      <div v-show="activeTab === 'feed'" class="tab-content">
        <div class="feed-toolbar gradient-warm shadow-warm">
          <div class="toolbar-left">
            <el-button type="primary" @click="showCreatePost = true" class="create-btn glow-effect">
              <el-icon><Plus /></el-icon>
              发布动态
            </el-button>
            <el-button @click="showFilters = true" class="filter-btn">
              <el-icon><Filter /></el-icon>
              筛选
            </el-button>
          </div>
          <div class="toolbar-right">
            <el-tag v-if="filteredPosts.length > 0" type="info" class="count-tag">
              共 {{ postsPagination.total }} 条动态
            </el-tag>
          </div>
        </div>

        <!-- 动态列表 -->
        <div class="posts-container">
          <div v-if="postsLoading" class="loading-container">
            <el-icon class="loading-icon" size="32">
              <Loading />
            </el-icon>
            <p>加载动态中...</p>
          </div>
          
          <div v-else-if="filteredPosts.length === 0" class="empty-container">
            <el-icon size="64" color="var(--primary-light)"><InfoFilled /></el-icon>
            <h3>暂无动态</h3>
            <p>成为第一个分享的人吧！</p>
            <el-button type="primary" @click="showCreatePost = true" class="glow-effect">
              发布第一条动态
            </el-button>
          </div>
          
          <div v-else class="posts-list">
            <div v-for="post in filteredPosts" :key="post.id" class="post-card fade-in">
              <div class="post-header">
                <el-avatar 
                  :src="(post.user?.avatar) || defaultAvatar" 
                  :size="48" 
                  class="user-avatar"
                />
                <div class="user-info">
                  <h4 class="username warm-gradient-text">
                    {{ post.user?.nickname || post.user?.username || '匿名用户' }}
                  </h4>
                  <div class="post-meta">
                    <span class="post-time">{{ formatTime(post.created_at) }}</span>
                    <el-tag :type="getPostTypeColor(post.post_type)" size="small" class="post-type-tag">
                      {{ getPostTypeText(post.post_type) }}
                    </el-tag>
                    <el-tag v-if="post.is_featured" type="warning" size="small">
                      <el-icon><Star /></el-icon>
                      精选
                    </el-tag>
                  </div>
                </div>
              </div>
              
              <div class="post-content">
                <p class="post-text">{{ post.content }}</p>
                <div v-if="post.media_url" class="post-media">
                  <el-image 
                    :src="post.media_url" 
                    fit="cover" 
                    class="media-image shadow-warm"
                    :preview-src-list="[post.media_url]"
                  />
                </div>
              </div>
              
              <div class="post-actions">
                                  <el-button text @click="likePost(post)" class="action-btn like-btn">
                    <el-icon><StarFilled /></el-icon>
                    <span>{{ post.likes_count || 0 }}</span>
                  </el-button>
                <el-button text @click="commentPost(post)" class="action-btn comment-btn">
                  <el-icon><ChatDotRound /></el-icon>
                  <span>{{ post.comments_count || 0 }}</span>
                </el-button>
                <el-button text @click="sharePost(post)" class="action-btn share-btn">
                  <el-icon><Share /></el-icon>
                  <span>{{ post.shares_count || 0 }}</span>
                </el-button>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="filteredPosts.length > 0" class="pagination-container">
            <el-pagination
              v-model:current-page="postsPagination.page"
              v-model:page-size="postsPagination.page_size"
              :total="postsPagination.total"
              :page-sizes="[10, 20, 50]"
              layout="total, sizes, prev, pager, next, jumper"
              @current-change="loadFeedData"
              @size-change="loadFeedData"
              class="custom-pagination"
            />
          </div>
        </div>
      </div>

      <!-- 打卡挑战内容 -->
      <div v-show="activeTab === 'challenge'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="12" :lg="12" v-for="challenge in challenges" :key="challenge.id">
            <ElCard class="challenge-card">
              <ElTag :type="challenge.status === 'ongoing' ? 'primary' : 'info'" class="challenge-badge">
                {{ challenge.status === 'ongoing' ? '进行中' : '已完成' }}
              </ElTag>
              <h3>{{ challenge.title }}</h3>
              <p>{{ challenge.description }}</p>
              <div class="d-flex justify-content-between">
                <span>已参与: {{ challenge.participants }}人</span>
                <span>已打卡: {{ challenge.currentDay }}/{{ challenge.days }}天</span>
              </div>
              <ElProgress 
                :percentage="challenge.currentDay / challenge.days * 100" 
                :status="challenge.currentDay / challenge.days * 100 === 100 ? 'success' : undefined"
              />
              <ElButton type="primary" class="w-100 mt-3" @click="goToChallengeDetail(challenge.id)">
                查看详情
              </ElButton>
            </ElCard>
          </ElCol>
        </ElRow>
      </div>

      <!-- 非遗传承内容 -->
      <div v-show="activeTab === 'heritage'" class="tab-content">
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="8" :lg="8" v-for="project in heritageProjects" :key="project.id">
            <div class="heritage-card">
              <ElImage :src="project.cover_image || project.image_url || '/images/default-heritage.png'" fit="cover" class="heritage-image" />
              <div class="heritage-overlay">
                <h4>{{ project.name || project.title }}</h4>
                <p>{{ project.description }}</p>
              </div>
              <div class="project-actions">
                <el-button type="primary" size="small" @click="viewProjectDetail(project)">
                  <el-icon><View /></el-icon>
                  查看详情
                </el-button>
                <el-button 
                  v-if="!project.isJoined" 
                  type="success" 
                  size="small" 
                  @click="joinHeritageProject(project)"
                >
                  <el-icon><Plus /></el-icon>
                  加入计划
                </el-button>
                <el-button 
                  v-else 
                  type="warning" 
                  size="small" 
                  @click="leaveHeritageProject(project)"
                >
                  <el-icon><Minus /></el-icon>
                  退出计划
                </el-button>
              </div>
            </div>
          </ElCol>
        </ElRow>

        <ElCard class="mt-4">
          <h3>非遗舞蹈学习社区</h3>
          <p>加入我们的非遗舞蹈学习小组，与传承人互动交流，学习传统舞蹈文化。</p>
          <ElRow :gutter="20" class="mt-4">
            <ElCol :xs="24" :sm="24" :md="12" v-for="inheritor in heritageInheritors" :key="inheritor.id">
              <div class="d-flex align-items-center mb-3">
                <ElAvatar :src="inheritor.avatar_url" :size="60" class="me-3" />
                <div>
                  <h5 class="mb-0">{{ inheritor.name }}</h5>
                  <p class="text-muted mb-0">{{ inheritor.title }}</p>
                </div>
              </div>
              <p>{{ inheritor.description }}</p>
              <ElButton type="primary">加入学习小组</ElButton>
            </ElCol>
          </ElRow>
        </ElCard>
      </div>

      <!-- 私信聊天 -->
      <div v-show="activeTab === 'message'" class="tab-content">
        <div class="text-center py-5">
          <el-icon size="64" color="#409eff"><ChatDotRound /></el-icon>
          <h3 class="mt-3">开始聊天</h3>
          <p class="text-muted mb-4">与舞友们实时交流，分享学习心得</p>
          <el-button type="primary" size="large" @click="goToChat">
            <el-icon><MessageBox /></el-icon>
            进入聊天室
          </el-button>
        </div>
      </div>
    </div>

    <!-- 发布动态对话框 -->
    <el-dialog
      v-model="showCreatePost"
      title="发布动态"
      width="500px"
      :before-close="() => showCreatePost = false"
    >
      <el-form :model="newPost" label-width="80px">
        <el-form-item label="动态类型">
          <el-select v-model="newPost.post_type" placeholder="选择类型">
            <el-option label="文字" value="text" />
            <el-option label="图片" value="image" />
            <el-option label="视频" value="video" />
            <el-option label="舞蹈" value="dance" />
            <el-option label="非遗" value="heritage" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="内容">
          <el-input
            v-model="newPost.content"
            type="textarea"
            :rows="4"
            placeholder="分享你的想法..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="媒体链接" v-if="newPost.post_type !== 'text'">
          <el-input
            v-model="newPost.media_url"
            placeholder="请输入图片或视频链接"
          />
        </el-form-item>
        
        <el-form-item label="可见性">
          <el-switch
            v-model="newPost.is_public"
            active-text="公开"
            inactive-text="私密"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreatePost = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="publishPost"
            :loading="publishLoading"
          >
            发布
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 筛选器对话框 -->
    <el-dialog
      v-model="showFilters"
      title="筛选动态"
      width="400px"
    >
      <el-form :model="feedFilters" label-width="80px">
        <el-form-item label="动态类型">
          <el-select v-model="feedFilters.post_type" placeholder="全部类型" clearable>
            <el-option label="文字" value="text" />
            <el-option label="图片" value="image" />
            <el-option label="视频" value="video" />
            <el-option label="舞蹈" value="dance" />
            <el-option label="非遗" value="heritage" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="用户角色">
          <el-select v-model="feedFilters.user_role" placeholder="全部角色" clearable>
            <el-option label="老人" value="ELDERLY" />
            <el-option label="儿童" value="CHILD" />
            <el-option label="志愿者" value="VOLUNTEER" />
            <el-option label="教师" value="TEACHER" />
            <el-option label="医生" value="DOCTOR" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="精选内容">
          <el-select v-model="feedFilters.is_featured" placeholder="全部内容" clearable>
            <el-option label="精选内容" :value="true" />
            <el-option label="普通内容" :value="false" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="resetFilters">重置</el-button>
          <el-button type="primary" @click="applyFilters(); showFilters = false">
            应用筛选
          </el-button>
        </span>
      </template>
    </el-dialog>
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

.project-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
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
  .social-platform {
    padding: 15px 10px;
    padding-bottom: 80px; /* 为底部导航添加安全区域 */
  }

  .tab-button {
    flex: 1;
    padding: 12px 15px;
    min-width: 100px;
    min-height: 44px;
    font-size: 16px;
  }

  .feed-toolbar {
    padding: 8px 15px;
    flex-direction: column;
    gap: 10px;
  }

  .toolbar-left {
    justify-content: center;
  }

  .toolbar-right {
    justify-content: center;
  }

  .create-btn, .filter-btn {
    height: 44px;
    font-size: 15px;
  }

  .post-card {
    margin-bottom: 15px;
    padding: 15px;
  }

  .post-header {
    margin-bottom: 12px;
  }

  .user-avatar {
    width: 40px;
    height: 40px;
  }

  .username {
    font-size: 15px;
  }

  .post-meta {
    gap: 8px;
    font-size: 12px;
  }

  .post-text {
    font-size: 15px;
    line-height: 1.5;
    margin-bottom: 10px;
  }

  .post-image {
    max-height: 250px;
  }

  .media-image {
    height: 180px;
  }

  .post-actions {
    padding-top: 10px;
    gap: 10px;
  }

  .action-btn {
    font-size: 13px;
    height: 36px;
  }

  .custom-pagination {
    margin-top: 15px;
  }

  .challenge-card {
    margin-bottom: 15px;
  }

  .challenge-card :deep(.el-card__body) {
    padding: 15px;
  }

  .heritage-card {
    height: 180px;
    margin-bottom: 15px;
  }

  .project-actions {
    top: 8px;
    right: 8px;
  }

  .project-actions .el-button {
    height: 32px;
    font-size: 12px;
  }

  .text-center .el-button {
    height: 44px;
    font-size: 15px;
  }
}

@media (max-width: 576px) {
  .social-platform {
    padding: 10px 5px;
    padding-bottom: 80px;
  }

  .tab-button {
    padding: 10px 12px;
    min-width: 80px;
    min-height: 40px;
    font-size: 14px;
  }

  .feed-toolbar {
    padding: 6px 10px;
  }

  .create-btn, .filter-btn {
    height: 40px;
    font-size: 14px;
  }

  .post-card {
    margin-bottom: 12px;
    padding: 12px;
  }

  .post-header {
    margin-bottom: 10px;
  }

  .user-avatar {
    width: 36px;
    height: 36px;
  }

  .username {
    font-size: 14px;
  }

  .post-meta {
    gap: 6px;
    font-size: 11px;
  }

  .post-text {
    font-size: 14px;
    margin-bottom: 8px;
  }

  .post-image {
    max-height: 200px;
  }

  .media-image {
    height: 150px;
  }

  .post-actions {
    padding-top: 8px;
    gap: 8px;
  }

  .action-btn {
    font-size: 12px;
    height: 32px;
  }

  .custom-pagination :deep(.el-pagination .el-pager li) {
    min-width: 32px;
    height: 32px;
    line-height: 32px;
    font-size: 12px;
  }

  .challenge-card :deep(.el-card__body) {
    padding: 12px;
  }

  .heritage-card {
    height: 160px;
    margin-bottom: 12px;
  }

  .project-actions {
    top: 6px;
    right: 6px;
  }

  .project-actions .el-button {
    height: 28px;
    font-size: 11px;
  }

  .text-center .el-button {
    height: 40px;
    font-size: 14px;
  }

  .tabs-container {
    margin-bottom: 30px;
    gap: 6px;
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

/* 新增样式 */
.gradient-warm {
  background: linear-gradient(to right, #ffd700, #ffa500);
  color: white;
  padding: 10px 20px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 10px rgba(255, 135, 0, 0.3);
}

.shadow-warm {
  box-shadow: 0 4px 10px rgba(255, 135, 0, 0.3);
}

.toolbar-left {
  display: flex;
  gap: 10px;
}

.create-btn {
  background-color: #fff;
  color: var(--el-color-primary);
  border: 1px solid var(--el-color-primary);
  border-radius: 25px;
  padding: 8px 15px;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.create-btn:hover {
  background-color: var(--el-color-primary);
  color: #fff;
  border-color: var(--el-color-primary);
}

.filter-btn {
  background-color: #fff;
  color: var(--el-text-color-primary);
  border: 1px solid var(--el-border-color-light);
  border-radius: 25px;
  padding: 8px 15px;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.filter-btn:hover {
  background-color: var(--el-color-primary);
  color: #fff;
  border-color: var(--el-color-primary);
}

.count-tag {
  background-color: rgba(255, 255, 255, 0.2);
  color: #fff;
  border-radius: 20px;
  padding: 5px 10px;
  font-weight: bold;
  font-size: 14px;
}

.posts-container {
  position: relative;
}

.loading-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--el-text-color-primary);
}

.loading-container p {
  margin-top: 10px;
  font-size: 16px;
}

.empty-container {
  padding: 50px 20px;
  text-align: center;
  color: var(--el-text-color-secondary);
}

.empty-container h3 {
  margin-top: 20px;
  color: var(--el-text-color-primary);
}

.empty-container p {
  margin-top: 10px;
  font-size: 16px;
}

.posts-list {
  display: flex;
  flex-direction: column;
}

.post-card {
  background-color: #fff;
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.user-avatar {
  margin-right: 15px;
  border: 2px solid var(--el-color-primary);
}

.user-info {
  flex-grow: 1;
}

.username {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.warm-gradient-text {
  background: linear-gradient(to right, #ffd700, #ffa500);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.post-type-tag {
  border-radius: 10px;
  padding: 3px 8px;
  font-weight: bold;
}

.post-text {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 10px;
  color: var(--el-text-color-regular);
}

.post-media {
  margin-top: 10px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.media-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.post-actions {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
  margin-top: 15px;
  border-top: 1px solid var(--el-border-color-lighter);
  padding-top: 15px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  font-weight: bold;
  transition: color 0.3s ease;
}

.action-btn:hover {
  color: var(--el-color-primary);
}

.like-btn:hover {
  color: var(--el-color-danger);
}

.comment-btn:hover {
  color: var(--el-color-info);
}

.share-btn:hover {
  color: var(--el-color-warning);
}

.custom-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>