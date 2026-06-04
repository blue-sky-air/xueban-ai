<template>
  <div class="home">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner">
      <div class="banner-content">
        <div class="banner-text">
          <h2>👋 你好，{{ authStore.username || '同学' }}！</h2>
          <p>让AI成为你的学习伙伴，规划、竞赛、创新一站搞定</p>
        </div>
        <div class="banner-stats">
          <div class="stat-item">
            <span class="stat-num">3</span>
            <span class="stat-label">核心功能</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">15+</span>
            <span class="stat-label">项目方向</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">11</span>
            <span class="stat-label">竞赛类型</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 三大功能卡片 -->
    <div class="feature-cards">
      <div class="feature-card" v-for="(card, i) in cards" :key="card.title"
           :style="{ animationDelay: `${i * 0.12}s` }" @click="router.push(card.path)">
        <div class="card-glow" :style="{ background: card.glow }"></div>
        <div class="card-icon" :style="{ background: card.gradient }">
          <span>{{ card.icon }}</span>
        </div>
        <h3>{{ card.title }}</h3>
        <p>{{ card.desc }}</p>
        <div class="card-tags">
          <el-tag v-for="tag in card.tags" :key="tag.text" :type="tag.type" size="small" effect="plain">
            {{ tag.text }}
          </el-tag>
        </div>
        <div class="card-action">
          <span>{{ card.action }}</span>
          <el-icon><ArrowRight /></el-icon>
        </div>
      </div>
    </div>

    <!-- 快速开始 -->
    <div class="quick-section">
      <h3>💡 快速开始</h3>
      <div class="quick-items">
        <el-button v-for="q in quickItems" :key="q.text" @click="router.push(q.path)" size="large" class="quick-btn">
          {{ q.icon }} {{ q.text }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const cards = [
  {
    icon: '📚', title: 'AI学习规划', path: '/study',
    desc: '输入专业、年级和目标，AI为你量身定制个性化学习路径',
    gradient: 'linear-gradient(135deg, #667eea, #764ba2)',
    glow: 'radial-gradient(circle at 50% 0%, rgba(102,126,234,0.15), transparent 70%)',
    tags: [{ text: '个性化路径', type: '' }, { text: '课程推荐', type: 'success' }],
    action: '开始规划'
  },
  {
    icon: '🏆', title: 'AI竞赛辅导', path: '/competition',
    desc: '选择竞赛类型，获取专业备赛方案、学习资源和获奖技巧',
    gradient: 'linear-gradient(135deg, #f093fb, #f5576c)',
    glow: 'radial-gradient(circle at 50% 0%, rgba(240,147,251,0.15), transparent 70%)',
    tags: [{ text: '备赛计划', type: 'warning' }, { text: '资源推荐', type: 'info' }],
    action: '开始辅导'
  },
  {
    icon: '🚀', title: 'AI项目生成', path: '/project',
    desc: '选择方向，AI自动生成完整项目方案：命名、简介、技术路线、商业模式',
    gradient: 'linear-gradient(135deg, #4facfe, #00f2fe)',
    glow: 'radial-gradient(circle at 50% 0%, rgba(79,172,254,0.15), transparent 70%)',
    tags: [{ text: '5步生成', type: 'danger' }, { text: '完整方案', type: '' }],
    action: '开始生成', featured: true
  }
]

const quickItems = [
  { icon: '🚀', text: '生成一个AI+医疗项目', path: '/project' },
  { icon: '🏆', text: '数学建模竞赛备赛', path: '/competition' },
  { icon: '📚', text: '制定考研学习规划', path: '/study' }
]
</script>

<style scoped>
.home { padding: 0 0 40px; }

/* 欢迎横幅 */
.welcome-banner {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #a855f7 100%);
  border-radius: 20px;
  padding: 32px;
  color: #fff;
  margin-bottom: 28px;
  animation: fadeInUp 0.5s ease-out;
  position: relative;
  overflow: hidden;
}
.welcome-banner::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 300px;
  height: 300px;
  background: rgba(255,255,255,0.06);
  border-radius: 50%;
}
.banner-content { display: flex; justify-content: space-between; align-items: center; position: relative; }
.banner-text h2 { font-size: 22px; margin-bottom: 6px; }
.banner-text p { opacity: 0.85; font-size: 14px; }
.banner-stats { display: flex; gap: 24px; }
.stat-item { text-align: center; }
.stat-num { display: block; font-size: 28px; font-weight: 800; }
.stat-label { font-size: 12px; opacity: 0.7; }

/* 功能卡片 */
.feature-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}
.feature-card {
  background: #fff;
  border-radius: 20px;
  padding: 28px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
  animation: fadeInUp 0.5s ease-out both;
}
.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: transparent;
}
.card-glow {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 120px;
  opacity: 0;
  transition: opacity 0.4s;
  pointer-events: none;
}
.feature-card:hover .card-glow { opacity: 1; }

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-bottom: 16px;
  transition: transform 0.3s;
}
.feature-card:hover .card-icon { transform: scale(1.1) rotate(-3deg); }

.feature-card h3 { font-size: 18px; margin-bottom: 8px; color: #1e293b; font-weight: 700; }
.feature-card p { color: #64748b; font-size: 13px; line-height: 1.6; margin-bottom: 12px; }
.card-tags { margin-bottom: 16px; display: flex; gap: 6px; }

.card-action {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #4F46E5;
  font-weight: 600;
  font-size: 14px;
  transition: gap 0.3s;
}
.feature-card:hover .card-action { gap: 8px; }

/* 快速开始 */
.quick-section {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  animation: fadeInUp 0.5s ease-out 0.4s both;
  border: 1px solid #e2e8f0;
}
.quick-section h3 { margin-bottom: 16px; color: #1e293b; font-weight: 700; }
.quick-items { display: flex; gap: 12px; flex-wrap: wrap; }
.quick-btn {
  border-radius: 12px !important;
  font-weight: 500 !important;
  transition: all 0.3s !important;
}
.quick-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

@media (max-width: 768px) {
  .feature-cards { grid-template-columns: 1fr; }
  .banner-content { flex-direction: column; gap: 16px; }
  .banner-stats { gap: 16px; }
}
</style>
