<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-card__title">找回密码</h1>
      <p class="auth-card__sub">输入注册邮箱，我们将发送重置链接</p>

      <form v-if="!sent" @submit.prevent="handleSubmit" class="auth-form">
        <BaseInput label="邮箱" v-model="email" type="email" placeholder="your@email.com" :error="errors.email" />
        <div v-if="serverError" class="auth-form__error">{{ serverError }}</div>
        <BaseButton type="submit" :loading="loading" :full="true">发送重置邮件</BaseButton>
      </form>

      <div v-else class="auth-form__success">
        <p>重置邮件已发送，请检查您的邮箱（包括垃圾邮件）。</p>
        <p style="margin-top: 8px; font-size: 12px; color: var(--color-placeholder)">链接有效期 1 小时</p>
      </div>

      <div class="auth-links">
        <RouterLink to="/login" class="auth-link">返回登录</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authApi } from '@/api/auth'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'

const email = ref('')
const loading = ref(false)
const sent = ref(false)
const serverError = ref('')
const errors = ref({ email: '' })

async function handleSubmit() {
  errors.value.email = ''
  serverError.value = ''
  if (!email.value) { errors.value.email = '请输入邮箱'; return }

  loading.value = true
  try {
    await authApi.forgotPassword(email.value)
    sent.value = true
  } catch {
    serverError.value = '发送失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface-alt);
  padding: 24px;
}

.auth-card {
  background: var(--color-surface);
  width: 100%;
  max-width: 400px;
  padding: 48px 40px;
  border-radius: var(--radius-card);
}

.auth-card__title {
  font-size: 28px;
  font-weight: 500;
  color: var(--color-heading);
  margin-bottom: 8px;
}

.auth-card__sub {
  font-size: 14px;
  color: var(--color-tertiary);
  margin-bottom: 32px;
}

.auth-form { display: flex; flex-direction: column; gap: 20px; }

.auth-form__error {
  font-size: 13px;
  color: var(--color-error);
  padding: 10px 12px;
  background: #ffeaea;
  border-radius: var(--radius-btn);
}

.auth-form__success {
  font-size: 14px;
  color: #2e7d32;
  padding: 16px;
  background: #e8f5e9;
  border-radius: var(--radius-btn);
  line-height: 1.6;
}

.auth-links { margin-top: 24px; }
.auth-link {
  font-size: 13px;
  color: var(--color-tertiary);
  transition: color var(--transition);
}
.auth-link:hover { color: var(--color-primary); }
</style>
