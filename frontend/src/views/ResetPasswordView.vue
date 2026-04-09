<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-card__title">重置密码</h1>
      <p class="auth-card__sub">设置您的新密码</p>

      <div v-if="!token" class="auth-form__error">链接无效，请重新申请重置密码。</div>

      <form v-else-if="!done" @submit.prevent="handleSubmit" class="auth-form">
        <BaseInput label="新密码" v-model="password" type="password" placeholder="至少6位" :error="errors.password" />
        <BaseInput label="确认新密码" v-model="confirm" type="password" placeholder="再次输入" :error="errors.confirm" />
        <div v-if="serverError" class="auth-form__error">{{ serverError }}</div>
        <BaseButton type="submit" :loading="loading" :full="true">重置密码</BaseButton>
      </form>

      <div v-else class="auth-form__success">
        密码已重置！<RouterLink to="/login" class="auth-link">点击登录</RouterLink>
      </div>

      <div class="auth-links" v-if="!done">
        <RouterLink to="/login" class="auth-link">返回登录</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { authApi } from '@/api/auth'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'

const route = useRoute()
const token = ref((route.query.token as string) || '')
const password = ref('')
const confirm = ref('')
const loading = ref(false)
const done = ref(false)
const serverError = ref('')
const errors = ref({ password: '', confirm: '' })

async function handleSubmit() {
  errors.value = { password: '', confirm: '' }
  serverError.value = ''
  if (password.value.length < 6) { errors.value.password = '密码至少6位'; return }
  if (password.value !== confirm.value) { errors.value.confirm = '两次密码不一致'; return }

  loading.value = true
  try {
    await authApi.resetPassword(token.value, password.value)
    done.value = true
  } catch (e: any) {
    serverError.value = e.response?.data?.detail ?? '重置失败，链接可能已过期'
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
}

.auth-links { margin-top: 24px; }
.auth-link {
  font-size: 13px;
  color: var(--color-primary);
  transition: color var(--transition);
}
</style>
