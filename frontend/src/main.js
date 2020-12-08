/* ================================================================= //
// ===-----------------------------------------------------------=== //
//       PACKAGE: @dmodules/pejan                                    //
//        AUTHOR: D-Modules                                          //
//       CREATED: 2020.07.14                                         //
// ===-----------------------------------------------------------=== //
// ================================================================= */
import Vue from 'vue'
import App from '@/App.vue'
import axios from 'axios'
import fr from 'vuetify/es5/locale/fr'
import i18n from '@/i18n'
import router from '@/router'
import store from '@/store'
import Vuetify from 'vuetify/lib'
/* ================================================================= //
// ===--- vueconfig ---------------------------------------------=== //
// ================================================================= */
Vue.config.productionTip = false
/* ================================================================= //
// ===--- axios -------------------------------------------------=== //
// ================================================================= */
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
Vue.prototype.$axios = axios
/* ================================================================= //
// ===--- prototype variables -----------------------------------=== //
// ================================================================= */
const stage = document.querySelector('meta[data-dm="dmodules"]') ? document.querySelector('meta[data-dm="dmodules"]').dataset.stage : 'live'
if (process.env.NODE_ENV === "production") {
  if (stage === "live") {
    Vue.prototype.$web_url = 'https://d-shop.us.aldryn.io'
    Vue.prototype.$app_url = 'https://d-shop.us.aldryn.io/commande'
    Vue.prototype.$api_url = 'https://d-shop.us.aldryn.io/shop/api'
  }
  else {
    Vue.prototype.$web_url = 'https://d-shop-stage.us.aldryn.io'
    Vue.prototype.$app_url = 'https://d-shop-stage.us.aldryn.io/commande'
    Vue.prototype.$api_url = 'https://d-shop-stage.us.aldryn.io/shop/api'
  }
} else {
  Vue.prototype.$web_url = 'http://localhost:8000'
  Vue.prototype.$app_url = 'http://localhost:8000/app'
  Vue.prototype.$api_url = 'http://localhost:8000/shop/api'
}
/* ================================================================= //
// ===--- vuetify -----------------------------------------------=== //
// ================================================================= */
Vue.use(Vuetify)
const vuetify = new Vuetify({
  lang: {
    locales: {fr},
    current: 'fr'
  },
  theme: {
    dark: false,
    light: true,
    options: {
      customProperties: true
    },
    themes: {
      light: {
        primary: '#48a89e'
      }
    }
  }
})
/* ================================================================= //
// ===--- vue ---------------------------------------------------=== //
// ================================================================= */
new Vue({
  i18n,
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
