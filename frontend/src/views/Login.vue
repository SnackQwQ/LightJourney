<template>
  <div class="login-page">
    <div class="login-card">
      <h1 class="login-card__title">LightJourney</h1>
      <p class="login-card__subtitle">AI 驱动的旅行行程管理</p>

      <el-form ref="formRef" :model="form" :rules="rules" size="large" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" class="login-card__btn" @click="handleLogin">
            登 录
          </el-button>
        </el-form-item>
      </el-form>

      <p class="login-card__link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
// TODO: P3 实现 — 登录逻辑（调用 api/auth.js → store → 跳转）
import { ref, reactive } from 'vue'

const form = reactive({ username: '', password: '' })
const loading = ref(false)

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const handleLogin = async () => {
  // TODO: P3 实现
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.login-card {
  width: 380px;
  padding: var(--spacing-xl);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}
.login-card__title {
  text-align: center;
  font-size: 24px;
  font-weight: var(--font-weight-medium);
  color: var(--color-accent);
  margin: 0 0 var(--spacing-xs);
}
.login-card__subtitle {
  text-align: center;
  font-size: var(--font-size-md);
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-lg);
}
.login-card__btn {
  width: 100%;
  background-color: var(--color-accent);
  border-color: var(--color-accent);
}
.login-card__link {
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}
.login-card__link a {
  color: var(--color-accent);
}
</style>
