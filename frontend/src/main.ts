import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { useViewModeStore } from './stores/viewMode'
import './styles/global.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

// Hydrate auth before router guard runs
const auth = useAuthStore()
auth.initFromStorage()

// Initialize view mode from cookie
const viewMode = useViewModeStore()
viewMode.initFromCookie()

app.use(router)
app.mount('#app')
