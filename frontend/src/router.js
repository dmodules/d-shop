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
    path: '/en/commande/',
    component: () => import('@/views/Checkout.vue')
  },
  {
    path: '/fr/commande/devis/',
    name: 'Quotation',
    component: () => import('@/views/Quotation.vue')
  },
  {
    path: '/en/commande/quotation/',
    component: () => import('@/views/Quotation.vue')
  },
  {
    path: '/fr/commande/mes-devis/',
    name: 'QuotationsList',
    component: () => import('@/views/QuotationsList.vue')
  },
  {
    path: '/en/commande/my-quotations/',
    component: () => import('@/views/QuotationsList.vue')
  },
  {
    path: '/fr/commande/mes-devis/:number',
    name: 'QuotationsDetail',
    component: () => import('@/views/QuotationsList.vue')
  },
  {
    path: '/en/commande/my-quotations/:number',
    component: () => import('@/views/QuotationsList.vue')
  },
  {
    path: '/fr/commande/profil/',
    name: 'Profil',
    component: () => import('@/views/Profil.vue')
  },
  {
    path: '/en/commande/profil/',
    component: () => import('@/views/Profil.vue')
  },
  {
    path: '/fr/commande/promocodes/',
    name: 'PromoCodes',
    component: () => import('@/views/PromoCodes.vue')
  },
  {
    path: '/en/commande/promocodes/',
    component: () => import('@/views/PromoCodes.vue')
  },
  {
    path: '/fr/commande/password/:action/:uidb64/:token',
    component: () => import('@/views/Password.vue')
  },
  {
    path: '/en/commande/password/:action/:uidb64/:token',
    component: () => import('@/views/Password.vue')
  },
  {
    path: '/fr/commande/password/:action',
    name: 'Password',
    component: () => import('@/views/Password.vue')
  },
  {
    path: '/en/commande/password/:action',
    component: () => import('@/views/Password.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
