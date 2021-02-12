<template>
    <div class="quotation" id="app-quotation">
        <template v-if="isLoading">
            <v-row>
                <v-col cols="12" class="text-center">
                    <v-progress-circular
                        indeterminate
                        :size="200"
                        :width="20"
                        color="primary"
                    />
                </v-col>
            </v-row>
        </template>
        <template v-else>
            <div v-if="isAuth && !$route.params.number" class="container">
                <v-row>
                    <div class="col-12 text-left">
                        <h2>{{ $i18n.t("MyQuotations") }}</h2>
                    </div>
                </v-row>
                <v-row>
                    <v-col cols="12">
                        <v-data-table
                            dense
                            :headers="quotationsHeaders"
                            :items="quotationsList"
                            hide-default-footer
                            item-key="id"
                            class="elevation-0"
                        >
                            <template v-slot:[`header.updated_at`]="">
                                {{ $i18n.t('LastUpdate') }}
                            </template>
                            <template v-slot:[`item.status`]="{ item }">
                                <div class="py-2">
                                    <v-chip v-if="item.status == 1" color="primary" small dark><span v-text="$i18n.t('Created')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 2" color="primary" small dark><span v-text="$i18n.t('Submitted')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 3" color="success" small dark><span v-text="$i18n.t('Approved')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 4" color="info" small dark><span v-text="$i18n.t('Ordered')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 5" color="error" small dark><span v-text="$i18n.t('Rejected')"></span></v-chip>
                                    <v-chip v-else color="secondary" small dark><span v-text="$i18n.t('Unknown')"></span></v-chip>
                                </div>
                            </template>
                            <template v-slot:[`item.updated_at`]="{ item }">
                                <span>{{ new Date(item.updated_at) | fixdate }}</span>
                            </template>
                        </v-data-table>
                    </v-col>
                </v-row>
            </div>
            <div v-else-if="isAuth && $route.params.number" class="container">
                <v-row v-if="hasAccess">
                    <v-col cols="12" class="text-left">
                        <h2>{{ $i18n.t("YourQuotation") }} #{{ $route.params.number.split('-')[1] }}</h2>
                    </v-col>
                    <v-col cols="12">
                        <v-list>
                            <v-list-item>
                                <v-row class="align-items-center">
                                    <v-col cols="12" md="9" class="text-left">
                                        {{ $i18n.t("Product") }}
                                    </v-col>
                                    <v-col cols="12" md="3" class="text-center">
                                        {{ $i18n.t("Quantity") }}
                                    </v-col>
                                </v-row>
                            </v-list-item>
                            <template v-for="(item, n) in quotationsDetail.items.items">
                                <v-divider v-if="n > 0" :key="'divider-'+item.product_code+'-' + n" />
                                <v-list-item :key="'product-' + n">
                                    <v-row class="align-items-center">
                                        <v-col cols="2" md="1" class="text-center">
                                            <v-icon>mdi-cat</v-icon>
                                        </v-col>
                                        <v-col cols="8" md="8" class="text-left">
                                            <span v-text="item.product_name"></span>
                                        </v-col>
                                        <v-col cols="2" md="3" class="text-center">
                                            <span v-text="item.quantity"></span>
                                        </v-col>
                                    </v-row>
                                </v-list-item>
                            </template>
                        </v-list>
                    </v-col>
                </v-row>
                <v-row v-else>
                    <v-col cols="12" class="text-center py-6">
                        <h2>{{ $i18n.t("Thisquotationnotexist") }}</h2>
                        <p>
                            <a href="/">{{ $i18n.t("Retourneralaccueil") }}</a>
                        </p>
                    </v-col>
                </v-row>
            </div>
            <div v-else-if="!isAuth">
                <dm-auth @is-auth="setAuth()" />
            </div>
        </template>
    </div>
</template>

<script>
    export default {
        name: "QuotationsList",
        components: {
            dmAuth: () => import("@/components/Auth.vue"),
        },
        data: () => ({
            isAuth: false,
            isLoading: true,
            hasAccess: false,
            quotationsHeaders: [
                {
                    text: "#",
                    align: "start",
                    sortable: true,
                    value: "number"
                },
                {
                    text: "Status",
                    align: "start",
                    sortable: true,
                    value: "status"
                },
                {
                    text: "Last Update",
                    align: "end",
                    sortable: false,
                    value: "updated_at"
                }
            ],
            quotationsList: [],
            quotationsDetail: null
        }),
        mounted() {
            document.title = this.$i18n.t('MyQuotations')
            if (!this.$route.params.number) {
                this.getQuotationsList()
            } else {
                this.getQuotationsDetail()
            }
        },
        methods: {
            setAuth() {
                this.$set(this, "isAuth", true)
            },
            /* =========================================================== //
            // ===---   getQuotationsList                           ---=== //
            // =========================================================== */
            getQuotationsList () {
                let self = this
                this.$set(this, "quotationsList", [])
                // ===--- BEGIN: axios
                this.$axios
                    .get(this.$web_url + "/quotation/list/", {
                        headers: {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        },
                    })
                    .then((apiSuccess) => {
                        if (apiSuccess.data && apiSuccess.data[0] && apiSuccess.data[0].id) {
                            self.$set(this, "quotationsList", apiSuccess.data)
                        }
                        self.$set(self, "isLoading", false)
                    })
                    .catch(() => {
                        self.$set(self, "isLoading", false)
                    });
                // ===--- END: axios
            },
            /* =========================================================== //
            // ===---   getQuotationsDetail                         ---=== //
            // =========================================================== */
            getQuotationsDetail () {
                let self = this
                this.$set(this, "hasAccess", false)
                this.$set(this, "quotationsDetail", null)
                // ===--- BEGIN: axios
                this.$axios
                    .get(this.$web_url + "/quotation/number/"+this.$route.params.number.split('-')[0], {
                        headers: {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        },
                    })
                    .then((apiSuccess) => {
                        if (apiSuccess.data && apiSuccess.data.number && apiSuccess.data.number == this.$route.params.number.split('-')[1]) {
                            self.$set(this, "quotationsDetail", apiSuccess.data)
                            self.$set(self, "hasAccess", true)
                        } else {
                            self.$set(self, "hasAccess", false)
                        }
                        self.$set(self, "isLoading", false)
                    })
                    .catch(() => {
                        self.$set(self, "isLoading", false)
                    });
                // ===--- END: axios
            }
        }
    }
</script>
