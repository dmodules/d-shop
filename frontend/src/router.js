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
    path: '/fr/commande/password/:action/:uidb64/:token',
    component: () => import('@/views/Password.vue')
  },
  {
    path: '/fr/commande/password/:action',
    name: 'Password',
    component: () => import('@/views/Password.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
