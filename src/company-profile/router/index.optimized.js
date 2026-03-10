import { createRouter, createWebHashHistory } from 'vue-router'

// HYBRID LAZY LOADING UNTUK OPTIMIZED
const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/HomeView.vue')
        },
        {
            path: '/tentang',
            name: 'about',
            // Manual Chunks
            component: () => import('../views/AboutView.vue')
        },
        {
            path: '/layanan',
            name: 'services',
            component: () => import('../views/ServicesView.vue')
        }
    ]
})

// Prefetching logic (Hybrid Lazy Load) sama seperti SIMTA
router.isReady().then(() => {
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            import('../views/AboutView.vue');
            import('../views/ServicesView.vue');
        });
    } else {
        setTimeout(() => {
            import('../views/AboutView.vue');
            import('../views/ServicesView.vue');
        }, 2000);
    }
});

export default router
