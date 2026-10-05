<template>
  <view class="container">
    <view class="header">
      <text class="title">🇰🇷🇨🇳 韩到中 Demand Posts</text>
      <text class="subtitle">韩国潮牌/美妆/Popup 实时需求列表</text>
    </view>

    <!-- 로딩 상태 -->
    <view v-if="loading" class="loading">
      <text>Data loading from FastAPI...</text>
    </view>

    <!-- 에러 상태 -->
    <view v-else-if="error" class="error">
      <text>{{ error }}</text>
    </view>

    <!-- Demand Posts 리스트 카드 -->
    <view v-else class="post-list">
      <view v-for="post in demands" :key="post.id" class="post-card">
        <view class="card-header">
          <text class="tag">{{ post.category }}</text>
          <text class="status">{{ post.status }}</text>
        </view>
        <text class="post-title">{{ post.title }}</text>
        <text class="post-desc" v-if="post.description">{{ post.description }}</text>
        <view class="card-footer">
          <text class="price">₩ {{ post.target_price_krw.toLocaleString() }}</text>
        </view>
      </view>

      <view v-if="demands.length === 0" class="empty">
        <text>尚未发布任何需求贴 (Swagger UI 에서 POST 테스트 해보세요!)</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchDemands, type DemandPost } from '../../api/demands'

const demands = ref<DemandPost[]>([])
const loading = ref<boolean>(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    demands.value = await fetchDemands()
  } catch (err) {
    error.value = 'FastAPI 로부터 데이터를 불러오는데 실패했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.container {
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}
.header {
  margin-bottom: 20px;
}
.title {
  font-size: 20px;
  font-weight: bold;
  color: #1a1a1a;
  display: block;
}
.subtitle {
  font-size: 13px;
  color: #666;
  margin-top: 4px;
  display: block;
}
.loading, .error, .empty {
  text-align: center;
  padding: 30px;
  color: #888;
}
.post-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.post-card {
  background: #ffffff;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}
.tag {
  background: #eef2ff;
  color: #4f46e5;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}
.status {
  font-size: 11px;
  color: #059669;
}
.post-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  display: block;
  margin-bottom: 6px;
}
.post-desc {
  font-size: 13px;
  color: #4b5563;
  display: block;
  margin-bottom: 10px;
}
.card-footer {
  text-align: right;
}
.price {
  font-size: 16px;
  font-weight: bold;
  color: #e11d48;
}
</style>