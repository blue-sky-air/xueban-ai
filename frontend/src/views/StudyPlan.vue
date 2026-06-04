<template>
  <div class="study-plan">
    <h2 class="page-title">📚 AI学习规划</h2>
    <p class="page-desc">输入你的专业、年级和学习目标，AI为你量身定制学习路径</p>

    <div class="content-wrapper">
      <!-- 左侧输入 -->
      <div class="input-panel">
        <el-card shadow="never">
          <template #header><span style="font-weight:600">📋 填写信息</span></template>
          <el-form label-position="top">
            <el-form-item label="专业">
              <el-select v-model="form.major" placeholder="选择专业" style="width:100%">
                <el-option v-for="m in majors" :key="m" :label="m" :value="m" />
              </el-select>
            </el-form-item>
            <el-form-item label="年级">
              <el-radio-group v-model="form.grade">
                <el-radio-button v-for="g in grades" :key="g" :value="g">{{ g }}</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="学习目标">
              <el-radio-group v-model="form.goal">
                <el-radio-button v-for="g in goals" :key="g" :value="g">{{ g }}</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="已有基础（可多选）">
              <el-checkbox-group v-model="form.basics">
                <el-checkbox v-for="b in basicsList" :key="b" :value="b" :label="b" />
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="目标院校（可选）">
              <el-input v-model="form.target_school" placeholder="如：浙江大学" />
            </el-form-item>
            <el-button type="primary" size="large" :loading="loading" @click="handleGenerate" style="width:100%">
              {{ loading ? 'AI规划中...' : '🎯 生成学习规划' }}
            </el-button>
          </el-form>
        </el-card>
      </div>

      <!-- 右侧结果 -->
      <div class="result-panel">
        <el-card v-if="!result && !loading" shadow="never" class="empty-card">
          <el-empty description="填写左侧信息后点击生成，AI将为你定制学习规划" />
        </el-card>

        <el-card v-if="loading" shadow="never" class="loading-card">
          <div class="loading-animation">
            <el-icon class="is-loading" :size="40" color="#4F46E5"><Loading /></el-icon>
            <p class="loading-text">AI正在生成中，请稍候...</p>
          </div>
        </el-card>

        <template v-if="result && !loading">
          <el-card shadow="never" class="result-card">
            <div class="overview">
              <h3>📋 {{ form.major }} · {{ form.grade }} · {{ form.goal }}</h3>
              <p>{{ result.overview }}</p>
            </div>
          </el-card>

          <el-card v-for="(phase, i) in result.phases" :key="i" shadow="never" class="result-card phase-card">
            <div class="phase-header">
              <span class="phase-num">阶段{{ i + 1 }}</span>
              <span class="phase-title">{{ phase.title }}</span>
              <el-tag size="small" type="info">{{ phase.period }}</el-tag>
            </div>
            <div class="phase-body">
              <h4>📌 学习任务</h4>
              <ul><li v-for="(t, j) in phase.tasks" :key="j">{{ t }}</li></ul>
              <h4 v-if="phase.resources?.length">📖 推荐资源</h4>
              <ul v-if="phase.resources?.length"><li v-for="(r, j) in phase.resources" :key="j">{{ r }}</li></ul>
            </div>
          </el-card>

          <el-card v-if="result.daily_plan" shadow="never" class="result-card">
            <h3>⏰ 每日学习计划</h3>
            <p class="daily-plan">{{ result.daily_plan }}</p>
          </el-card>

          <el-card v-if="result.tips?.length" shadow="never" class="result-card">
            <h3>💡 学习建议</h3>
            <ul class="tips-list"><li v-for="(t, i) in result.tips" :key="i">{{ t }}</li></ul>
          </el-card>

          <div class="action-bar">
            <el-button @click="handleFavorite" :type="isFavorite ? 'warning' : 'default'">
              {{ isFavorite ? '⭐ 已收藏' : '☆ 收藏' }}
            </el-button>
            <el-button @click="exportResult">📥 导出Markdown</el-button>
            <el-button @click="result = null">🔄 重新生成</el-button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { studyApi, favoriteApi } from '../api'
import { ElMessage } from 'element-plus'

const majors = ['计算机科学与技术', '软件工程', '人工智能', '数据科学', '信息安全', '电子信息工程', '通信工程', '自动化', '数学与应用数学', '其他']
const grades = ['大一', '大二', '大三', '大四']
const goals = ['考研', '就业', '出国', '竞赛', '综合提升']
const basicsList = ['Python', 'Java', 'C/C++', 'JavaScript', '英语四级', '英语六级', '高数', '线性代数', '概率论']

const form = ref({ major: '计算机科学与技术', grade: '大三', goal: '考研', basics: ['Python', '英语四级'], target_school: '' })
const loading = ref(false)
const result = ref(null)
const recordId = ref(null)
const isFavorite = ref(false)

async function handleGenerate() {
  loading.value = true
  result.value = null
  try {
    const res = await studyApi.generate(form.value)
    if (res.data.result?.error) {
      ElMessage.error(res.data.result.error)
    } else {
      result.value = res.data.result
      recordId.value = res.data.id
      isFavorite.value = false
    }
  } catch (e) {} finally { loading.value = false }
}

async function handleFavorite() {
  if (!recordId.value) return
  try {
    const res = await favoriteApi.toggle({ type: 'plan', ref_id: recordId.value })
    isFavorite.value = res.data.is_favorite
    ElMessage.success(isFavorite.value ? '已收藏' : '已取消收藏')
  } catch (e) {}
}

function exportResult() {
  if (!result.value) return
  let md = `# 学习规划 - ${form.value.major} · ${form.value.grade} · ${form.value.goal}\n\n`
  md += `> ${result.value.overview}\n\n`
  result.value.phases?.forEach((p, i) => {
    md += `## 阶段${i + 1}：${p.title}（${p.period}）\n\n`
    md += `### 学习任务\n`; p.tasks?.forEach(t => md += `- ${t}\n`)
    md += `\n### 推荐资源\n`; p.resources?.forEach(r => md += `- ${r}\n`); md += `\n`
  })
  if (result.value.daily_plan) md += `## 每日计划\n${result.value.daily_plan}\n\n`
  if (result.value.tips?.length) { md += `## 学习建议\n`; result.value.tips.forEach(t => md += `- ${t}\n`) }
  const blob = new Blob([md], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = `学习规划_${form.value.major}_${form.value.grade}.md`; a.click()
  URL.revokeObjectURL(url); ElMessage.success('导出成功')
}
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 4px; }
.page-desc { color: #64748b; margin-bottom: 20px; font-size: 14px; }
.content-wrapper { display: grid; grid-template-columns: 360px 1fr; gap: 20px; }
.input-panel .el-card { border-radius: 12px; }
.result-card { border-radius: 12px; margin-bottom: 16px; }
.empty-card, .loading-card { border-radius: 12px; }
.loading-animation { text-align: center; padding: 60px 20px; }
.loading-text { color: #4F46E5; margin-top: 16px; font-size: 15px; }
.overview h3 { margin-bottom: 8px; }
.overview p { color: #475569; line-height: 1.8; }
.phase-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.phase-num { background: #4F46E5; color: #fff; padding: 2px 10px; border-radius: 10px; font-size: 12px; font-weight: 600; }
.phase-title { font-weight: 600; font-size: 16px; }
.phase-body h4 { margin: 10px 0 6px; color: #4F46E5; font-size: 14px; }
.phase-body ul { padding-left: 20px; }
.phase-body li { line-height: 1.8; color: #475569; font-size: 14px; }
.daily-plan { color: #475569; line-height: 1.8; white-space: pre-line; }
.tips-list { padding-left: 20px; }
.tips-list li { line-height: 1.8; color: #475569; }
.action-bar { display: flex; gap: 10px; margin-top: 8px; }
@media (max-width: 768px) { .content-wrapper { grid-template-columns: 1fr; } }
</style>
