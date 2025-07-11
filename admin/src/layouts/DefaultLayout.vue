<template>
  <div class="layout-container">
    <el-container>
      <el-aside width="200px">
        <div class="logo">
          <h1>管理系统</h1>
        </div>
        <el-menu
          router
          :default-active="route.path"
          class="el-menu-vertical"
        >
          <el-menu-item index="/">
            <el-icon><DataLine /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/courses">
            <el-icon><Reading /></el-icon>
            <span>课程管理</span>
          </el-menu-item>
          <el-menu-item index="/prescriptions">
            <el-icon><Document /></el-icon>
            <span>运动处方</span>
          </el-menu-item>
          <el-menu-item index="/health-records">
            <el-icon><List /></el-icon>
            <span>健康记录</span>
          </el-menu-item>
          <el-menu-item index="/challenges">
            <el-icon><Trophy /></el-icon>
            <span>打卡挑战</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                {{ userStore.userInfo.username }}
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import {
  DataLine,
  User,
  Reading,
  Document,
  List,
  Trophy,
  ArrowDown
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.logo {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  background-color: var(--el-menu-bg-color);
}

.logo h1 {
  margin: 0;
  font-size: 18px;
}

.el-aside {
  background-color: var(--el-menu-bg-color);
  color: var(--el-menu-text-color);
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.el-main {
  background-color: #f5f7fa;
  padding: 0;
}
</style> 