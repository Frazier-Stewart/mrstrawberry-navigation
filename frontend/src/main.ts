import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import './styles/global.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

// Hydrate auth before router guard runs
const auth = useAuthStore()
auth.initFromStorage()

app.use(router)
app.mount('#app')
