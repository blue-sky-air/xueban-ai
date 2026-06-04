import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000,
})

// 请求拦截器
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器
api.interceptors.response.use(
  res => res.data,
  err => {
    const status = err.response?.status
    const msg = err.response?.data?.detail || err.message || '请求失败'
    if (status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else if (status === 500) {
      ElMessage.error('服务端错误：' + msg)
    } else if (err.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，AI服务响应较慢，请稍后重试')
    } else {
      ElMessage.error(msg)
    }
    return Promise.reject(err)
  }
)

// 认证
export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  guest: () => api.post('/auth/guest'),
  me: () => api.get('/auth/me'),
}

// 学习规划
export const studyApi = {
  generate: (data) => api.post('/study/generate', data),
  history: () => api.get('/study/history'),
  detail: (id) => api.get(`/study/${id}`),
}

// 竞赛辅导
export const competitionApi = {
  list: () => api.get('/competition/list'),
  generate: (data) => api.post('/competition/generate', data),
  history: () => api.get('/competition/history'),
}

// 项目生成
export const projectApi = {
  directions: () => api.get('/project/directions'),
  generate: (data) => api.post('/project/generate', data),
  regenerateStep: (data) => api.post('/project/regenerate-step', data),
  history: () => api.get('/project/history'),
  detail: (id) => api.get(`/project/${id}`),
}

// 收藏
export const favoriteApi = {
  toggle: (data) => api.post('/favorite/toggle', data),
  list: () => api.get('/favorite/list'),
}

export default api
