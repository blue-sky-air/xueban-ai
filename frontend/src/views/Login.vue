<template>
  <div class="login-page">
    <div class="login-bg">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
      <div class="bg-shape shape-3"></div>
    </div>
    <div class="login-card">
      <div class="logo-area">
        <div class="logo-icon">🎓</div>
        <h1 class="title">学伴AI</h1>
        <p class="subtitle">你的专属AI学习助手</p>
      </div>

      <el-tabs v-model="activeTab" class="tabs">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" @submit.prevent="handleLogin">
            <el-form-item>
              <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="User" size="large" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password />
            </el-form-item>
            <el-button type="primary" size="large" :loading="loading" @click="handleLogin" style="width:100%">
              登 录
            </el-button>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form :model="regForm" @submit.prevent="handleRegister">
            <el-form-item>
              <el-input v-model="regForm.username" placeholder="用户名" prefix-icon="User" size="large" />
            </el-form-item>
            <el-form-item>
              <el-input v-model="regForm.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password />
            </el-form-item>
            <el-form-item>
              <el-select v-model="regForm.major" placeholder="选择专业（可选）" size="large" clearable style="width:100%">
                <el-option v-for="m in majors" :key="m" :label="m" :value="m" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-select v-model="regForm.grade" placeholder="选择年级（可选）" size="large" clearable style="width:100%">
                <el-option v-for="g in grades" :key="g" :label="g" :value="g" />
              </el-select>
            </el-form-item>
            <el-button type="primary" size="large" :loading="loading" @click="handleRegister" style="width:100%">
              注 册
            </el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>

      <div class="divider">
        <span>或者</span>
      </div>

      <el-button class="guest-btn" size="large" @click="guestLogin" :loading="guestLoading">
        🚀 游客模式快速体验
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authApi } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const activeTab = ref('login')
const loading = ref(false)
const guestLoading = ref(false)

const loginForm = ref({ username: '', password: '' })
const regForm = ref({ username: '', password: '', major: '', grade: '' })

const majors = ['计算机科学与技术', '软件工程', '人工智能', '数据科学', '信息安全', '电子信息工程', '通信工程', '自动化', '数学与应用数学', '其他']
const grades = ['大一', '大二', '大三', '大四', '研一', '研二']

async function handleLogin() {
  if (!loginForm.value.username || !loginForm.value.password) { ElMessage.warning('请输入用户名和密码'); return }
  loading.value = true
  try { const res = await authApi.login(loginForm.value); authStore.setAuth(res); ElMessage.success('登录成功'); router.push('/') } catch (e) {} finally { loading.value = false }
}

async function handleRegister() {
  if (!regForm.value.username || !regForm.value.password) { ElMessage.warning('请输入用户名和密码'); return }
  loading.value = true
  try { const res = await authApi.register(regForm.value); authStore.setAuth(res); ElMessage.success('注册成功'); router.push('/') } catch (e) {} finally { loading.value = false }
}

async function guestLogin() {
  guestLoading.value = true
  try { const res = await authApi.guest(); authStore.setAuth(res); router.push('/') } catch (e) {} finally { guestLoading.value = false }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.login-bg { position: absolute; inset: 0; overflow: hidden; }
.bg-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
  animation: float 8s ease-in-out infinite;
}
.shape-1 {
  width: 400px; height: 400px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  top: -100px; right: -100px;
  animation-delay: 0s;
}
.shape-2 {
  width: 300px; height: 300px;
  background: linear-gradient(135deg, #f093fb, #f5576c);
  bottom: -80px; left: -80px;
  animation-delay: -3s;
}
.shape-3 {
  width: 200px; height: 200px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  top: 50%; left: 10%;
  animation-delay: -5s;
}
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(5deg); }
  66% { transform: translateY(10px) rotate(-3deg); }
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 40px;
  width: 420px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
  animation: scaleIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.logo-area { text-align: center; margin-bottom: 28px; }
.logo-icon {
  font-size: 48px;
  margin-bottom: 8px;
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.title {
  font-size: 32px;
  background: linear-gradient(135deg, #4F46E5, #7C3AED);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  letter-spacing: -0.5px;
}
.subtitle { color: #94a3b8; margin-top: 4px; font-size: 14px; }

.tabs :deep(.el-tabs__nav-wrap::after) { display: none; }
.tabs :deep(.el-tabs__item) { font-size: 15px; font-weight: 500; }

.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  color: #94a3b8;
  font-size: 13px;
}
.divider::before, .divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e2e8f0;
}
.divider span { padding: 0 12px; }

.guest-btn {
  width: 100%;
  border-radius: 12px !important;
  border: 2px dashed #c7d2fe !important;
  color: #4F46E5 !important;
  background: #f5f3ff !important;
  font-weight: 600 !important;
  transition: all 0.3s !important;
}
.guest-btn:hover {
  border-color: #4F46E5 !important;
  background: #ede9fe !important;
  transform: translateY(-1px);
}
</style>
