<template>
  <div>
    <div v-if="isLoading">
      <v-row>
        <v-col cols="12" class="text-center">
          <v-progress-circular indeterminate :size="200" :width="20" color="primary" />
        </v-col>
      </v-row>
    </div>
    <div v-else-if="needAuth" class="container">
      <v-row>
        <v-col cols="12" class="text-left">
          <h2>{{$i18n.t('Commander')}}</h2>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6" lg="4">
          <div class="service-item item-content">
            <div class="service-content-box px-6">
              <v-form v-model="formLogin.valid">
                <v-row>
                  <v-col cols="12">
                    <div class="service-title">{{$i18n.t('Connexion')}}</div>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="formLogin.username"
                      :label="$i18n.t('Votrecourriel')"
                      placeholder=" "
                      :type="'email'"
                      :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    />
                    <v-text-field
                      v-model="formLogin.password"
                      :label="$i18n.t('Motdepasse')"
                      placeholder=" "
                      :type="'password'"
                      :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    />
                    <v-checkbox
                      :label="$i18n.t('Resterconnecte')"
                    />
                  </v-col>
                </v-row>
                <v-row v-if="formLogin.error">
                  <v-col cols="12">
                    <v-alert text color="error">
                      <div v-html="formLogin.error"></div>
                    </v-alert>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-btn tile color="primary" :disabled="!formLogin.valid" :loading="isLoadingLogin" @click="authLogin()">{{$i18n.t('Seconnecter')}}</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </div>
          </div>
        </v-col>
        <v-col cols="12" md="6" lg="4">
          <div class="service-item item-content">
            <div class="service-content-box px-6">
              <v-form v-model="formRegister.valid">
                <v-row>
                  <v-col cols="12">
                    <div class="service-title">{{$i18n.t('Inscription')}}</div>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="formRegister.email"
                      :label="$i18n.t('Votrecourriel')"
                      placeholder=" "
                      :type="'email'"
                      :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    />
                    <v-text-field
                      v-model="formRegister.password1"
                      :label="$i18n.t('Motdepasse')"
                      placeholder=" "
                      :type="'password'"
                      :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    />
                    <v-text-field
                      v-model="formRegister.password2"
                      :label="$i18n.t('Motdepasseconfirmation')"
                      placeholder=" "
                      :type="'password'"
                      :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    />
                  </v-col>
                </v-row>
                <v-row v-if="formRegister.error">
                  <v-col cols="12">
                    <v-alert text color="error">
                      <div v-html="formRegister.error"></div>
                    </v-alert>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-btn tile color="primary" :disabled="!formRegister.valid" :loading="isLoadingRegister" @click="authRegister()">{{$i18n.t('Sinscrire')}}</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </div>
          </div>
        </v-col>
        <v-col cols="12" lg="4">
          <div class="service-item item-content">
            <div class="service-content-box px-6">
              <v-form>
                <v-row>
                  <v-col cols="12">
                    <div class="service-title">{{$i18n.t('Continuereninvite')}}</div>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-btn tile color="primary" :loading="isLoadingGuest" @click="authAsGuest()">{{$i18n.t('Continuer')}}</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </div>
          </div>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Auth',
    data: () => ({
      isLoading: true,
      isLoadingLogin: false,
      isLoadingRegister: false,
      isLoadingGuest: false,
      needAuth: false,
      formLogin: {
        username: '',
        password: '',
        valid: false,
        error: null
      },
      formRegister: {
        email: '',
        password1: '',
        password2: '',
        valid: false,
        error: null
      }
    }),
    mounted () {
      this.getAuth()
    },
    methods: {
      /* =========================================================== //
      // ===---   setAuth                                     ---=== //
      // =========================================================== */
      setAuth () {
        this.$emit('is-auth', true)
      },
      /* =========================================================== //
      // ===---   getAuth                                     ---=== //
      // =========================================================== */
      getAuth () {
        let self = this
        // ===--- BEGIN: axios
        this.$axios.get(this.$web_url+'/api/fe/customer/', {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then((apiSuccess) => {
          if (apiSuccess.data.customer.guest === true) {
            self.$set(self, 'isLoading', false)
            self.$set(self, 'needAuth', true)
          } else {
            self.setAuth()
          }
        })
        .catch(() => {})
        // ===--- END: axios
      },
      /* =========================================================== //
      // ===---   authLogin                                   ---=== //
      // =========================================================== */
      authLogin () {
        let self = this
        // reset
        this.$set(this.formLogin, 'error', null)
        this.$set(this, 'isLoadingLogin', true)
        let datas = {
          form_data: {
            email: this.formLogin.username,
            password: this.formLogin.password
          }
        }
        // ===--- BEGIN: axios
        this.$axios.post(this.$web_url+'/shop/auth/login/', datas, {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then(() => {
          self.setAuth()
          self.$set(self, 'isLoadingLogin', false)
        })
        .catch((apiFail) => {
          self.$set(self, 'isLoadingLogin', false)
          if (apiFail.response && apiFail.response.data && apiFail.response.data.login_form) {
            if (apiFail.response.data.login_form.non_field_errors) {
              self.$set(self.formLogin, 'error', apiFail.response.data.login_form.non_field_errors[0])
            }
            if (apiFail.response.data.login_form.email) {
              self.$set(self.formLogin, 'error', apiFail.response.data.login_form.email[0])
            }
          }
        })
        // ===--- END: axios
      },
      /* =========================================================== //
      // ===---   authRegister                                ---=== //
      // =========================================================== */
      authRegister () {
        let self = this
        // reset
        this.$set(this.formRegister, 'error', null)
        this.$set(this, 'isLoadingRegister', true)
        let datas = {
          form_data: {
            email: this.formRegister.email,
            password1: this.formRegister.password1,
            password2: this.formRegister.password2
          }
        }
        // ===--- BEGIN: axios
        this.$axios.post(this.$web_url+'/shop/auth/register/', datas, {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then(() => {
          self.setAuth()
          self.$set(self, 'isLoadingRegister', false)
        })
        .catch((apiFail) => {
          self.$set(self, 'isLoadingRegister', false)
          if (apiFail.response && apiFail.response.data && apiFail.response.data.register_user_form) {
            if (apiFail.response.data.register_user_form.__all__) {
              self.$set(self.formRegister, 'error', apiFail.response.data.register_user_form.__all__[0])
            }
          }
        })
        // ===--- END: axios
      },
      /* =========================================================== //
      // ===---   authAsGuest                                 ---=== //
      // =========================================================== */
      authAsGuest () {
        let self = this
        // reset
        this.$set(this, 'isLoadingGuest', true)
        // ===--- BEGIN: axios
        this.$axios.post(this.$web_url+'/shop/auth/continue/', {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then(() => {
          self.setAuth()
          self.$set(self, 'isLoadingGuest', false)
        })
        .catch(() => {})
        // ===--- END: axios
      }
      /* =========================================================== //
      // ===-----------------------------------------------------=== //
      // =========================================================== */
    }
  }
</script>