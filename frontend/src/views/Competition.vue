<template>
  <div class="competition">
    <h2 class="page-title">🏆 AI竞赛辅导</h2>
    <p class="page-desc">选择竞赛类型，获取专业备赛方案和学习资源</p>

    <div class="content-wrapper">
      <div class="input-panel">
        <el-card shadow="never">
          <template #header><span style="font-weight:600">⚙️ 竞赛配置</span></template>
          <div class="quick-select">
            <p class="label">快速选择竞赛：</p>
            <div class="tags">
              <el-tag v-for="c in competitions.slice(0, 8)" :key="c.name"
                      :type="form.competition === c.name ? '' : 'info'"
                      @click="form.competition = c.name" class="clickable-tag">
                {{ c.name.length > 10 ? c.name.slice(0, 10) + '...' : c.name }}
              </el-tag>
            </div>
          </div>
          <el-form label-position="top" style="margin-top: 16px;">
            <el-form-item label="竞赛名称">
              <el-input v-model="form.competition" placeholder="输入或选择竞赛名称" />
            </el-form-item>
            <el-form-item label="参赛角色">
              <el-radio-group v-model="form.role">
                <el-radio-button value="队长">队长</el-radio-button>
                <el-radio-button value="队员">队员</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="距离比赛">
              <el-select v-model="form.time_remaining" style="width:100%">
                <el-option label="1个月" value="1个月" />
                <el-option label="3个月" value="3个月" />
                <el-option label="6个月" value="6个月" />
                <el-option label="1年" value="1年" />
              </el-select>
            </el-form-item>
            <el-form-item label="当前水平">
              <el-radio-group v-model="form.level">
                <el-radio-button value="零基础">零基础</el-radio-button>
                <el-radio-button value="入门">入门</el-radio-button>
                <el-radio-button value="有经验">有经验</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-button type="primary" size="large" :loading="loading" @click="handleGenerate" style="width:100%">
              {{ loading ? '生成中...' : '🎯 生成备赛方案' }}
            </el-button>
          </el-form>
        </el-card>
      </div>

      <div class="result-panel">
        <el-card v-if="!result && !loading" shadow="never" class="empty-card">
          <el-empty description="选择竞赛并配置参数后，AI将为你生成详细备赛方案" />
        </el-card>

        <el-card v-if="loading" shadow="never" class="loading-card">
          <div class="loading-animation">
            <el-icon class="is-loading" :size="40" color="#f5576c"><Loading /></el-icon>
            <p class="loading-text">AI正在生成中，请稍候...</p>
          </div>
        </el-card>

        <template v-if="result && !loading">
          <el-card shadow="never" class="result-card">
            <h3>🏆 {{ form.competition }}</h3>
            <p class="intro-text">{{ result.intro }}</p>
          </el-card>

          <el-card shadow="never" class="result-card">
            <h3>📅 备赛时间线</h3>
            <el-timeline>
              <el-timeline-item v-for="(phase, i) in result.timeline" :key="i"
                                :timestamp="phase.period" placement="top" :color="['#4F46E5','#10B981','#F59E0B','#EF4444'][i % 4]">
                <el-card shadow="hover" class="timeline-card">
                  <h4>{{ phase.title }}</h4>
                  <ul><li v-for="(t, j) in phase.tasks" :key="j">{{ t }}</li></ul>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-card>

          <el-card v-if="result.resources?.length" shadow="never" class="result-card">
            <h3>📖 推荐学习资源</h3>
            <div class="resource-grid">
              <div v-for="(r, i) in result.resources" :key="i" class="resource-item">
                <el-tag :type="['','success','warning','info','danger'][i % 5]" size="small">{{ r.type }}</el-tag>
                <span class="resource-name">{{ r.name }}</span>
                <span class="resource-desc">{{ r.desc }}</span>
              </div>
            </div>
          </el-card>

          <el-card v-if="result.tips?.length" shadow="never" class="result-card">
            <h3>💡 获奖技巧</h3>
            <ul class="tips-list"><li v-for="(t, i) in result.tips" :key="i">{{ t }}</li></ul>
          </el-card>

          <el-card v-if="result.team_advice" shadow="never" class="result-card">
            <h3>👥 组队建议</h3>
            <p class="team-text">{{ result.team_advice }}</p>
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
import { ref, onMounted } from 'vue'
import { competitionApi, favoriteApi } from '../api'
import { ElMessage } from 'element-plus'

const competitions = ref([])
const form = ref({ competition: '全国大学生数学建模竞赛', role: '队员', time_remaining: '3个月', level: '入门' })
const loading = ref(false)
const result = ref(null)
const recordId = ref(null)
const isFavorite = ref(false)

onMounted(async () => { try { const res = await competitionApi.list(); competitions.value = res.data } catch (e) {} })

async function handleGenerate() {
  if (!form.value.competition) { ElMessage.warning('请选择或输入竞赛名称'); return }
  loading.value = true; result.value = null
  try {
    const res = await competitionApi.generate(form.value)
    if (res.data.result?.error) {
      ElMessage.error(res.data.result.error)
    } else {
      result.value = res.data.result; recordId.value = res.data.id; isFavorite.value = false
    }
  } catch (e) {} finally { loading.value = false }
}

async function handleFavorite() {
  if (!recordId.value) return
  try { const res = await favoriteApi.toggle({ type: 'competition', ref_id: recordId.value }); isFavorite.value = res.data.is_favorite; ElMessage.success(isFavorite.value ? '已收藏' : '已取消收藏') } catch (e) {}
}

function exportResult() {
  if (!result.value) return
  let md = `# 竞赛备赛方案 - ${form.value.competition}\n\n> ${result.value.intro}\n\n## 备赛时间线\n\n`
  result.value.timeline?.forEach(p => { md += `### ${p.title}（${p.period}）\n`; p.tasks?.forEach(t => md += `- ${t}\n`); md += `\n` })
  if (result.value.resources?.length) { md += `## 推荐资源\n`; result.value.resources.forEach(r => md += `- **${r.type}** ${r.name}：${r.desc}\n`); md += `\n` }
  if (result.value.tips?.length) { md += `## 获奖技巧\n`; result.value.tips.forEach(t => md += `- ${t}\n`); md += `\n` }
  if (result.value.team_advice) md += `## 组队建议\n${result.value.team_advice}\n`
  const blob = new Blob([md], { type: 'text/markdown' }); const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = `竞赛备赛_${form.value.competition}.md`; a.click()
  URL.revokeObjectURL(url); ElMessage.success('导出成功')
}
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 4px; }
.page-desc { color: #64748b; margin-bottom: 20px; font-size: 14px; }
.content-wrapper { display: grid; grid-template-columns: 360px 1fr; gap: 20px; }
.input-panel .el-card { border-radius: 12px; }
.result-card { border-radius: 12px; margin-bottom: 16px; }
.result-card h3 { margin-bottom: 12px; }
.quick-select { margin-bottom: 8px; }
.quick-select .label { font-size: 13px; color: #64748b; margin-bottom: 8px; }
.tags { display: flex; flex-wrap: wrap; gap: 6px; }
.clickable-tag { cursor: pointer; transition: all 0.2s; }
.clickable-tag:hover { transform: scale(1.05); }
.loading-animation { text-align: center; padding: 60px 20px; }
.loading-text { color: #f5576c; margin-top: 16px; font-size: 15px; }
.intro-text { color: #475569; line-height: 1.8; }
.timeline-card { margin-top: 8px; }
.timeline-card h4 { margin-bottom: 8px; color: #1e293b; }
.timeline-card ul { padding-left: 20px; }
.timeline-card li { line-height: 1.8; color: #475569; font-size: 14px; }
.resource-grid { display: flex; flex-direction: column; gap: 10px; }
.resource-item { display: flex; align-items: center; gap: 10px; }
.resource-name { font-weight: 500; }
.resource-desc { color: #64748b; font-size: 13px; }
.tips-list { padding-left: 20px; }
.tips-list li { line-height: 1.8; color: #475569; }
.team-text { color: #475569; line-height: 1.8; }
.action-bar { display: flex; gap: 10px; margin-top: 8px; }
@media (max-width: 768px) { .content-wrapper { grid-template-columns: 1fr; } }
</style>
