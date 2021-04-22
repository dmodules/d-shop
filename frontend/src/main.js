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
// const stage = document.querySelector('meta[data-dm="dmodules"]') ? document.querySelector('meta[data-dm="dmodules"]').dataset.stage : 'live'
Vue.prototype.$web_url = window.location.origin
Vue.prototype.$app_url = window.location.origin+'/commande'
Vue.prototype.$shp_url = window.location.origin+'/shop'
Vue.prototype.$api_url = window.location.origin+'/shop/api'
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
        primary: '#066bf9'
      }
    }
  }
})
/* ================================================================= //
// ===--- Filters -----------------------------------------------=== //
// ================================================================= */
Vue.filter('fixdate', function (d) {
    let day = d.getDate()
    if (day < 10) {
        day = "0" + day
    }
    let month = d.getMonth()+1
    if (month < 10) {
        month = "0" + month
    }
    let year = d.getFullYear()
    let hour = d.getHours()
    if (hour < 10) {
        hour = "0" + hour
    }
    let minute = d.getMinutes()
    if (minute < 10) {
        minute = "0" + minute
    }
    return year + "-" + month + "-" + day + " " + hour + ":" + minute
})
/* ================================================================= //
// ===--- vue ---------------------------------------------------=== //
// ================================================================= */
if (document.getElementById("app")) {
    new Vue({
      i18n,
      router,
      store,
      vuetify,
      render: h => h(App)
    }).$mount("#app")
}
