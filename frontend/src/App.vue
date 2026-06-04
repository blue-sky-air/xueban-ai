<template>
  <div id="app">
    <router-view v-slot="{ Component, route }">
      <transition name="page" mode="out-in">
        <component :is="Component" :key="route.path" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'PingFang SC', 'Microsoft YaHei', -apple-system, sans-serif;
  background: #f0f2f5;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
}
#app { min-height: 100vh; }

/* 页面切换动画 */
.page-enter-active {
  animation: pageIn 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.page-leave-active {
  animation: pageOut 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes pageIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes pageOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-8px); }
}
</style>
