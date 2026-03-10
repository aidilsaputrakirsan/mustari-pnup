import { createRouter, createWebHashHistory } from 'vue-router'

// EAGER LOADING DENGAN SENGAJA UNTUK BASELINE
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ServicesView from '../views/ServicesView.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/', name: 'home', component: HomeView },
        { path: '/tentang', name: 'about', component: AboutView },
        { path: '/layanan', name: 'services', component: ServicesView }
    ]
})

export default router
