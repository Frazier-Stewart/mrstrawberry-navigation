<template>
  <div class="layout">
    <Navbar />

    <div class="page">
      <div class="page__inner">
        <RouterLink to="/" class="back-link">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
            <path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          返回
        </RouterLink>

        <h1 class="page__title">个人中心</h1>

        <!-- 账户信息 -->
        <section class="card">
          <h2 class="card__title">账户信息</h2>
          <div v-if="auth.user" class="info-list">
            <div class="info-row">
              <span class="info-row__label">邮箱</span>
              <span class="info-row__value">{{ auth.user.email }}</span>
            </div>
            <div class="info-row">
              <span class="info-row__label">注册时间</span>
              <span class="info-row__value">{{ formatDate(auth.user.created_at) }}</span>
            </div>
            <div class="info-row">
              <span class="info-row__label">账户状态</span>
              <span class="info-row__value info-row__value--active">正常</span>
            </div>
          </div>
          <div v-else class="info-loading">
            <span class="spinner" />
          </div>
        </section>

        <!-- 修改密码 -->
        <section class="card">
          <h2 class="card__title">修改密码</h2>
          <form @submit.prevent="handleChangePassword" class="form">
            <BaseInput
              label="当前密码"
              v-model="form.oldPassword"
              type="password"
              placeholder="输入当前密码"
              :error="errors.oldPassword"
            />
            <BaseInput
              label="新密码"
              v-model="form.newPassword"
              type="password"
              placeholder="至少6位"
              :error="errors.newPassword"
            />
            <BaseInput
              label="确认新密码"
              v-model="form.confirmPassword"
              type="password"
              placeholder="再次输入新密码"
              :error="errors.confirmPassword"
            />

            <div v-if="serverError" class="form__error">{{ serverError }}</div>
            <div v-if="successMsg" class="form__success">{{ successMsg }}</div>

            <div class="form__footer">
              <BaseButton type="submit" :loading="loading">保存新密码</BaseButton>
            </div>
          </form>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'
import Navbar from '@/components/Navbar.vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'

const auth = useAuthStore()

onMounted(() => {
  if (!auth.user) auth.fetchMe()
})

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
}

// ── Change password ───────────────────────────────────────────────────────────
const form = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const errors = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const loading = ref(false)
const serverError = ref('')
const successMsg = ref('')

async function handleChangePassword() {
  errors.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  serverError.value = ''
  successMsg.value = ''

  if (!form.value.oldPassword) { errors.value.oldPassword = '请输入当前密码'; return }
  if (form.value.newPassword.length < 6) { errors.value.newPassword = '新密码至少6位'; return }
  if (form.value.newPassword !== form.value.confirmPassword) {
    errors.value.confirmPassword = '两次密码不一致'; return
  }

  loading.value = true
  try {
    await authApi.changePassword(form.value.oldPassword, form.value.newPassword)
    successMsg.value = '密码已修改成功'
    form.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  } catch (e: any) {
    serverError.value = e.response?.data?.detail ?? '修改失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-surface-alt);
}

.page {
  flex: 1;
  padding: 40px 24px;
}

.page__inner {
  max-width: 560px;
  margin: 0 auto;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-tertiary);
  margin-bottom: 24px;
  transition: color var(--transition);
}
.back-link:hover { color: var(--color-heading); }

.page__title {
  font-size: 24px;
  font-weight: 500;
  color: var(--color-heading);
  margin-bottom: 24px;
}

.card {
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: 28px 32px;
  margin-bottom: 16px;
}

.card__title {
  font-size: 15px;
  font-weight: 500;
  color: var(--color-heading);
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
}

.info-row__label {
  color: var(--color-tertiary);
}

.info-row__value {
  color: var(--color-heading);
  font-weight: 500;
}

.info-row__value--active {
  color: #2e7d32;
}

.info-loading {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form__error {
  font-size: 13px;
  color: var(--color-error);
  padding: 10px 12px;
  background: #ffeaea;
  border-radius: var(--radius-btn);
}

.form__success {
  font-size: 13px;
  color: #2e7d32;
  padding: 10px 12px;
  background: #e8f5e9;
  border-radius: var(--radius-btn);
}

.form__footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 4px;
}
</style>
