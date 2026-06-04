<template>
  <div class="favorites">
    <h2 class="page-title">⭐ 我的收藏 & 历史记录</h2>

    <el-tabs v-model="activeTab" @tab-change="loadData">
      <el-tab-pane label="收藏" name="favorites" />
      <el-tab-pane label="学习规划" name="plans" />
      <el-tab-pane label="竞赛辅导" name="competitions" />
      <el-tab-pane label="项目生成" name="projects" />
    </el-tabs>

    <!-- 收藏列表 -->
    <template v-if="activeTab === 'favorites'">
      <el-empty v-if="!favorites.length" description="暂无收藏，去各功能页面收藏内容吧" />
      <el-card v-for="f in favorites" :key="f.type + f.id" shadow="hover" class="item-card">
        <div class="item-row">
          <span class="item-icon">{{ {plan:'📚',competition:'🏆',project:'🚀'}[f.type] }}</span>
          <div class="item-info">
            <h4>{{ f.title }}</h4>
            <span class="item-time">{{ f.created_at }}</span>
          </div>
          <el-tag size="small" :type="{plan:'',competition:'warning',project:'success'}[f.type]">
            {{ {plan:'学习规划',competition:'竞赛辅导',project:'项目生成'}[f.type] }}
          </el-tag>
        </div>
      </el-card>
    </template>

    <!-- 学习规划历史 -->
    <template v-if="activeTab === 'plans'">
      <el-empty v-if="!plans.length" description="暂无学习规划记录" />
      <el-card v-for="p in plans" :key="p.id" shadow="hover" class="item-card">
        <div class="item-row">
          <span class="item-icon">📚</span>
          <div class="item-info">
            <h4>{{ p.major }} · {{ p.grade }} · {{ p.goal }}</h4>
            <span class="item-time">{{ p.created_at }}</span>
            <p class="item-preview" v-if="p.result?.overview">{{ p.result.overview }}</p>
          </div>
          <div class="item-actions">
            <el-button size="small" @click="toggleFav('plan', p.id)">{{ p.is_favorite ? '⭐' : '☆' }}</el-button>
          </div>
        </div>
      </el-card>
    </template>

    <!-- 竞赛辅导历史 -->
    <template v-if="activeTab === 'competitions'">
      <el-empty v-if="!competitions.length" description="暂无竞赛辅导记录" />
      <el-card v-for="c in competitions" :key="c.id" shadow="hover" class="item-card">
        <div class="item-row">
          <span class="item-icon">🏆</span>
          <div class="item-info">
            <h4>{{ c.competition }}</h4>
            <span class="item-time">{{ c.created_at }}</span>
            <p class="item-preview" v-if="c.result?.intro">{{ c.result.intro }}</p>
          </div>
          <div class="item-actions">
            <el-button size="small" @click="toggleFav('competition', c.id)">{{ c.is_favorite ? '⭐' : '☆' }}</el-button>
          </div>
        </div>
      </el-card>
    </template>

    <!-- 项目生成历史 -->
    <template v-if="activeTab === 'projects'">
      <el-empty v-if="!projects.length" description="暂无项目生成记录" />
      <el-card v-for="p in projects" :key="p.id" shadow="hover" class="item-card">
        <div class="item-row">
          <span class="item-icon">🚀</span>
          <div class="item-info">
            <h4>{{ p.project_name || p.direction }}</h4>
            <span class="item-time">{{ p.created_at }}</span>
            <el-tag size="small" type="info">{{ p.project_type }}</el-tag>
          </div>
          <div class="item-actions">
            <el-button size="small" @click="toggleFav('project', p.id)">{{ p.is_favorite ? '⭐' : '☆' }}</el-button>
          </div>
        </div>
      </el-card>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { favoriteApi, studyApi, competitionApi, projectApi } from '../api'
import { ElMessage } from 'element-plus'

const activeTab = ref('favorites')
const favorites = ref([])
const plans = ref([])
const competitions = ref([])
const projects = ref([])

onMounted(() => loadData())

async function loadData() {
  try {
    if (activeTab.value === 'favorites') {
      const res = await favoriteApi.list()
      favorites.value = res.data
    } else if (activeTab.value === 'plans') {
      const res = await studyApi.history()
      plans.value = res.data
    } else if (activeTab.value === 'competitions') {
      const res = await competitionApi.history()
      competitions.value = res.data
    } else if (activeTab.value === 'projects') {
      const res = await projectApi.history()
      projects.value = res.data
    }
  } catch (e) {}
}

async function toggleFav(type, id) {
  try {
    const res = await favoriteApi.toggle({ type, ref_id: id })
    ElMessage.success(res.data.is_favorite ? '已收藏' : '已取消收藏')
    loadData()
  } catch (e) {}
}
</script>

<style scoped>
.page-title { font-size: 24px; margin-bottom: 16px; }
.item-card { border-radius: 12px; margin-bottom: 12px; }
.item-row { display: flex; align-items: center; gap: 14px; }
.item-icon { font-size: 32px; }
.item-info { flex: 1; }
.item-info h4 { margin-bottom: 4px; font-size: 15px; }
.item-time { color: #94a3b8; font-size: 12px; }
.item-preview { color: #64748b; font-size: 13px; margin-top: 4px; line-height: 1.5; }
.item-actions { display: flex; gap: 6px; }
</style>
