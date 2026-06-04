<template>
  <div class="project-gen">
    <h2 class="page-title">🚀 AI项目生成 <el-tag type="danger" effect="dark">核心功能</el-tag></h2>
    <p class="page-desc">选择项目方向，AI自动生成完整方案：命名 → 简介 → 技术路线 → 商业模式 → 可行性分析</p>

    <div class="content-wrapper">
      <div class="input-panel">
        <el-card shadow="never">
          <template #header><span style="font-weight:600">⚙️ 项目配置</span></template>
          <el-form label-position="top">
            <el-form-item label="项目方向">
              <div class="direction-tags">
                <el-tag v-for="d in directions" :key="d" :type="form.direction === d ? '' : 'info'"
                        @click="form.direction = d" class="clickable-tag">{{ d }}</el-tag>
              </div>
              <el-input v-model="form.direction" placeholder="自定义方向" style="margin-top: 8px;" />
            </el-form-item>
            <el-form-item label="项目类型">
              <el-select v-model="form.project_type" style="width:100%">
                <el-option label="课程设计" value="课程设计" />
                <el-option label="毕业设计" value="毕业设计" />
                <el-option label="竞赛项目" value="竞赛项目" />
                <el-option label="创业项目" value="创业项目" />
              </el-select>
            </el-form-item>
            <el-form-item label="技术偏好">
              <el-radio-group v-model="form.tech_preference">
                <el-radio-button value="Web">Web</el-radio-button>
                <el-radio-button value="移动端">移动端</el-radio-button>
                <el-radio-button value="嵌入式">嵌入式</el-radio-button>
                <el-radio-button value="数据分析">数据分析</el-radio-button>
                <el-radio-button value="不限">不限</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="团队规模">
              <el-radio-group v-model="form.team_size">
                <el-radio-button :value="1">1人</el-radio-button>
                <el-radio-button :value="3">2-3人</el-radio-button>
                <el-radio-button :value="5">4-5人</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="特色关键词（可选）">
              <el-input v-model="form.keywords" placeholder="如：边缘计算,知识图谱" />
            </el-form-item>
            <el-button type="primary" size="large" :loading="loading" @click="handleGenerate" style="width:100%">
              {{ loading ? 'AI生成中...' : '🚀 开始生成项目方案' }}
            </el-button>
          </el-form>
        </el-card>
      </div>

      <div class="result-panel">
        <el-card v-if="!result && !loading" shadow="never" class="empty-card">
          <el-empty description="配置项目参数后点击生成，AI将为你构建完整项目方案" />
        </el-card>

        <el-card v-if="loading" shadow="never" class="loading-card">
          <div class="loading-animation">
            <el-icon class="is-loading" :size="40" color="#4F46E5"><Loading /></el-icon>
            <p class="loading-text">AI正在生成完整项目方案，请稍候...</p>
          </div>
        </el-card>

        <template v-if="result && !loading">
          <!-- Step 1: 项目命名 -->
          <el-card shadow="never" class="result-card step-card">
            <div class="step-header">
              <span class="step-badge">1</span>
              <h3>💡 项目命名</h3>
              <el-button size="small" text @click="regenerate('name')">🔄 重新命名</el-button>
            </div>
            <div class="project-name-box">
              <h2>「{{ result.project_name }}」</h2>
              <p class="subtitle" v-if="result.subtitle">{{ result.subtitle }}</p>
            </div>
            <p v-if="result.naming?.reasoning" class="reasoning"><strong>命名逻辑：</strong>{{ result.naming.reasoning }}</p>
          </el-card>

          <!-- Step 2: 项目简介 -->
          <el-card shadow="never" class="result-card step-card">
            <div class="step-header">
              <span class="step-badge">2</span>
              <h3>📝 项目简介</h3>
              <el-button size="small" text @click="regenerate('summary')">🔄 重新生成</el-button>
            </div>
            <template v-if="result.summary">
              <div class="summary-section"><h4>📋 项目背景</h4><p>{{ result.summary.background }}</p></div>
              <div class="summary-section"><h4>❗ 痛点分析</h4><ul><li v-for="(p, i) in result.summary.pain_points" :key="i">{{ p }}</li></ul></div>
              <div class="summary-section"><h4>✅ 解决方案</h4><p>{{ result.summary.solution }}</p></div>
              <div class="summary-section"><h4>⭐ 核心创新点</h4><ul><li v-for="(inn, i) in result.summary.innovations" :key="i">{{ inn }}</li></ul></div>
            </template>
          </el-card>

          <!-- Step 3: 技术路线 -->
          <el-card shadow="never" class="result-card step-card">
            <div class="step-header">
              <span class="step-badge">3</span>
              <h3>🛠️ 技术路线</h3>
              <el-button size="small" text @click="regenerate('tech_route')">🔄 重新生成</el-button>
            </div>
            <template v-if="result.tech_route">
              <div class="tech-stack">
                <div class="stack-item" v-for="(val, key) in result.tech_route.tech_stack" :key="key">
                  <span class="stack-label">{{ {frontend:'前端',backend:'后端',ai:'AI/模型',database:'数据库',other:'其他'}[key] || key }}</span>
                  <span class="stack-value">{{ val }}</span>
                </div>
              </div>
              <div class="summary-section" v-if="result.tech_route.architecture"><h4>🏗️ 架构描述</h4><p>{{ result.tech_route.architecture }}</p></div>
              <div class="summary-section" v-if="result.tech_route.phases?.length">
                <h4>📅 开发阶段</h4>
                <div v-for="(phase, i) in result.tech_route.phases" :key="i" class="tech-phase">
                  <el-tag size="small" type="info">{{ phase.duration }}</el-tag>
                  <strong>{{ phase.name }}</strong>
                  <ul><li v-for="(t, j) in phase.tasks" :key="j">{{ t }}</li></ul>
                </div>
              </div>
            </template>
          </el-card>

          <!-- Step 4: 商业模式 -->
          <el-card shadow="never" class="result-card step-card">
            <div class="step-header">
              <span class="step-badge">4</span>
              <h3>💰 商业模式</h3>
              <el-button size="small" text @click="regenerate('business_model')">🔄 重新生成</el-button>
            </div>
            <template v-if="result.business_model">
              <div class="summary-section"><h4>💎 价值主张</h4><p class="highlight-text">{{ result.business_model.value_proposition }}</p></div>
              <div class="summary-section"><h4>👥 目标用户</h4><el-tag v-for="s in result.business_model.customer_segments" :key="s" style="margin: 4px;">{{ s }}</el-tag></div>
              <div class="summary-section"><h4>💵 收入来源</h4><div v-for="(r, i) in result.business_model.revenue_streams" :key="i" class="revenue-item"><strong>{{ r.name }}</strong>：{{ r.desc }}</div></div>
              <div class="summary-section"><h4>🏆 竞争优势</h4><ul><li v-for="(a, i) in result.business_model.competitive_advantage" :key="i">{{ a }}</li></ul></div>
            </template>
          </el-card>

          <!-- Step 5: 可行性分析 -->
          <el-card shadow="never" class="result-card step-card">
            <div class="step-header">
              <span class="step-badge">5</span>
              <h3>📊 可行性分析</h3>
              <el-button size="small" text @click="regenerate('feasibility')">🔄 重新生成</el-button>
            </div>
            <template v-if="result.feasibility">
              <div class="score-grid">
                <div v-for="(val, key) in result.feasibility.scores" :key="key" class="score-item">
                  <div class="score-label">{{ {technical:'技术可行性',market:'市场可行性',team:'团队可行性',business:'商业可行性'}[key] || key }}</div>
                  <el-rate :model-value="val.score" disabled show-score />
                  <p class="score-reason">{{ val.reason }}</p>
                </div>
              </div>
              <div class="summary-section" v-if="result.feasibility.overall_score">
                <h4>综合评分</h4>
                <el-progress :percentage="result.feasibility.overall_score * 20" :stroke-width="20" :color="result.feasibility.overall_score >= 4 ? '#10B981' : '#F59E0B'" />
              </div>
              <div class="summary-section" v-if="result.feasibility.risks?.length">
                <h4>⚠️ 风险与应对</h4>
                <el-table :data="result.feasibility.risks" border size="small">
                  <el-table-column prop="risk" label="风险" />
                  <el-table-column prop="mitigation" label="应对策略" />
                </el-table>
              </div>
              <div class="summary-section" v-if="result.feasibility.suggestion"><h4>💡 总体建议</h4><p>{{ result.feasibility.suggestion }}</p></div>
            </template>
          </el-card>

          <div class="action-bar">
            <el-button @click="handleFavorite" :type="isFavorite ? 'warning' : 'default'" size="large">
              {{ isFavorite ? '⭐ 已收藏' : '☆ 收藏' }}
            </el-button>
            <el-button @click="exportResult" type="primary" size="large">📥 导出完整方案</el-button>
            <el-button @click="resetAll" size="large">🔄 全部重新生成</el-button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { projectApi, favoriteApi } from '../api'
import { ElMessage } from 'element-plus'

const directions = ['AI+医疗', 'AI+教育', 'AI+金融', 'AI+农业', 'AI+环保', 'AI+文旅', 'AI+交通', '智能家居', '物联网', '区块链']
const form = ref({ direction: 'AI+医疗', project_type: '竞赛项目', tech_preference: 'Web', team_size: 3, keywords: '' })
const loading = ref(false)
const result = ref(null)
const recordId = ref(null)
const isFavorite = ref(false)

async function handleGenerate() {
  if (!form.value.direction) { ElMessage.warning('请选择项目方向'); return }
  loading.value = true; result.value = null
  try {
    const res = await projectApi.generate(form.value)
    if (res.data?.error) {
      ElMessage.error(res.data.error)
    } else {
      result.value = res.data; recordId.value = res.data.id; isFavorite.value = false
    }
  } catch (e) {} finally { loading.value = false }
}

async function regenerate(step) {
  if (!recordId.value) return
  ElMessage.info('正在重新生成...')
  try {
    const res = await projectApi.regenerateStep({ project_id: recordId.value, step })
    if (step === 'name') { result.value.project_name = res.data.result.name; result.value.naming = res.data.result }
    else if (step === 'summary') result.value.summary = res.data.result
    else if (step === 'tech_route') result.value.tech_route = res.data.result
    else if (step === 'business_model') result.value.business_model = res.data.result
    else if (step === 'feasibility') result.value.feasibility = res.data.result
    ElMessage.success('重新生成成功')
  } catch (e) {}
}

async function handleFavorite() {
  if (!recordId.value) return
  try { const res = await favoriteApi.toggle({ type: 'project', ref_id: recordId.value }); isFavorite.value = res.data.is_favorite; ElMessage.success(isFavorite.value ? '已收藏' : '已取消收藏') } catch (e) {}
}

function resetAll() { result.value = null; recordId.value = null }

function exportResult() {
  if (!result.value) return
  const r = result.value
  let md = `# ${r.project_name}\n`; if (r.subtitle) md += `> ${r.subtitle}\n`; md += `\n---\n\n`
  md += `## 一、项目简介\n\n`
  if (r.summary) {
    md += `### 项目背景\n${r.summary.background}\n\n### 痛点分析\n${r.summary.pain_points?.map(p => `- ${p}`).join('\n')}\n\n### 解决方案\n${r.summary.solution}\n\n### 核心创新点\n${r.summary.innovations?.map(i => `- ${i}`).join('\n')}\n\n`
  }
  md += `## 二、技术路线\n\n`
  if (r.tech_route) {
    md += `### 技术栈\n`; for (const [k, v] of Object.entries(r.tech_route.tech_stack || {})) md += `- **${k}**：${v}\n`
    md += `\n### 架构\n${r.tech_route.architecture}\n\n`
    r.tech_route.phases?.forEach(p => { md += `### ${p.name}（${p.duration}）\n${p.tasks?.map(t => `- ${t}`).join('\n')}\n\n` })
  }
  md += `## 三、商业模式\n\n`
  if (r.business_model) {
    md += `**价值主张**：${r.business_model.value_proposition}\n\n**目标用户**：${r.business_model.customer_segments?.join('、')}\n\n`
    md += `**收入来源**：\n${r.business_model.revenue_streams?.map(s => `- ${s.name}：${s.desc}`).join('\n')}\n\n`
    md += `**竞争优势**：\n${r.business_model.competitive_advantage?.map(a => `- ${a}`).join('\n')}\n\n`
  }
  md += `## 四、可行性分析\n\n`
  if (r.feasibility) {
    for (const [k, v] of Object.entries(r.feasibility.scores || {})) md += `- **${k}**：${'⭐'.repeat(v.score)} - ${v.reason}\n`
    md += `\n**综合评分**：${r.feasibility.overall_score}/5\n\n`
    if (r.feasibility.risks?.length) { md += `### 风险与应对\n`; r.feasibility.risks.forEach(rk => { md += `- **风险**：${rk.risk} → **应对**：${rk.mitigation}\n` }) }
    md += `\n**建议**：${r.feasibility.suggestion}\n`
  }
  const blob = new Blob([md], { type: 'text/markdown' }); const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = `项目方案_${r.project_name || '未命名'}.md`; a.click()
  URL.revokeObjectURL(url); ElMessage.success('导出成功')
}
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 4px; display: flex; align-items: center; gap: 10px; }
.page-desc { color: #64748b; margin-bottom: 16px; font-size: 14px; }
.content-wrapper { display: grid; grid-template-columns: 360px 1fr; gap: 20px; }
.input-panel .el-card { border-radius: 12px; }
.result-card { border-radius: 12px; margin-bottom: 16px; }
.direction-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.clickable-tag { cursor: pointer; transition: all 0.2s; }
.clickable-tag:hover { transform: scale(1.05); }
.loading-animation { text-align: center; padding: 60px 20px; }
.loading-text { color: #4F46E5; margin-top: 16px; font-size: 15px; }
.step-card { border-left: 4px solid #4F46E5; }
.step-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.step-badge { width: 28px; height: 28px; background: #4F46E5; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.step-header h3 { flex: 1; margin: 0; }
.project-name-box { text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px; margin-bottom: 12px; }
.project-name-box h2 { color: #4F46E5; font-size: 22px; }
.project-name-box .subtitle { color: #64748b; margin-top: 4px; }
.reasoning { color: #475569; font-size: 13px; line-height: 1.6; background: #f1f5f9; padding: 10px; border-radius: 8px; }
.summary-section { margin-bottom: 16px; }
.summary-section h4 { margin-bottom: 6px; color: #4F46E5; font-size: 14px; }
.summary-section p { color: #475569; line-height: 1.8; }
.summary-section ul { padding-left: 20px; }
.summary-section li { line-height: 1.8; color: #475569; }
.tech-stack { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; }
.stack-item { background: #f1f5f9; padding: 8px 14px; border-radius: 8px; }
.stack-label { color: #4F46E5; font-weight: 600; margin-right: 6px; font-size: 13px; }
.stack-value { color: #475569; font-size: 13px; }
.tech-phase { margin-bottom: 10px; }
.tech-phase strong { margin-left: 6px; }
.tech-phase ul { padding-left: 20px; margin-top: 4px; }
.tech-phase li { color: #475569; line-height: 1.6; font-size: 14px; }
.highlight-text { background: linear-gradient(135deg, #667eea20, #764ba220); padding: 12px; border-radius: 8px; font-size: 16px; color: #4F46E5; font-weight: 500; }
.revenue-item { margin-bottom: 6px; color: #475569; }
.score-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.score-item { background: #f8fafc; padding: 12px; border-radius: 10px; }
.score-label { font-weight: 600; margin-bottom: 4px; }
.score-reason { color: #64748b; font-size: 12px; margin-top: 4px; }
.action-bar { display: flex; gap: 10px; margin-top: 8px; }
@media (max-width: 768px) { .content-wrapper { grid-template-columns: 1fr; } .score-grid { grid-template-columns: 1fr; } }
</style>
