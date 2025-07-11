<template>
  <div class="dashboard-container">
    <h2>仪表板</h2>
    <div class="dashboard-content">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>总课程数</span>
              </div>
            </template>
            <div class="card-content">
              <h3>{{ stats.totalCourses || 0 }}</h3>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>总用户数</span>
              </div>
            </template>
            <div class="card-content">
              <h3>{{ stats.totalUsers || 0 }}</h3>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { statsApi } from '@/api'

const stats = ref({
  totalCourses: 0,
  totalUsers: 0
})

const fetchStats = async () => {
  try {
    const res = await statsApi.getDashboardStats()
    stats.value = res.data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-content {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.card-content h3 {
  margin: 0;
  font-size: 24px;
  color: #409EFF;
}
</style> 