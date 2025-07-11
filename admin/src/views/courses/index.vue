<template>
  <div class="course-container">
    <div class="header">
      <h2>课程管理</h2>
      <el-button type="primary" @click="handleAdd">添加课程</el-button>
    </div>

    <el-table v-loading="loading" :data="courses" border style="width: 100%">
      <el-table-column prop="title" label="课程名称" />
      <el-table-column prop="description" label="课程描述" show-overflow-tooltip />
      <el-table-column prop="difficulty" label="难度等级">
        <template #default="{ row }">
          <el-tag :type="row.difficulty === 'beginner' ? 'success' : row.difficulty === 'intermediate' ? 'warning' : 'danger'">
            {{ row.difficulty === 'beginner' ? '初级' : row.difficulty === 'intermediate' ? '中级' : '高级' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="duration" label="时长">
        <template #default="{ row }">
          {{ row.duration }}分钟
        </template>
      </el-table-column>
      <el-table-column label="封面图片" width="120">
        <template #default="{ row }">
          <el-image
            v-if="row.cover_url"
            :src="row.cover_url"
            :preview-src-list="[row.cover_url]"
            fit="cover"
            style="width: 50px; height: 50px"
          />
          <span v-else>暂无封面</span>
        </template>
      </el-table-column>
      <el-table-column label="课程视频" width="120">
        <template #default="{ row }">
          <el-button v-if="row.video_url" type="primary" link @click="handlePreviewVideo(row)">
            预览视频
          </el-button>
          <span v-else>暂无视频</span>
        </template>
      </el-table-column>
      <el-table-column prop="instructor" label="教练" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" @click="handleDelete(row.id)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="课程描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="难度等级" prop="difficulty">
          <el-select v-model="form.difficulty" style="width: 100%">
            <el-option label="初级" value="beginner" />
            <el-option label="中级" value="intermediate" />
            <el-option label="高级" value="advanced" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程时长" prop="duration">
          <el-input-number v-model="form.duration" :min="1" :max="360" />
          <span class="unit">分钟</span>
        </el-form-item>
        <el-form-item label="封面图片" prop="cover_url">
          <el-upload
            class="cover-uploader"
            action="/api/v1/courses/upload/image"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleCoverSuccess"
            :on-error="handleUploadError"
            accept="image/*"
          >
            <el-image
              v-if="form.cover_url"
              :src="form.cover_url"
              fit="cover"
              class="cover-preview"
            />
            <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="课程视频" prop="video_url">
          <el-upload
            class="video-uploader"
            action="/api/v1/courses/upload/video"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleVideoSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeVideoUpload"
            accept="video/*"
          >
            <div v-if="form.video_url" class="video-preview">
              <video :src="form.video_url" controls width="200"></video>
            </div>
            <el-icon v-else class="video-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit(formRef)">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="previewVisible" title="视频预览" width="800px">
      <video v-if="previewVideoUrl" :src="previewVideoUrl" controls width="100%"></video>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { courseApi } from '@/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(false)
const courses = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref('add')
const formRef = ref(null)
const previewVisible = ref(false)
const previewVideoUrl = ref('')

const uploadUrl = `${import.meta.env.VITE_API_BASE_URL}/api/v1/courses/upload-video`
const uploadHeaders = {
  Authorization: `Bearer ${userStore.token}`
}

const form = ref({
  id: '',
  title: '',
  description: '',
  difficulty: 'beginner',
  duration: 60,
  cover_url: '',
  video_url: ''
})

const rules = {
  title: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入课程描述', trigger: 'blur' }],
  difficulty: [{ required: true, message: '请选择难度等级', trigger: 'change' }],
  duration: [{ required: true, message: '请输入课程时长', trigger: 'blur' }]
}

const fetchCourses = async () => {
  loading.value = true
  try {
    const res = await courseApi.getCourses({
      page: currentPage.value,
      pageSize: pageSize.value
    })
    courses.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取课程列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  formMode.value = 'add'
  dialogTitle.value = '添加课程'
  form.value = {
    id: '',
    title: '',
    description: '',
    difficulty: 'beginner',
    duration: 60,
    cover_url: '',
    video_url: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑课程'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除该课程吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await courseApi.deleteCourse(id)
      ElMessage.success('删除成功')
      fetchCourses()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleSubmit = async (formEl) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        if (formMode.value === 'add') {
          await courseApi.createCourse(form.value)
          ElMessage.success('添加成功')
        } else {
          await courseApi.updateCourse(form.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchCourses()
      } catch (error) {
        ElMessage.error(formMode.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

const beforeVideoUpload = (file) => {
  const isVideo = file.type.startsWith('video/')
  const isLt100M = file.size / 1024 / 1024 < 100

  if (!isVideo) {
    ElMessage.error('请上传视频文件！')
    return false
  }
  if (!isLt100M) {
    ElMessage.error('视频大小不能超过 100MB！')
    return false
  }
  return true
}

const handleCoverSuccess = (response) => {
  form.value.cover_url = response.url
  ElMessage.success('封面上传成功')
}

const handleVideoSuccess = (response) => {
  form.value.video_url = response.url
  ElMessage.success('视频上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const handlePreviewVideo = (row) => {
  previewVideoUrl.value = row.video_url
  previewVisible.value = true
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchCourses()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchCourses()
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.course-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.cover-uploader,
.video-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}

.cover-uploader:hover,
.video-uploader:hover {
  border-color: #409EFF;
}

.cover-uploader-icon,
.video-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-preview {
  width: 100px;
  height: 100px;
  display: block;
}

.video-preview {
  width: 200px;
}

.unit {
  margin-left: 10px;
}
</style> 