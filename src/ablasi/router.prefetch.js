/**
 * ROUTER ABLASI - LAZY LOADING + PREFETCHING
 * Sama dengan router.lazy.js, ditambah prefetching saat idle
 * (identik dengan strategi pada router/index.optimized.js).
 */
import router from './router.lazy.js'

function saatIdle(fn) {
    if ('requestIdleCallback' in window) requestIdleCallback(fn)
    else setTimeout(fn, 1000)
}

router.afterEach((to) => {
    if (to.name === 'Dashboard') {
        saatIdle(() => {
            import('../views/DaftarJudulView.vue')
            import('../views/DetailBimbinganView.vue')
        })
    }
    if (to.name === 'DaftarJudul') {
        saatIdle(() => import('../views/DetailBimbinganView.vue'))
    }
})

export default router
