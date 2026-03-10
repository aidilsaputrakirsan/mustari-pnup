import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.optimized.js'

import { initPerformanceTracker } from '../../src/services/PerformanceTracker.js'

initPerformanceTracker('Company Profile - Optimized')

const app = createApp(App)
app.use(router)

router.isReady().then(() => {
    app.mount('#app')
})
