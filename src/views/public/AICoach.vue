<script setup lang="ts">
import { ref, onUnmounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { VideoCameraFilled, VideoCamera, Check } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import { Pose, POSE_CONNECTIONS } from '@mediapipe/pose'
import { Camera } from '@mediapipe/camera_utils'
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'

// 状态管理
const isCameraActive = ref(false)
const videoStream = ref<MediaStream | null>(null)
const videoElementRef = ref<HTMLVideoElement | null>(null)
const canvasElementRef = ref<HTMLCanvasElement | null>(null)
const totalScore = ref(0)
const coordinationScore = ref(0)
const rhythmScore = ref(0)
let scoreUpdateInterval: number | null = null
let pose: Pose | null = null
let camera: Camera | null = null

// 动作要点
interface KeyPoint {
  id: number
  content: string
  type: string
  color: string
}

const keyPoints = ref<KeyPoint[]>([
  {
    id: 1,
    content: '双脚与肩同宽，保持重心稳定',
    type: 'primary',
    color: '#409eff'
  },
  {
    id: 2,
    content: '手臂自然弯曲，保持在胸前位置',
    type: 'success',
    color: '#67c23a'
  },
  {
    id: 3,
    content: '跟随音乐节奏，保持呼吸均匀',
    type: 'warning',
    color: '#e6a23c'
  },
  {
    id: 4,
    content: '注意保护膝关节，避免过度弯曲',
    type: 'danger',
    color: '#f56c6c'
  }
])

// 练习建议
interface Suggestion {
  id: string
  title: string
  content: string
}

const activeCollapse = ref(['1'])
const suggestions = ref<Suggestion[]>([
  {
    id: '1',
    title: '动作改进建议',
    content: '建议加强手臂的协调性训练，可以通过慢动作练习来提高准确度。'
  },
  {
    id: '2',
    title: '节奏训练建议',
    content: '可以先不跟音乐，单独练习基本步伐，熟练后再配合音乐。'
  },
  {
    id: '3',
    title: '体能建议',
    content: '目前运动强度适中，建议每次练习时间控制在45分钟以内。'
  }
])

// 练习历史
interface PracticeRecord {
  date: string
  duration: string
  dance: string
  score: number
  improvement: string
}

const practiceHistory = ref<PracticeRecord[]>([
  {
    date: '2025-03-28 15:30',
    duration: '30分钟',
    dance: '广场舞基础步伐',
    score: 85,
    improvement: '手臂动作需要更加协调'
  },
  {
    date: '2025-03-27 16:00',
    duration: '45分钟',
    dance: '民族舞基础',
    score: 92,
    improvement: '节奏把握得很好，继续保持'
  },
  {
    date: '2025-03-26 14:30',
    duration: '20分钟',
    dance: '健身舞基础',
    score: 78,
    improvement: '需要加强重心的稳定性'
  }
])

// 生成80到98之间的随机整数
const getRandomScore = (): number => {
  return Math.floor(Math.random() * (98 - 80 + 1)) + 80
}

// 更新分数
const updateScores = (): void => {
  let score1 = getRandomScore()
  let score2 = getRandomScore()
  let score3 = getRandomScore()

  // 确保三个分数不相同
  while (score2 === score1) {
    score2 = getRandomScore()
  }
  while (score3 === score1 || score3 === score2) {
    score3 = getRandomScore()
  }

  totalScore.value = score1
  coordinationScore.value = score2
  rhythmScore.value = score3
}

// 启动分数更新定时器
const startScoreUpdates = (): void => {
  stopScoreUpdates() // 先清除可能存在的旧定时器
  updateScores() // 立即更新一次分数
  scoreUpdateInterval = window.setInterval(updateScores, 2000)
}

// 停止分数更新定时器
const stopScoreUpdates = (): void => {
  if (scoreUpdateInterval) {
    clearInterval(scoreUpdateInterval)
    scoreUpdateInterval = null
  }
}

// 初始化 MediaPipe Pose
const initPose = async (): Promise<void> => {
  pose = new Pose({
    locateFile: (file) => {
      return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
    }
  })
  
  pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: false,
    smoothSegmentation: false,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
  })
  
  pose.onResults(onPoseResults)
}

// 处理姿态检测结果
const onPoseResults = (results: any): void => {
  if (!canvasElementRef.value) return
  
  const canvasCtx = canvasElementRef.value.getContext('2d')
  if (!canvasCtx) return
  
  // 清空画布
  canvasCtx.save()
  canvasCtx.clearRect(0, 0, canvasElementRef.value.width, canvasElementRef.value.height)
  
  // 绘制视频帧（镜像翻转）
  if (videoElementRef.value) {
    canvasCtx.translate(canvasElementRef.value.width, 0)
    canvasCtx.scale(-1, 1)
    canvasCtx.drawImage(
      videoElementRef.value, 
      0, 
      0, 
      canvasElementRef.value.width, 
      canvasElementRef.value.height
    )
    canvasCtx.setTransform(1, 0, 0, 1, 0, 0)
  }
  
  // 绘制骨骼
  if (results.poseLandmarks) {
    // 由于画面已经镜像翻转，我们需要翻转坐标
    const flippedLandmarks = results.poseLandmarks.map((landmark: any) => ({
      ...landmark,
      x: 1 - landmark.x
    }))
    
    // 绘制连接线（红色）
    drawConnectors(canvasCtx, flippedLandmarks, POSE_CONNECTIONS, {
      color: '#FF0000',
      lineWidth: 2
    })
    
    // 绘制关键点（绿色）
    drawLandmarks(canvasCtx, flippedLandmarks, {
      color: '#00FF00',
      lineWidth: 2,
      radius: 4
    })
  }
  
  canvasCtx.restore()
}

// 启动摄像头和录制
const startRecording = async (): Promise<void> => {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    ElMessage.error('您的浏览器不支持访问摄像头。')
    return
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        width: 1280, 
        height: 720 
      }, 
      audio: false 
    })
    videoStream.value = stream
    isCameraActive.value = true
    
    // 使用 nextTick 确保 video 和 canvas 元素已渲染
    await nextTick()
    
    if (videoElementRef.value && canvasElementRef.value) {
      videoElementRef.value.srcObject = stream
      
      // 等待视频元数据加载完成
      await new Promise((resolve) => {
        if (videoElementRef.value) {
          videoElementRef.value.onloadedmetadata = resolve
        }
      })
      
      // 设置 canvas 尺寸与视频一致
      if (canvasElementRef.value && videoElementRef.value) {
        canvasElementRef.value.width = videoElementRef.value.videoWidth
        canvasElementRef.value.height = videoElementRef.value.videoHeight
      }
      
      // 初始化 MediaPipe Pose
      await initPose()
      
      // 启动相机处理
      if (pose && videoElementRef.value) {
        camera = new Camera(videoElementRef.value, {
          onFrame: async () => {
            if (videoElementRef.value && pose) {
              await pose.send({ image: videoElementRef.value })
            }
          },
          width: 1280,
          height: 720
        })
        camera.start()
      }
    }
    
    startScoreUpdates() // 开始更新分数
    ElMessage.success('摄像头已启动，骨骼追踪已开启')
  } catch (err: any) {
    console.error('无法访问摄像头:', err)
    let message = '无法访问摄像头，请检查权限或设备连接。'
    if (err.name === 'NotAllowedError') {
      message = '您拒绝了摄像头访问权限。请在浏览器设置中允许摄像头访问。'
    } else if (err.name === 'NotFoundError') {
      message = '未检测到摄像头设备。请确认设备已正确连接。'
    } else if (err.name === 'NotReadableError') {
      message = '摄像头设备被其他应用程序占用。请关闭其他使用摄像头的应用程序，然后重试。'
    } else if (err.name === 'OverconstrainedError') {
      message = '摄像头不支持当前配置。'
    } else if (err.name === 'SecurityError') {
      message = '由于安全限制无法访问摄像头。请确保在HTTPS环境下使用。'
    }
    ElMessage.error(message)
    isCameraActive.value = false // 确保状态回滚
  }
}

// 停止摄像头和录制
const stopRecording = (): void => {
  stopScoreUpdates() // 停止更新分数，数值固定
  
  // 停止相机
  if (camera) {
    camera.stop()
    camera = null
  }
  
  // 关闭 pose
  if (pose) {
    pose.close()
    pose = null
  }
  
  if (videoStream.value) {
    videoStream.value.getTracks().forEach(track => track.stop())
    videoStream.value = null
  }
  if (videoElementRef.value) {
    videoElementRef.value.srcObject = null
  }
  
  // 清空 canvas
  if (canvasElementRef.value) {
    const canvasCtx = canvasElementRef.value.getContext('2d')
    if (canvasCtx) {
      canvasCtx.clearRect(0, 0, canvasElementRef.value.width, canvasElementRef.value.height)
    }
  }
  
  isCameraActive.value = false
  ElMessage.info('录制已停止')
}

// 切换摄像头状态
const toggleCamera = (): void => {
  if (isCameraActive.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

// 组件卸载时清理资源
onUnmounted(() => {
  stopRecording() // 确保摄像头和定时器被停止
})

// 初始化分数
updateScores()
</script>

<template>
  <div class="ai-coach-page page-with-nav">
    <PageHeader title="AI 智能教练" subtitle="实时分析您的舞蹈动作，提供专业指导" />

    <!-- 视频区域 -->
    <ElRow :gutter="20" class="mt-4">
      <ElCol :xs="24" :sm="24" :md="24" :lg="16">
        <ElCard class="video-section">
          <div class="video-container">
            <div v-if="!isCameraActive" class="video-placeholder">
              <el-icon :size="50"><VideoCameraFilled /></el-icon>
              <h3>准备开始练习</h3>
              <p>请启动摄像头，AI将实时追踪您的动作</p>
            </div>
            <div v-else class="video-canvas-wrapper">
              <video ref="videoElementRef" autoplay playsinline style="display: none;"></video>
              <canvas ref="canvasElementRef" class="pose-canvas"></canvas>
            </div>
          </div>
          <div class="video-controls">
            <ElButton :type="isCameraActive ? 'danger' : 'primary'" size="large" @click="toggleCamera">
              <el-icon><VideoCamera /></el-icon>
              {{ isCameraActive ? '停止录制' : '启动摄像头' }}
            </ElButton>
          </div>
        </ElCard>
      </ElCol>

      <ElCol :xs="24" :sm="24" :md="24" :lg="8">
        <ElCard class="score-section">
          <template #header>
            <div class="card-header">
              <span>实时得分</span>
            </div>
          </template>
          <ElRow :gutter="20">
            <ElCol :xs="8" :sm="8" :md="8" :lg="8" class="score-item">
              <ElProgress type="dashboard" :percentage="totalScore" :width="100" status="success">
                <template #default>
                  <div class="percentage">{{ totalScore }}<span>分</span></div>
                  <div class="progress-label">总体评分</div>
                </template>
              </ElProgress>
            </ElCol>
            <ElCol :xs="8" :sm="8" :md="8" :lg="8" class="score-item">
              <ElProgress type="dashboard" :percentage="coordinationScore" :width="100" color="#409eff">
                <template #default>
                  <div class="percentage">{{ coordinationScore }}<span>分</span></div>
                  <div class="progress-label">动作协调</div>
                </template>
              </ElProgress>
            </ElCol>
            <ElCol :xs="8" :sm="8" :md="8" :lg="8" class="score-item">
              <ElProgress type="dashboard" :percentage="rhythmScore" :width="100" color="#e6a23c">
                <template #default>
                  <div class="percentage">{{ rhythmScore }}<span>分</span></div>
                  <div class="progress-label">节奏感</div>
                </template>
              </ElProgress>
            </ElCol>
          </ElRow>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 动作指导与建议 -->
    <ElRow :gutter="20" class="mt-4">
      <ElCol :xs="24" :sm="24" :md="12">
        <ElCard class="guidance-section">
          <template #header>
            <div class="card-header">
              <span>动作要点</span>
            </div>
          </template>
          <div class="feedback-container">
            <div 
              v-for="point in keyPoints" 
              :key="point.id" 
              class="feedback-item"
              :style="{ backgroundColor: `${point.color}10`, color: point.color }"
            >
              <el-icon><Check /></el-icon>
              {{ point.content }}
            </div>
          </div>
        </ElCard>
      </ElCol>
      
      <ElCol :xs="24" :sm="24" :md="12">
        <ElCard class="suggestions-section">
          <template #header>
            <div class="card-header">
              <span>练习建议</span>
            </div>
          </template>
          <ElCollapse v-model="activeCollapse">
            <ElCollapseItem 
              v-for="suggestion in suggestions" 
              :key="suggestion.id" 
              :title="suggestion.title" 
              :name="suggestion.id"
            >
              {{ suggestion.content }}
            </ElCollapseItem>
          </ElCollapse>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 练习历史 -->
    <ElRow class="mt-4">
      <ElCol :span="24">
        <ElCard class="history-section">
          <template #header>
            <div class="card-header">
              <span>练习历史</span>
            </div>
          </template>
          <ElTable :data="practiceHistory" stripe style="width: 100%">
            <ElTableColumn prop="date" label="日期时间" />
            <ElTableColumn prop="duration" label="时长" />
            <ElTableColumn prop="dance" label="舞蹈类型" />
            <ElTableColumn prop="score" label="得分" />
            <ElTableColumn prop="improvement" label="改进建议" />
          </ElTable>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>

<style scoped>
/* AICoach页面主样式 */
.ai-coach-page {
  padding: 20px;
  padding-bottom: 100px; /* 为底部导航添加安全区域 */
  max-width: 1200px;
  margin: 0 auto;
}

.ai-coach-page.page-with-nav {
  /* 确保与顶部导航栏有正确间距 */
  padding-top: 20px;
}

.video-container {
  height: 400px;
  background-color: #f5f7fa;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-placeholder {
  text-align: center;
  color: #909399;
}

.video-placeholder .el-icon {
  margin-bottom: 20px;
}

.video-controls {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.score-section {
  height: 100%;
}

.score-item {
  text-align: center;
}

.progress-label {
  font-size: 18px;
  color: #606266;
  line-height: 1.4;
}

.percentage {
  font-size: 20px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.guidance-section, .suggestions-section {
  height: 100%;
  margin-bottom: 20px;
}

.feedback-container {
  margin-bottom: 15px;
}

.feedback-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.feedback-item .el-icon {
  margin-right: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 自定义工具类 */
.mt-1 { margin-top: 0.25rem !important; }
.mt-2 { margin-top: 0.5rem !important; }
.mt-3 { margin-top: 1rem !important; }
.mt-4 { margin-top: 1.5rem !important; }
.mt-5 { margin-top: 3rem !important; }

.history-section {
  margin-bottom: 80px;
}

@media (max-width: 992px) {
  .video-container {
    height: 300px;
  }
  
  .ai-coach {
    margin-bottom: 60px;
  }
}

@media (max-width: 768px) {
  .video-container {
    height: 250px;
  }
  
  .score-item {
    margin-bottom: 20px;
  }
}

.video-container video {
  display: block; /* 防止video底部出现小间隙 */
}

.video-canvas-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pose-canvas {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  display: block;
}
</style> 