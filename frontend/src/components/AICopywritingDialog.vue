<template>
  <el-dialog
    :model-value="visible"
    title="生成分享文案"
    width="520px"
    :close-on-click-modal="false"
    @update:model-value="$emit('update:visible', $event)"
  >
    <div v-if="loading" class="copywriting-loading">
      <el-skeleton :rows="4" animated />
    </div>

    <div v-else-if="copywritingText" class="copywriting-result">
      <div class="copywriting-result__trip-info">
        <el-tag size="small">{{ tripTitle }}</el-tag>
        <span class="copywriting-result__date">{{ tripDate }}</span>
      </div>
      <el-input
        v-model="copywritingText"
        type="textarea"
        :rows="6"
        class="copywriting-result__textarea"
      />
      <div class="copywriting-result__actions">
        <el-button type="primary" @click="handleCopy">
          <el-icon><DocumentCopy /></el-icon> 一键复制
        </el-button>
      </div>
    </div>

    <el-empty v-else description="点击生成按钮获取 AI 文案" />
  </el-dialog>
</template>

<script setup>
// TODO: P5 实现 — 调用 /api/ai/copywriting + 剪贴板复制
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  visible: { type: Boolean, default: false },
  trip: { type: Object, default: null },
})

const emit = defineEmits(['update:visible'])

const loading = ref(false)
const copywritingText = ref('')
const tripTitle = ref('')
const tripDate = ref('')

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(copywritingText.value)
    ElMessage.success('已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败，请手动选择文字')
  }
}
</script>

<style scoped>
.copywriting-loading {
  padding: var(--spacing-lg) 0;
}
.copywriting-result__trip-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}
.copywriting-result__date {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}
.copywriting-result__textarea {
  margin-bottom: var(--spacing-md);
}
.copywriting-result__actions {
  display: flex;
  justify-content: flex-end;
}
</style>
