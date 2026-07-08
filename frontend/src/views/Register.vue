<template>
  <div class="register-page">
    <div class="register-card">
      <h1 class="register-card__title">创建账号</h1>
      <p class="register-card__subtitle">加入 LightJourney，开始智能规划旅行</p>

      <el-form ref="formRef" :model="form" :rules="rules" size="large" @submit.prevent="handleRegister">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名（2-20位字母数字下划线）" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码（6-30位）" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" class="register-card__btn" @click="handleRegister">
            注 册
          </el-button>
        </el-form-item>
      </el-form>

      <p class="register-card__link">
        已有账号？<router-link to="/login">去登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
// TODO: P3 实现 — 注册逻辑
import { ref, reactive } from 'vue'

const form = reactive({ username: '', password: '', confirmPassword: '' })
const loading = ref(false)

const validateConfirm = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]{2,20}$/, message: '2-20位字母、数字或下划线', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 30, message: '密码长度为6-30位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' },
  ],
}

const handleRegister = async () => {
  // TODO: P3 实现
}
</script>

<style scoped>
.register-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.register-card {
  width: 380px;
  padding: var(--spacing-xl);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}
.register-card__title {
  text-align: center;
  font-size: 24px;
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs);
}
.register-card__subtitle {
  text-align: center;
  font-size: var(--font-size-md);
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-lg);
}
.register-card__btn {
  width: 100%;
  background-color: var(--color-accent);
  border-color: var(--color-accent);
}
.register-card__link {
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}
.register-card__link a {
  color: var(--color-accent);
}
</style>
