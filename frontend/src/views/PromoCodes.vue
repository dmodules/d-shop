<template>
    <div id="promocodes">
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
                        <h2>{{$i18n.t('PromoCodes')}}</h2>
                    </v-col>
                </v-row>
                <v-form v-model="formCode">
                    <v-row>
                        <v-col cols="12" md="10" class="text-left">
                            <v-text-field
                                v-model="newCode"
                                :label="$i18n.t('Enteryourcodehere')"
                                placeholder=" "
                                :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                                :error-messages="hasErrorNewCode"
                                required
                                filled
                                @keydown="hasErrorNewCode = null"
                            />
                        </v-col>
                        <v-col cols="12" md="2" class="text-left">
                            <v-btn tile color="primary" class="btn btn-block" @click="doPromoCode()">{{$i18n.t('Add')}}</v-btn>
                        </v-col>
                    </v-row>
                </v-form>
                <v-row v-if="hasError || hasSuccess">
                    <v-col cols="12">
                        <v-alert v-if="hasError" text type="error">
                            <div v-html="hasError"></div>
                        </v-alert>
                        <v-alert v-if="hasSuccess" text type="success">
                            <div v-html="hasSuccess"></div>
                        </v-alert>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12" class="text-left">
                        <v-list dense two-line>
                            <template v-for="(item, n) in listPromo">
                                <v-list-item :key="'item'+n" v-if="!item.is_expired">
                                    <v-list-item-content>
                                        <v-list-item-title v-text="item.name"></v-list-item-title>
                                        <v-list-item-subtitle v-if="item.is_expired">Utilisé</v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                                <v-divider v-if="n < listPromo.length && !item.is_expired" :key="'divider'+n" />
                            </template>
                        </v-list>
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
        name: 'PromoCodes',
        components: {
            dmAuth: () => import("@/components/Auth.vue"),
        },
        data: () => ({
            isLoading: true,
            isAuth: false,
            listPromo: [],
            newCode: '',
            formCode: false,
            hasError: null,
            hasSuccess: null,
            hasErrorNewCode: null
        }),
        mounted () {
            this.setPromoCodes()
        },
        methods: {
            /* ========================================================= //
            // ===---   setAuth                                   ---=== //
            // ========================================================= */
            setAuth() {
                this.$set(this, "isAuth", true)
                this.setPromoCodes()
            },
            /* ========================================================= //
            // ===---   setPromoCodes                             ---=== //
            // ========================================================= */
            setPromoCodes () {
                let self = this
                this.$set(this, 'isLoading', false)
                this.$set(this, 'listPromo', [])
                // ===---
                this.$axios.get(this.$web_url+'/discount/promocodes/', {
                    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
                })
                .then((apiSuccess) => {
                    self.$set(self, 'listPromo', apiSuccess.data.promolist)
                })
                .catch(() => {})
            },
            doPromoCode () {
                let self = this
                this.$set(this, 'isLoading', false)
                this.$set(this, 'hasError', null)
                this.$set(this, 'hasSuccess', null)
                this.$set(this, 'hasErrorNewCode', null)
                // ===---
                let datas = {
                    promocode: this.newCode
                }
                // ===---
                if (!datas.promocode) {
                    this.$set(this, 'hasErrorNewCode', this.$i18n.t('Cechampsesrrequis'))
                }
                // ===---
                if (!this.hasError && !this.hasErrorNewCode) {
                    this.$axios.post(this.$web_url+'/discount/promocode/?promocode='+datas.promocode, datas, {
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
                    })
                    .then((apiSuccess) => {
                        if (apiSuccess.data.valid === true) {
                            self.$set(self, 'newCode', '')
                            self.$set(self, 'hasSuccess', self.$i18n.t('Codeaddedsuccess'))
                            self.setPromoCodes()
                        } else if (apiSuccess.data.valid === 'already') {
                            self.$set(self, 'hasError', self.$i18n.t('Codealreadyused'))
                        } else {
                            self.$set(self, 'hasError', self.$i18n.t('Codenotexist'))
                        }
                    })
                    .catch(() => {
                        self.$set(self, 'hasError', self.$i18n.t('Anerroroccured'))
                    })
                }
            }
        }
    }
</script>

<style scoped>
    .v-divider {
        margin: 2px 0;
    }
    .v-list--two-line .v-list-item,
    .v-list-item--two-line {
        min-height: 50px;
    }
</style>