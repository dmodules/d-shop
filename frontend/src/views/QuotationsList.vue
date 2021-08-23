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
            <div v-if="isAuth && !hasDetail" class="container">
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
                            <template v-slot:[`item.number`]="{ item }">
                                <div class="cursor-pointer py-2" @click="getQuotationsDetail(item.id+'-'+item.number)">
                                    <span v-text="item.number"></span>
                                </div>
                            </template>
                            <template v-slot:[`item.status`]="{ item }">
                                <div class="py-2" @click="getQuotationsDetail(item.id+'-'+item.number)">
                                    <v-chip v-if="item.status == 1" color="primary" small dark><span v-text="$i18n.t('Created')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 2" color="primary" small dark><span v-text="$i18n.t('Submitted')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 3" color="success" small dark><span v-text="$i18n.t('Approved')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 4" color="info" small dark><span v-text="$i18n.t('Ordered')"></span></v-chip>
                                    <v-chip v-else-if="item.status == 5" color="error" small dark><span v-text="$i18n.t('Rejected')"></span></v-chip>
                                    <v-chip v-else color="secondary" small dark><span v-text="$i18n.t('Unknown')"></span></v-chip>
                                </div>
                            </template>
                            <template v-slot:[`item.updated_at`]="{ item }">
                                <span @click="getQuotationsDetail(item.id+'-'+item.number)">{{ new Date(item.updated_at) | fixdate }}</span>
                            </template>
                        </v-data-table>
                    </v-col>
                </v-row>
            </div>
            <div v-else-if="isAuth && hasDetail" class="container">
                <v-row v-if="hasAccess">
                    <v-col cols="12" md="6" class="text-left">
                        <h2>
                            <v-btn tile color="primary" class="dmbtn-nowidth mr-3" @click="hasDetail = false">
                                <v-icon>mdi-chevron-left</v-icon>
                            </v-btn>
                            <span>{{ $i18n.t("YourQuotation") }} #{{ quotationsDetail.number }}</span>
                        </h2>
                    </v-col>
                    <v-col cols="12" md="6" class="text-left text-md-right">
                        <div class="py-2">
                            <v-chip v-if="quotationsDetail.status == 1" color="primary" dark><span v-text="$i18n.t('Created')"></span></v-chip>
                            <v-chip v-else-if="quotationsDetail.status == 2" color="primary" dark><span v-text="$i18n.t('Submitted')"></span></v-chip>
                            <v-chip v-else-if="quotationsDetail.status == 3" color="success" dark><span v-text="$i18n.t('Approved')"></span></v-chip>
                            <v-chip v-else-if="quotationsDetail.status == 4" color="info" dark><span v-text="$i18n.t('Ordered')"></span></v-chip>
                            <v-chip v-else-if="quotationsDetail.status == 5" color="error" dark><span v-text="$i18n.t('Rejected')"></span></v-chip>
                            <v-chip v-else color="secondary" dark><span v-text="$i18n.t('Unknown')"></span></v-chip>
                        </div>
                    </v-col>
                    <v-col cols="12">
                        <v-list>
                            <v-list-item>
                                <v-row class="align-items-center">
                                    <v-col cols="8" class="text-left">
                                        {{ $i18n.t("Product") }}
                                    </v-col>
                                    <v-col cols="2" class="text-center">
                                        {{ $i18n.t("Quantity") }}
                                    </v-col>
                                    <v-col cols="2" class="text-center">
                                        {{ $i18n.t("Price") }}
                                    </v-col>
                                </v-row>
                            </v-list-item>
                            <template v-for="(item, n) in quotationsDetail.items">
                                <v-divider v-if="n > 0" :key="'divider-'+item.product_code+'-' + n" />
                                <v-list-item :key="'product-' + n">
                                    <v-row class="align-items-center">
                                        <v-col cols="2" class="text-center">
                                            <a :href="item.product_url">
                                                <v-img :src="item.product_image" :alt="item.product_name" />
                                            </a>
                                        </v-col>
                                        <v-col cols="6" class="text-left">
                                            <a :href="item.product_url">
                                                <span v-text="item.product_name"></span>
                                            </a>
                                            <div v-if="item.variant_attribute">
                                                <span class="secondary--text" v-text="item.variant_attribute"></span>
                                            </div>
                                        </v-col>
                                        <v-col cols="2" class="text-center">
                                            <span v-text="item.quantity"></span>
                                        </v-col>
                                        <v-col cols="2" class="text-center">
                                            <span v-if="item.price" v-text="item.price"></span>
                                            <span v-else>- -</span>
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
            hasDetail: false,
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
                this.$set(this, 'hasDetail', false)
                this.getQuotationsList()
            } else {
                this.$set(this, 'hasDetail', true)
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
                this.$set(this, "hasDetail", false)
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
            getQuotationsDetail (query) {
                let self = this
                this.$set(this, "hasDetail", true)
                this.$set(this, "hasAccess", false)
                this.$set(this, "quotationsDetail", null)
                // ===---
                let number = null
                if (query) {
                    number = query
                } else if (this.$route.params.number) {
                    number = this.$route.params.number
                }
                if (number) {
                    // ===--- BEGIN: axios
                    this.$axios.get(this.$web_url + "/quotation/number/"+number.split('-')[0], {
                        headers: {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        },
                    })
                    .then((apiSuccess) => {
                        if (apiSuccess.data && apiSuccess.data.quotation && apiSuccess.data.quotation.number && apiSuccess.data.quotation.number == number.split('-')[1]) {
                            self.$set(this, "quotationsDetail", apiSuccess.data.quotation)
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
                } else {
                    self.$set(self, "hasAccess", false)
                    self.$set(self, "isLoading", false)
                }
            }
        }
    }
</script>
