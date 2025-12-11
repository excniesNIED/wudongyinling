<template>
  <div class="page-header">
    <div class="container">
      <!-- 面包屑导航 -->
      <div v-if="showBreadcrumb && breadcrumbs.length > 0" class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item 
            v-for="(item, index) in breadcrumbs" 
            :key="index"
            :to="item.to"
            :class="{ 'is-current': index === breadcrumbs.length - 1 }"
          >
            <el-icon v-if="item.icon" class="breadcrumb-icon">
              <component :is="item.icon" />
            </el-icon>
            {{ item.label }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">{{ title }}</h1>
          <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
        </div>
        
        <div v-if="$slots.actions" class="actions-section">
          <slot name="actions"></slot>
        </div>
      </div>
      
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

interface BreadcrumbItem {
  label: string
  to?: string
  icon?: any
}

const props = defineProps({
  /**
   * 页面标题
   */
  title: {
    type: String,
    required: true
  },
  /**
   * 页面副标题
   */
  subtitle: {
    type: String,
    default: ''
  },
  /**
   * 是否显示面包屑导航
   */
  showBreadcrumb: {
    type: Boolean,
    default: true
  },
  /**
   * 自定义面包屑导航
   */
  customBreadcrumbs: {
    type: Array as () => BreadcrumbItem[],
    default: () => []
  },
  /**
   * 是否自动生成面包屑
   */
  autoBreadcrumb: {
    type: Boolean,
    default: true
  }
})

const route = useRoute()

// 自动生成面包屑导航
const breadcrumbs = computed(() => {
  if (props.customBreadcrumbs.length > 0) {
    return props.customBreadcrumbs
  }
  
  if (!props.autoBreadcrumb) {
    return []
  }
  
  const crumbs: BreadcrumbItem[] = []
  const pathSegments = route.path.split('/').filter(segment => segment)
  
  // 添加首页
  crumbs.push({
    label: '首页',
    to: '/',
    icon: 'House'
  })
  
  // 根据路径生成面包屑
  let currentPath = ''
  const routeMap: Record<string, string> = {
    'dance-courses': '舞蹈课程',
    'my-courses': '我的课程',
    'ai-coach': 'AI教练',
    'health-management': '健康管理',
    'social-platform': '社交平台',
    'user-profile': '个人资料',
    'favorites': '我的收藏',
    'chat-room': '聊天室',
    'about': '关于我们',
    'contact': '联系我们',
    'faq': '常见问题',
    'login': '登录',
    'register': '注册',
    'admin': '管理后台',
    'dashboard': '仪表盘',
    'user-management': '用户管理',
    'course-management': '课程管理',
    'health-records': '健康记录',
    'statistics': '数据统计',
    'system-settings': '系统设置'
  }
  
  pathSegments.forEach((segment, index) => {
    currentPath += `/${segment}`
    const isLast = index === pathSegments.length - 1
    
    if (routeMap[segment]) {
      crumbs.push({
        label: routeMap[segment],
        to: isLast ? undefined : currentPath
      })
    }
  })
  
  return crumbs
})
</script>

<style scoped>
.page-header {
  @apply py-8 mb-8;
  /* 使用金黄色主题替代蓝色，与整体风格一致 */
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(205, 133, 63, 0.15) 100%);
  min-height: 120px;
  display: flex;
  align-items: center;
}

.container {
  @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
  width: 100%;
}

.breadcrumb-container {
  @apply mb-6;
}

.breadcrumb-icon {
  @apply mr-1;
}

:deep(.el-breadcrumb) {
  @apply justify-center;
}

:deep(.el-breadcrumb__item) {
  @apply text-sm;
}

:deep(.el-breadcrumb__item.is-current) {
  @apply font-medium;
  /* 使用金黄色主题替代蓝色 */
  color: var(--primary-color, #d4af37);
}

.header-content {
  @apply flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6;
}

.title-section {
  @apply flex-1 text-center lg:text-left;
}

.actions-section {
  @apply flex-shrink-0;
}

.page-title {
  @apply text-2xl sm:text-3xl md:text-4xl font-bold mb-2 sm:mb-4;
  /* 使用金黄色主题替代蓝色 */
  color: var(--primary-color, #d4af37);
  line-height: 1.2;
  word-break: break-word;
}

.page-subtitle {
  @apply text-sm sm:text-base lg:text-lg text-gray-600 max-w-2xl mx-auto lg:mx-0;
  line-height: 1.5;
  margin-top: 8px;
}

/* 为大屏幕优化显示 */
@media (min-width: 1024px) {
  .page-header {
    @apply py-12;
    min-height: 160px;
  }
  
  .page-title {
    @apply text-4xl lg:text-5xl;
  }
  
  .page-subtitle {
    @apply text-xl;
  }
  
  :deep(.el-breadcrumb) {
    @apply justify-start;
  }
}

/* 为小屏幕优化显示 */
@media (max-width: 640px) {
  .page-header {
    @apply py-6;
    min-height: 100px;
    margin-bottom: 1.5rem;
  }
  
  .container {
    @apply px-3;
  }
  
  .breadcrumb-container {
    @apply mb-3;
  }
  
  :deep(.el-breadcrumb) {
    @apply text-xs;
  }
  
  .header-content {
    @apply gap-3;
  }
  
  .page-title {
    @apply text-xl mb-2;
  }
  
  .page-subtitle {
    @apply text-sm;
  }
}

/* 响应式面包屑 */
@media (max-width: 768px) {
  .breadcrumb-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  .breadcrumb-container::-webkit-scrollbar {
    display: none;
  }
  
  :deep(.el-breadcrumb) {
    @apply whitespace-nowrap inline-flex;
  }
  
  :deep(.el-breadcrumb__item) {
    @apply flex-shrink-0;
  }
}

@media (max-width: 480px) {
  :deep(.el-breadcrumb__item:not(:first-child):not(:last-child)) {
    @apply hidden;
  }
  
  :deep(.el-breadcrumb__item:nth-last-child(2))::before {
    content: "...";
    @apply mx-1 text-gray-400;
  }
  
  .page-header {
    padding-top: env(safe-area-inset-top, 24px);
  }
}
</style> 