<template>
  <view class="container">
    <view class="header">
      <view class="header-text">
        <text class="title">🇰🇷🇨🇳 韩到中 Demand Posts</text>
        <text class="subtitle">韩国潮牌/美妆/Popup 实时需求列表</text>
      </view>
      <button class="create-button" @click="openForm">发布需求</button>
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
        <text>尚未发布任何需求贴。点击上方「发布需求」，填写标题、分类和目标价格。</text>
      </view>
    </view>

    <view v-if="showForm" class="mask" @click="closeForm">
      <view class="sheet" @click.stop>
        <text class="sheet-title">发布需求</text>

        <text class="label">标题</text>
        <input
          class="field"
          type="text"
          maxlength="255"
          placeholder="例如：弘大 Gentle Monster 限量墨镜"
          :value="form.title"
          @input="onTitleInput"
        />

        <text class="label">分类</text>
        <picker
          mode="selector"
          :range="categoryOptions"
          range-key="label"
          :value="categoryIndex < 0 ? 0 : categoryIndex"
          @change="onCategoryChange"
        >
          <view class="field picker-value">
            {{ selectedCategoryLabel }}
          </view>
        </picker>

        <text class="label">目标价格 (KRW)</text>
        <input
          class="field"
          type="number"
          placeholder="大于 0 的整数"
          :value="form.targetPrice"
          @input="onPriceInput"
        />

        <text class="label">描述（可选）</text>
        <textarea
          class="field textarea"
          maxlength="2000"
          placeholder="尺码、颜色、购买地点等"
          :value="form.description"
          @input="onDescriptionInput"
        />

        <text v-if="formError" class="form-error">{{ formError }}</text>

        <view class="sheet-actions">
          <button class="ghost-button" :disabled="submitting" @click="closeForm">取消</button>
          <button class="submit-button" :disabled="submitting" @click="submitForm">
            {{ submitting ? "发布中..." : "发布" }}
          </button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { createDemand, fetchDemands, type CreateDemandPayload, type DemandPost } from "../../api/demands";

const categoryOptions = [
  { value: "fashion", label: "fashion · 潮牌" },
  { value: "beauty", label: "beauty · 美妆" },
  { value: "popup", label: "popup · Popup" },
] as const;

type Category = CreateDemandPayload["category"];

const demands = ref<DemandPost[]>([]);
const loading = ref<boolean>(true);
const error = ref<string | null>(null);
const showForm = ref(false);
const submitting = ref(false);
const formError = ref<string | null>(null);
const form = ref({
  title: "",
  category: "" as "" | Category,
  targetPrice: "",
  description: "",
});

const categoryIndex = computed(() =>
  categoryOptions.findIndex((item) => item.value === form.value.category)
);
const selectedCategoryLabel = computed(() =>
  categoryIndex.value < 0 ? "请选择分类" : categoryOptions[categoryIndex.value].label
);

onMounted(async () => {
  try {
    await reloadDemands();
  } finally {
    loading.value = false;
  }
});

async function reloadDemands() {
  try {
    demands.value = await fetchDemands();
    error.value = null;
  } catch (err) {
    error.value = "FastAPI 로부터 데이터를 불러오는데 실패했습니다.";
    console.error(err);
    throw err;
  }
}

function openForm() {
  formError.value = null;
  showForm.value = true;
}

function closeForm() {
  if (submitting.value) return;
  showForm.value = false;
  formError.value = null;
}

function resetForm() {
  form.value = { title: "", category: "", targetPrice: "", description: "" };
}

function onTitleInput(event: { detail: { value: string } }) {
  form.value.title = event.detail.value;
}

function onPriceInput(event: { detail: { value: string } }) {
  form.value.targetPrice = event.detail.value;
}

function onDescriptionInput(event: { detail: { value: string } }) {
  form.value.description = event.detail.value;
}

function onCategoryChange(event: { detail: { value: string | number } }) {
  const index = Number(event.detail.value);
  const selected = categoryOptions[index];
  if (selected) {
    form.value.category = selected.value;
  }
}

function validateForm(): string | null {
  const title = form.value.title.trim();
  if (!title || title.length > 255) {
    return "标题需要 1 到 255 个字符";
  }
  if (!form.value.category) {
    return "请选择分类";
  }
  const price = Number(form.value.targetPrice);
  if (!Number.isInteger(price) || price <= 0) {
    return "目标价格需要是大于 0 的整数";
  }
  if (form.value.description.trim().length > 2000) {
    return "描述不能超过 2000 个字符";
  }
  return null;
}

async function submitForm() {
  const message = validateForm();
  if (message) {
    formError.value = message;
    return;
  }
  const category = form.value.category;
  if (!category) {
    formError.value = "请选择分类";
    return;
  }

  submitting.value = true;
  formError.value = null;
  const description = form.value.description.trim();
  try {
    await createDemand({
      title: form.value.title.trim(),
      category,
      target_price_krw: Number(form.value.targetPrice),
      ...(description ? { description } : {}),
    });
  } catch (err) {
    formError.value = err instanceof Error ? err.message : "发布失败";
    return;
  } finally {
    submitting.value = false;
  }

  showForm.value = false;
  formError.value = null;
  resetForm();
  try {
    await reloadDemands();
  } catch {
    // reloadDemands already records the page-level error
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
}
.header-text {
  flex: 1;
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
.create-button,
.submit-button,
.ghost-button {
  margin: 0;
  line-height: 1.2;
  font-size: 14px;
  border-radius: 8px;
}
.create-button,
.submit-button {
  background: #4f46e5;
  color: #ffffff;
}
.create-button {
  padding: 8px 12px;
  flex-shrink: 0;
}
.ghost-button {
  background: #ffffff;
  color: #374151;
  border: 1px solid #d1d5db;
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
.mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: rgba(17, 24, 39, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 20;
}
.sheet {
  width: 100%;
  max-width: 440px;
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-sizing: border-box;
}
.sheet-title {
  display: block;
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}
.label {
  display: block;
  font-size: 13px;
  color: #374151;
  margin-bottom: 6px;
}
.field {
  width: 100%;
  box-sizing: border-box;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0 12px;
  margin-bottom: 14px;
  font-size: 14px;
  color: #111827;
  height: 44px;
  line-height: 44px;
}
.field :deep(.uni-input-wrapper),
.field :deep(.uni-input-input),
.field :deep(.uni-textarea-wrapper),
.field :deep(.uni-textarea-textarea) {
  width: 100%;
  height: 100%;
  font-size: 14px;
}
.picker-value {
  height: 44px;
  line-height: 44px;
}
.textarea {
  height: 96px;
  padding: 10px 12px;
  line-height: 1.5;
}
.form-error {
  display: block;
  color: #be123c;
  font-size: 13px;
  margin-bottom: 12px;
}
.sheet-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
.submit-button,
.ghost-button {
  padding: 8px 16px;
}
</style>
