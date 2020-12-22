<template>
  <div>
    <div v-if="isLoading">
      <v-row>
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate :size="200" :width="20" color="primary" />
        </v-col>
      </v-row>
    </div>
    <div v-else class="container">
        <div v-if="isAuth">
            <v-row>
                <v-col cols="12" class="text-left">
                <h2>{{$i18n.t('Profil')}}</h2>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12">
                <v-form v-model="formProfil.valid">
                    <v-row>
                    <v-col cols="12" md="6">
                        <v-select
                        v-model="formProfil.customer.salutation"
                        :label="$i18n.t('Salutation')"
                        placeholder=" "
                        :items="listSalutation"
                        :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                        :error-messages="formError.customer.salutation"
                        required
                        filled
                        attach
                        @keydown="formError.customer.salutation = null"
                        />
                    </v-col>
                    <v-col cols="12" md="6">
                        <v-text-field
                        v-model="formProfil.customer.email"
                        :label="$i18n.t('Courriel')"
                        placeholder=" "
                        :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                        :error-messages="formError.customer.email"
                        required
                        filled
                        @keydown="formError.customer.email = null"
                        />
                    </v-col>
                    <v-col cols="12" md="6">
                        <v-text-field
                        v-model="formProfil.customer.first_name"
                        :label="$i18n.t('Prenom')"
                        placeholder=" "
                        :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                        :error-messages="formError.customer.first_name"
                        required
                        filled
                        @keydown="formError.customer.first_name = null"
                        />
                    </v-col>
                    <v-col cols="12" md="6">
                        <v-text-field
                        v-model="formProfil.customer.last_name"
                        :label="$i18n.t('Nomdefamille')"
                        placeholder=" "
                        :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                        :error-messages="formError.customer.last_name"
                        required
                        filled
                        @keydown="formError.customer.last_name = null"
                        />
                    </v-col>
                    </v-row>
                    <v-row v-if="formProfil.success">
                    <v-col cols="12">
                        <v-alert text color="success">
                        <div v-html="formProfil.success"></div>
                        </v-alert>
                    </v-col>
                    </v-row>
                    <v-row>
                    <v-col cols="12">
                        <v-btn tile color="primary" :disabled="!formProfil.valid" @click="setUpload()">{{$i18n.t('Modifier')}}</v-btn>
                    </v-col>
                    </v-row>
                </v-form>
                </v-col>
            </v-row>
        </div>
        <div v-else>
            <dm-auth @is-auth="setAuth()" />
        </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Profil',
    components: {
        dmAuth: () => import("@/components/Auth.vue"),
    },
    data: () => ({
      isLoading: true,
      isLoadingProfil: false,
      isAuth: false,
      listSalutation: [],
      formProfil: {
        valid: false,
        success: null,
        customer: {
          plugin_order: 1,
          salutation: null,
          first_name: null,
          last_name: null,
          email: null
        }
      },
      formError: {
        customer: {
          salutation: null,
          first_name: null,
          last_name: null,
          email: null
        }
      }
    }),
    mounted () {
      this.$set(this, 'listSalutation', [
        {text: this.$i18n.t('Madame'),value: 'mrs'},
        {text: this.$i18n.t('Monsieur'),value: 'mr'},
        {text: this.$i18n.t('Preferepasrepondre'),value: 'na'}
      ])
      this.getCustomer()
    },
    methods: {
        /* ========================================================= //
        // ===---   setAuth                                   ---=== //
        // ========================================================= */
        setAuth() {
            this.$set(this, "isAuth", true);
        },
      /* =========================================================== //
      // ===---   getCustomer                                 ---=== //
      // =========================================================== */
      getCustomer () {
        let self = this
        // reset
        this.$set(this, 'isLoading', true)
        // ===--- BEGIN: axios
        this.$axios.get(this.$web_url+'/api/fe/customer/', {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then((apiSuccess) => {
          // set customer form
          if (apiSuccess.data.customer) {
            self.$set(self.formProfil.customer, 'salutation', apiSuccess.data.customer.salutation ? apiSuccess.data.customer.salutation : '')
            self.$set(self.formProfil.customer, 'first_name', apiSuccess.data.customer.first_name ? apiSuccess.data.customer.first_name : '')
            self.$set(self.formProfil.customer, 'last_name', apiSuccess.data.customer.last_name ? apiSuccess.data.customer.last_name : '')
            self.$set(self.formProfil.customer, 'email', apiSuccess.data.customer.email ? apiSuccess.data.customer.email : '')
          }
          self.$set(self, 'isLoading', false)
        })
        .catch(() => {
          self.$set(self, 'isLoading', false)
        })
        // ===--- END: axios
      },
      /* =========================================================== //
      // ===---   setUpload                                   ---=== //
      // =========================================================== */
      setUpload () {
        let self = this
        // reset
        this.$set(this.formProfil, 'success', null)
        this.$set(this, 'isLoadingProfil', true)
        // data
        let datas = this.formProfil
        // ===--- BEGIN: axios
        this.$axios.put(this.$api_url+'/checkout/upload/', datas, {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then(() => {
          self.$set(self.formProfil, 'success', 'Profil mis à jour avec succès&nbsp;!')
          self.$set(self, 'isLoadingProfil', false)
        })
        .catch((apiFail) => {
          if (apiFail.response && apiFail.response.data) {
            if (apiFail.response.data.customer_form) {
              self.$set(self.formError.customer, 'salutation', apiFail.response.data.customer_form.salutation ? apiFail.response.data.customer_form.salutation : null)
              self.$set(self.formError.customer, 'first_name', apiFail.response.data.customer_form.first_name ? apiFail.response.data.customer_form.first_name : null)
              self.$set(self.formError.customer, 'last_name', apiFail.response.data.customer_form.last_name ? apiFail.response.data.customer_form.last_name : null)
              self.$set(self.formError.customer, 'email', apiFail.response.data.customer_form.email ? apiFail.response.data.customer_form.email : null)
            }
          }
          self.$set(self, 'isLoadingProfil', false)
        })
        // ===--- END: axios
      }
      /* =========================================================== //
      // ===-----------------------------------------------------=== //
      // =========================================================== */
    }
  }
</script>