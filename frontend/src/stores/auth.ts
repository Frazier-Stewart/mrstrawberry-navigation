import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type UserResponse } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<UserResponse | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  function initFromStorage() {
    const stored = localStorage.getItem('access_token')
    if (stored) token.value = stored
  }

  async function fetchMe() {
    const res = await authApi.getMe()
    user.value = res.data
  }

  async function login(email: string, password: string) {
    const res = await authApi.login(email, password)
    token.value = res.data.access_token
    localStorage.setItem('access_token', res.data.access_token)
  }

  async function register(email: string, password: string) {
    await authApi.register(email, password)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
  }

  return { token, user, isAuthenticated, initFromStorage, fetchMe, login, register, logout }
})
