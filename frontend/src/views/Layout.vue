<template>
  <div class="layout">
    <header class="header">
      <div class="header-inner">
        <div class="header-left" @click="router.push('/')">
          <span class="logo-icon">🎓</span>
          <span class="logo-text">学伴AI</span>
        </div>
        <nav class="nav-menu">
          <router-link v-for="item in navItems" :key="item.path" :to="item.path"
                       :class="['nav-item', { active: route.path === item.path }]">
            <span class="nav-icon">{{ item.icon }}</span>
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </nav>
        <div class="header-right">
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-avatar">
              <span>{{ (authStore.username || 'U')[0] }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item disabled>
                  <span style="font-weight:600">{{ authStore.username }}</span>
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>
    <main class="main-content">
      <router-view v-slot="{ Component, route: r }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="r.path" />
        </transition>
      </router-view>
    </main>
    <footer class="footer">
      <div class="footer-inner">
        <span class="copyright">© 2026 学伴AI</span>
        <span class="divider">|</span>
        <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer" class="icp-link">
          晋ICP备2026004245号
        </a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  { path: '/', icon: '🏠', label: '首页' },
  { path: '/study', icon: '📚', label: '学习规划' },
  { path: '/competition', icon: '🏆', label: '竞赛辅导' },
  { path: '/project', icon: '🚀', label: '项目生成' },
  { path: '/favorites', icon: '⭐', label: '收藏' }
]

function handleCommand(cmd) {
  if (cmd === 'logout') { authStore.logout(); router.push('/login') }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  margin-right: 32px;
  flex-shrink: 0;
}
.logo-icon { font-size: 24px; }
.logo-text {
  font-size: 18px;
  font-weight: 800;
  background: linear-gradient(135deg, #4F46E5, #7C3AED);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  gap: 4px;
  flex: 1;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 10px;
  text-decoration: none;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.25s;
  white-space: nowrap;
}
.nav-item:hover {
  color: #4F46E5;
  background: #f5f3ff;
}
.nav-item.active {
  color: #4F46E5;
  background: #ede9fe;
  font-weight: 600;
}
.nav-icon { font-size: 16px; }

.header-right { margin-left: auto; }
.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #4F46E5, #7C3AED);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}
.user-avatar:hover {
  transform: scale(1.08);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.main-content {
  max-width: 1200px;
  margin: 24px auto;
  width: 100%;
  padding: 0 24px;
  animation: fadeIn 0.3s ease-out;
  flex: 1;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 页面切换 */
.page-enter-active { animation: pageSlideIn 0.3s ease-out; }
.page-leave-active { animation: pageSlideOut 0.15s ease-in; }
@keyframes pageSlideIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes pageSlideOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

@media (max-width: 768px) {
  .nav-label { display: none; }
  .nav-item { padding: 8px 10px; }
  .header-left { margin-right: 12px; }
  .logo-text { display: none; }
}

/* 底部备案信息 */
.footer {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  padding: 16px 0;
  margin-top: auto;
}
.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 13px;
  color: #94a3b8;
}
.copyright {
  color: #64748b;
}
.divider {
  color: #cbd5e1;
}
.icp-link {
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s;
}
.icp-link:hover {
  color: #4F46E5;
  text-decoration: underline;
}
</style>
