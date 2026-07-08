<template>
  <el-dialog
    :model-value="visible"
    :title="isEdit ? '编辑行程' : '新建行程'"
    width="520px"
    :close-on-click-modal="false"
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="城市" prop="city">
        <el-input v-model="form.city" placeholder="如：成都" />
      </el-form-item>
      <el-form-item label="日期" prop="date">
        <el-date-picker
          v-model="form.date"
          type="date"
          placeholder="选择日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 100%"
        />
      </el-form-item>
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="开始" prop="start_time">
            <el-time-picker
              v-model="form.start_time"
              placeholder="开始时间"
              format="HH:mm"
              value-format="HH:mm"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="结束" prop="end_time">
            <el-time-picker
              v-model="form.end_time"
              placeholder="结束时间"
              format="HH:mm"
              value-format="HH:mm"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="行程标题" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="form.description" type="textarea" :rows="3" placeholder="行程描述（选填）" />
      </el-form-item>
      <el-form-item label="预算">
        <el-input-number v-model="form.budget" :min="0" :precision="2" :step="10" placeholder="预算（元）" style="width: 100%" />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
// TODO: P4 实现 — 表单提交逻辑（新建 / 编辑），调用 api/trips.js
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  trip: { type: Object, default: null },  // 编辑时传入
})

const emit = defineEmits(['update:visible', 'saved'])

const isEdit = ref(false)
const loading = ref(false)
const formRef = ref(null)

const form = reactive({
  city: '',
  date: '',
  start_time: '',
  end_time: '',
  title: '',
  description: '',
  budget: 0,
})

const rules = {
  city: [{ required: true, message: '请输入城市', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  start_time: [{ required: true, message: '请选择开始时间', trigger: 'change' }],
  end_time: [{ required: true, message: '请选择结束时间', trigger: 'change' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
}

watch(() => props.visible, (val) => {
  if (val && props.trip) {
    isEdit.value = true
    Object.assign(form, props.trip)
  } else if (val) {
    isEdit.value = false
    formRef.value?.resetFields()
  }
})

const handleSubmit = async () => {
  // TODO: P4 实现
}
</script>
