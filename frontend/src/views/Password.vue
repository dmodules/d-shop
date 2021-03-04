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
      <v-row v-if="$route.params.action === 'reset'">
            <v-col cols="12" class="text-left">
                <h2>{{$i18n.t('PasswordReset')}}</h2>
            </v-col>
            <v-col cols="12">
                <v-text-field
                    v-model="email"
                    :label="$i18n.t('Courriel')"
                    placeholder=" "
                    :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    :error-messages="hasErrorEmail"
                    required
                    filled
                    @keydown="hasErrorEmail = null"
                />
            </v-col>
            <v-col cols="12" v-if="hasErrorEmail">
                <v-alert text type="error">
                    <div v-html="hasErrorEmail"></div>
                </v-alert>
            </v-col>
            <v-col cols="12" v-else-if="hasSuccessEmail">
                <v-alert text type="success">
                    <div v-html="hasSuccessEmail"></div>
                </v-alert>
            </v-col>
            <v-col cols="12">
                <v-btn tile color="primary" @click="doPasswordReset()">{{$i18n.t('Envoyer')}}</v-btn>
            </v-col>
      </v-row>
      <v-row v-if="this.$route.params.action === 'reinitialisation-du-mot-de-passe'">
            <v-col cols="12" class="text-left">
                <h2>{{$i18n.t('PasswordReset')}}</h2>
            </v-col>
            <v-col v-if="!hasResetSuccess" cols="12">
                <v-text-field
                    v-model="password1"
                    :label="$i18n.t('Password')"
                    :type="'password'"
                    placeholder=" "
                    :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    :error-messages="hasErrorPassword1"
                    required
                    filled
                    @keydown="hasErrorPassword1 = null"
                />
            </v-col>
            <v-col v-if="!hasResetSuccess" cols="12">
                <v-text-field
                    v-model="password2"
                    :label="$i18n.t('PasswordConfirm')"
                    :type="'password'"
                    placeholder=" "
                    :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                    :error-messages="hasErrorPassword2"
                    required
                    filled
                    @keydown="hasErrorPassword2 = null"
                />
            </v-col>
            <v-col cols="12" v-if="hasError">
                <v-alert text type="error">
                    <div v-html="hasError"></div>
                </v-alert>
            </v-col>
            <v-col cols="12" v-else-if="hasSuccess">
                <v-alert text type="success">
                    <div v-html="hasSuccess"></div>
                </v-alert>
            </v-col>
            <v-col v-if="!hasResetSuccess" cols="12">
                <v-btn tile color="primary" @click="doConfirmPassword()">{{$i18n.t('Envoyer')}}</v-btn>
            </v-col>
            <v-col v-if="hasResetSuccess" cols="12">
                <v-btn tile color="primary" :href="'/'">{{$i18n.t('Retourneralaccueil')}}</v-btn>
            </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Password',
    data: () => ({
      isLoading: true,
      email: '',
      password1: '',
      password2: '',
      hasErrorEmail: null,
      hasErrorPassword1: null,
      hasErrorPassword2: null,
      hasError: null,
      hasSuccessEmail: null,
      hasSuccess: null,
      hasResetSuccess: false
    }),
    mounted () {
        this.$set(this, 'isLoading', false)
    },
    methods: {
        doPasswordReset () {
            let self = this
            this.$set(this, 'hasErrorEmail', null)
            this.$set(this, 'hasSuccessEmail', null)
            // ===---
            let datas = {
                form_data: {
                    email: this.email
                }
            }
            // ===--- BEGIN: axios
            this.$axios.post(this.$web_url+'/api/fe/send-unclone/', datas, {
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
            })
            // ===---
            this.$axios.post(this.$shp_url+'/auth/password/reset/', datas, {
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
            })
            .then((apiSuccess) => {
                if (apiSuccess.data && apiSuccess.data.password_reset_request_form && apiSuccess.data.password_reset_request_form.success_message) {
                    self.$set(self, 'hasSuccessEmail', apiSuccess.data.password_reset_request_form.success_message)
                }
                self.$axios.get(self.$web_url+'/api/fe/send-email/', {
                    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
                })
            })
            .catch((apiFail) => {
                if (apiFail.response && apiFail.response.data && apiFail.response.data.password_reset_request_form) {
                    self.$set(self, 'hasErrorEmail', apiFail.response.data.password_reset_request_form.email[0])
                } else {
                    self.$set(self, 'hasErrorEmail', self.$i18n.t('Anerroroccured'))
                }
            })
        },
        /* =========================================================== //
        // ===-----------------------------------------------------=== //
        // =========================================================== */
        doConfirmPassword () {
            let self = this
            this.$set(this, 'hasErrorPassword1', null)
            this.$set(this, 'hasErrorPassword2', null)
            this.$set(this, 'hasError', null)
            this.$set(this, 'hasSuccess', null)
            this.$set(this, 'hasResetSuccess', false)
            // ===---
            let datas = {
                "form_data" : {
                    new_password1: self.password1,
                    new_password2: self.password2,
                    token: self.$route.params.token ? self.$route.params.token : "error",
                    uid: self.$route.params.uidb64 ? self.$route.params.uidb64 : "error"
                }
            }
            // ===--- BEGIN: axios
            this.$axios.post(self.$shp_url+'/auth/password/reset-confirm/', datas, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            })
            .then((apiSuccess) => {
                if (apiSuccess.data && apiSuccess.data.password_reset_confirm_form && apiSuccess.data.password_reset_confirm_form.success_message) {
                    self.$set(self, 'hasSuccess', apiSuccess.data.password_reset_confirm_form.success_message)
                    self.$set(self, 'hasResetSuccess', true)
                } else {
                    self.$set(self, 'hasError', self.$i18n.t('Anerroroccured'))
                }
            })
            .catch((apiFail) => {
                if (apiFail.response && apiFail.response.data && apiFail.response.data.password_reset_confirm_form) {
                    if (apiFail.response.data.password_reset_confirm_form.new_password1) {
                        self.$set(self, 'hasErrorPassword1', apiFail.response.data.password_reset_confirm_form.new_password1[0])
                    }
                    if (apiFail.response.data.password_reset_confirm_form.new_password2) {
                        self.$set(self, 'hasErrorPassword2', apiFail.response.data.password_reset_confirm_form.new_password2[0])
                    }
                    if (apiFail.response.data.password_reset_confirm_form.token) {
                        self.$set(self, 'hasError', self.$i18n.t('Anerroroccured'))
                    }
                    if (apiFail.response.data.password_reset_confirm_form.uid) {
                        self.$set(self, 'hasError', self.$i18n.t('Anerroroccured'))
                    }
                } else {
                    self.$set(self, 'hasError', self.$i18n.t('Anerroroccured'))
                }
            })
            // ===--- END: axios
        }
        /* =========================================================== //
        // ===-----------------------------------------------------=== //
        // =========================================================== */
    }
  }
</script>