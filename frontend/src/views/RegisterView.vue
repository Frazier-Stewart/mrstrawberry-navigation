<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-card__title">注册</h1>
      <p class="auth-card__sub">创建您的导航站账号</p>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <BaseInput label="邮箱" v-model="email" type="email" placeholder="your@email.com" :error="errors.email" />
        <BaseInput label="密码" v-model="password" type="password" placeholder="至少6位" :error="errors.password" />
        <BaseInput label="确认密码" v-model="confirm" type="password" placeholder="再次输入密码" :error="errors.confirm" />

        <div v-if="serverError" class="auth-form__error">{{ serverError }}</div>
        <div v-if="success" class="auth-form__success">注册成功！正在跳转登录...</div>

        <BaseButton type="submit" :loading="loading" :full="true">注册</BaseButton>
      </form>

      <div class="auth-links">
        <RouterLink to="/login" class="auth-link">已有账号？登录</RouterLink>
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
const confirm = ref('')
const loading = ref(false)
const serverError = ref('')
const success = ref(false)
const errors = ref({ email: '', password: '', confirm: '' })

async function handleSubmit() {
  errors.value = { email: '', password: '', confirm: '' }
  serverError.value = ''

  if (!email.value) { errors.value.email = '请输入邮箱'; return }
  if (password.value.length < 6) { errors.value.password = '密码至少6位'; return }
  if (password.value !== confirm.value) { errors.value.confirm = '两次密码不一致'; return }

  loading.value = true
  try {
    await auth.register(email.value, password.value)
    success.value = true
    setTimeout(() => router.push('/login'), 1200)
  } catch (e: any) {
    serverError.value = e.response?.data?.detail ?? '注册失败，请重试'
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

.auth-form__success {
  font-size: 13px;
  color: #2e7d32;
  padding: 10px 12px;
  background: #e8f5e9;
  border-radius: var(--radius-btn);
}

.auth-links {
  margin-top: 24px;
  text-align: center;
}

.auth-link {
  font-size: 13px;
  color: var(--color-tertiary);
  transition: color var(--transition);
}
.auth-link:hover { color: var(--color-primary); }
</style>
