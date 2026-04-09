<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-card__title">登录</h1>
      <p class="auth-card__sub">欢迎回来</p>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <BaseInput label="邮箱" v-model="email" type="email" placeholder="your@email.com" :error="errors.email" />
        <BaseInput label="密码" v-model="password" type="password" placeholder="••••••••" :error="errors.password" />

        <div v-if="serverError" class="auth-form__error">{{ serverError }}</div>

        <BaseButton type="submit" :loading="loading" :full="true">登录</BaseButton>
      </form>

      <div class="auth-links">
        <RouterLink to="/forgot-password" class="auth-link">忘记密码？</RouterLink>
        <RouterLink to="/register" class="auth-link">没有账号？注册</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const serverError = ref('')
const errors = ref({ email: '', password: '' })

async function handleSubmit() {
  errors.value = { email: '', password: '' }
  serverError.value = ''
  if (!email.value) { errors.value.email = '请输入邮箱'; return }
  if (!password.value) { errors.value.password = '请输入密码'; return }

  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (e: any) {
    serverError.value = e.response?.data?.detail ?? '登录失败，请重试'
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

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.auth-form__error {
  font-size: 13px;
  color: var(--color-error);
  padding: 10px 12px;
  background: #ffeaea;
  border-radius: var(--radius-btn);
}

.auth-links {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
}

.auth-link {
  font-size: 13px;
  color: var(--color-tertiary);
  transition: color var(--transition);
}
.auth-link:hover { color: var(--color-primary); }
</style>
