import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const COOKIE_KEY = 'view_mode'
const COOKIE_MAX_AGE = 365 * 24 * 60 * 60 // 1 year

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return match ? decodeURIComponent(match[2]) : null
}

function setCookie(name: string, value: string, maxAge: number) {
  document.cookie = `${name}=${encodeURIComponent(value)};max-age=${maxAge};path=/;SameSite=Lax`
}

export const useViewModeStore = defineStore('viewMode', () => {
  // 'normal' | 'compact'
  const mode = ref<'normal' | 'compact'>('normal')

  const isCompact = computed(() => mode.value === 'compact')
  const isNormal = computed(() => mode.value === 'normal')

  function initFromCookie() {
    const saved = getCookie(COOKIE_KEY)
    if (saved === 'compact' || saved === 'normal') {
      mode.value = saved
    }
  }

  function setCompact() {
    mode.value = 'compact'
    setCookie(COOKIE_KEY, 'compact', COOKIE_MAX_AGE)
  }

  function setNormal() {
    mode.value = 'normal'
    setCookie(COOKIE_KEY, 'normal', COOKIE_MAX_AGE)
  }

  function toggle() {
    if (mode.value === 'normal') {
      setCompact()
    } else {
      setNormal()
    }
  }

  return {
    mode,
    isCompact,
    isNormal,
    initFromCookie,
    setCompact,
    setNormal,
    toggle,
  }
})
