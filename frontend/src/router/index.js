import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('../views/Home.vue') },
      { path: 'study', name: 'StudyPlan', component: () => import('../views/StudyPlan.vue') },
      { path: 'competition', name: 'Competition', component: () => import('../views/Competition.vue') },
      { path: 'project', name: 'ProjectGen', component: () => import('../views/ProjectGen.vue') },
      { path: 'favorites', name: 'Favorites', component: () => import('../views/Favorites.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
