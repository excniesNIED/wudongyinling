<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>舞动银龄 - 用户登录</h2>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginFormData"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginFormData.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginFormData.password"
            placeholder="请输入密码"
            type="password"
            show-password
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="loginFormData.remember">记住我</el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" class="login-button">
            登录
          </el-button>
        </el-form-item>
        
        <div class="login-tips">
          <p>演示账号: admin</p>
          <p>演示密码: admin</p>
        </div>
        
        <div class="demo-login">
          <el-button type="success" @click="demoLogin" :loading="loading">
            使用演示账号登录
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const loading = ref(false);
const loginFormRef = ref(null);
const loginFormData = reactive({
  username: '',
  password: '',
  remember: false
});

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 5, message: '密码至少为5个字符', trigger: 'blur' }
  ]
};

const handleLogin = () => {
  loginFormRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.error('请完善表单后重试');
      return;
    }
    loading.value = true;
    try {
      await userStore.login({
        username: loginFormData.username,
        password: loginFormData.password,
      });
      ElMessage.success('登录成功');
      const redirectPath = route.query.redirect || '/';
      await router.replace(redirectPath);
    } catch (error) {
      // The error message is already handled by the response interceptor in request.js
      console.error('Login failed in component:', error);
    } finally {
      loading.value = false;
    }
  });
};

const demoLogin = () => {
  loginFormData.username = 'admin';
  loginFormData.password = 'admin';
  handleLogin();
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  max-width: 90%;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: var(--primary-color);
}

.login-button {
  width: 100%;
}

.login-tips {
  margin-top: 20px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  color: #606266;
  font-size: 14px;
}

.login-tips p {
  margin: 5px 0;
}

.demo-login {
  margin-top: 20px;
  text-align: center;
}

@media (max-width: 480px) {
  .login-card {
    width: 320px;
  }
}
</style> 