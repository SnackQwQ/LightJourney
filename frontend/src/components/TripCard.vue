<template>
  <div class="trip-card">
    <div class="trip-card__time">
      <span class="trip-card__time-text">{{ trip.start_time }} - {{ trip.end_time }}</span>
    </div>
    <div class="trip-card__body">
      <div class="trip-card__header">
        <el-tag size="small" type="info">{{ trip.city }}</el-tag>
        <h3 class="trip-card__title">{{ trip.title }}</h3>
      </div>
      <p class="trip-card__desc" v-if="trip.description">{{ trip.description }}</p>
      <div class="trip-card__footer">
        <span class="trip-card__budget" v-if="trip.budget > 0">¥{{ trip.budget }}</span>
        <div class="trip-card__actions">
          <el-button text size="small" @click="$emit('edit', trip)">编辑</el-button>
          <el-button text size="small" type="primary" @click="$emit('copywriting', trip)">生成文案</el-button>
          <el-button text size="small" type="danger" @click="$emit('delete', trip)">删除</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

defineEmits(['edit', 'delete', 'copywriting'])
</script>

<style scoped>
.trip-card {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  transition: var(--transition-fast);
}
.trip-card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}
.trip-card__time {
  min-width: 100px;
  text-align: center;
}
.trip-card__time-text {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}
.trip-card__body {
  flex: 1;
}
.trip-card__header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
}
.trip-card__title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
}
.trip-card__desc {
  margin: var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.5;
}
.trip-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: var(--spacing-xs);
}
.trip-card__budget {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-accent);
}
.trip-card__actions {
  display: flex;
  gap: var(--spacing-xs);
  opacity: 0;
  transition: var(--transition-fast);
}
.trip-card:hover .trip-card__actions {
  opacity: 1;
}
</style>
