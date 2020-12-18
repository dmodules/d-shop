import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/fr/commande/',
    name: 'Checkout',
    component: () => import('@/views/Checkout.vue')
  },
  {
    path: '/fr/commande/profil/',
    name: 'Profil',
    component: () => import('@/views/Profil.vue')
  },
  {
    path: '/fr/commande/promocodes/',
    name: 'PromoCodes',
    component: () => import('@/views/PromoCodes.vue')
  },
  {
    path: '/fr/commande/soumission/',
    name: 'Soumission',
    component: () => import('@/views/Soumission.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
