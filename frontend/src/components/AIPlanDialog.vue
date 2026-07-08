<template>
  <el-dialog
    :model-value="visible"
    title="AI 智能规划行程"
    width="720px"
    :close-on-click-modal="false"
    @update:model-value="$emit('update:visible', $event)"
  >
    <!-- 步骤条 -->
    <el-steps :active="step" finish-status="success" align-center class="plan-steps">
      <el-step title="填写参数" />
      <el-step title="预览编辑" />
      <el-step title="确认保存" />
    </el-steps>

    <!-- Step 1: 参数填写 -->
    <div v-if="step === 0" class="plan-step-content">
      <el-form ref="paramFormRef" :model="params" :rules="paramRules" label-width="80px">
        <el-form-item label="目的地" prop="city">
          <el-input v-model="params.city" placeholder="如：成都" />
        </el-form-item>
        <el-form-item label="天数" prop="days">
          <el-input-number v-model="params.days" :min="1" :max="30" />
        </el-form-item>
        <el-form-item label="偏好" prop="preferences">
          <el-checkbox-group v-model="params.preferences">
            <el-checkbox label="美食">美食</el-checkbox>
            <el-checkbox label="自然风光">自然风光</el-checkbox>
            <el-checkbox label="人文历史">人文历史</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="预算上限">
          <el-input-number v-model="params.budget" :min="0" :step="100" placeholder="选填" style="width: 100%" />
        </el-form-item>
      </el-form>
      <div class="plan-step-actions">
        <el-button @click="$emit('update:visible', false)">取消</el-button>
        <el-button type="primary" :loading="generating" @click="handleGenerate">生成行程</el-button>
      </div>
    </div>

    <!-- Step 2: 预览编辑 -->
    <div v-else-if="step === 1" class="plan-step-content">
      <el-empty v-if="plan.length === 0" description="暂无生成的行程" />
      <div v-else class="plan-preview-table">
        <!-- TODO: P5 实现 — 行程预览表格、行展开编辑、冲突标记 -->
        <p class="plan-placeholder">P5 需要实现行程预览表格（展开编辑 + 冲突标记）</p>
      </div>
      <div class="plan-step-actions">
        <el-button @click="step = 0">返回修改</el-button>
        <el-button type="primary" @click="step = 2">下一步：确认保存</el-button>
      </div>
    </div>

    <!-- Step 3: 确认保存 -->
    <div v-else class="plan-step-content">
      <el-empty description="确认保存选中的行程">
        <template #extra>
          <p class="plan-placeholder">P5 需要实现批量保存逻辑 + 保存结果提示</p>
        </template>
      </el-empty>
      <div class="plan-step-actions">
        <el-button @click="step = 1">返回编辑</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">确认保存</el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
// TODO: P5 实现 — AI 规划三步弹窗完整逻辑
import { ref, reactive } from 'vue'

defineProps({
  visible: { type: Boolean, default: false },
})
const emit = defineEmits(['update:visible', 'saved'])

const step = ref(0)
const generating = ref(false)
const saving = ref(false)
const plan = ref([])

const params = reactive({
  city: '',
  days: 3,
  preferences: [],
  budget: null,
})

const paramRules = {
  city: [{ required: true, message: '请输入目的地', trigger: 'blur' }],
  days: [{ required: true, message: '请选择天数', trigger: 'change' }],
  preferences: [
    {
      type: 'array',
      min: 1,
      message: '请至少选择一个偏好',
      trigger: 'change',
    },
  ],
}

const handleGenerate = async () => {
  // TODO: P5 实现 — 调用 /api/ai/plan
}

const handleSave = async () => {
  // TODO: P5 实现 — 批量保存
}
</script>

<style scoped>
.plan-steps {
  margin: var(--spacing-lg) 0;
}
.plan-step-content {
  min-height: 300px;
}
.plan-step-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}
.plan-placeholder {
  text-align: center;
  color: var(--text-secondary);
  font-size: var(--font-size-md);
  padding: var(--spacing-xl) 0;
}
</style>
