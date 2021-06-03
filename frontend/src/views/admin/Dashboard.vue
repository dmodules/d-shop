<template>
    <div class="dmvue-admin-dashboard">
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
            <v-row>
                <v-col cols="12" md="6" lg="5" class="pa-0 ma-0">
                    <v-row class="text-left" style="height:100%">
                        <v-col cols="6">
                            <v-card style="height:100%">
                                <v-card-title class="caption text--secondary d-block text-truncate">
                                    <span v-text="$t('NewCustomers')"></span>
                                </v-card-title>
                                <v-card-text v-if="isLoadingCounts" class="text-center">
                                    <v-progress-circular
                                        indeterminate
                                        :size="60"
                                        :width="6"
                                        color="primary"
                                    />
                                </v-card-text>
                                <template v-else-if="!hasErrorCountsCustomers">
                                    <v-card-text class="display-1 font-weight-black">
                                        <span v-text="dataCounts.customers.thismonth"></span>
                                    </v-card-text>
                                    <v-card-actions class="caption py-1">
                                        <template v-if="dataCounts.customers.percent > 0">
                                            <v-icon small rounded color="success">mdi-trending-up</v-icon>
                                            <span class="success--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.customers.percent > 0">+</span><span v-text="dataCounts.customers.percent"></span>%
                                            </span>
                                        </template>
                                        <template v-else-if="dataCounts.customers.percent < 0">
                                            <v-icon small rounded color="error">mdi-trending-down</v-icon>
                                            <span class="error--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.customers.percent > 0">+</span><span v-text="dataCounts.customers.percent"></span>%
                                            </span>
                                        </template>
                                        <template v-else>
                                            <v-icon small rounded color="primary">mdi-trending-neutral</v-icon>
                                            <span class="primary--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.customers.percent > 0">+</span><span v-text="dataCounts.customers.percent"></span>%
                                            </span>
                                        </template>
                                        <span class="text--secondary d-inline-block text-truncate">depuis le mois dernier</span>
                                    </v-card-actions>
                                </template>
                                <template v-else>
                                    <v-card-text>
                                        <v-alert text type="error">
                                            <div v-html="hasErrorCountsCustomers"></div>
                                        </v-alert>
                                    </v-card-text>
                                </template>
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-card style="height:100%">
                                <v-card-title class="caption text--secondary d-block text-truncate">
                                    <span v-text="$t('OrdersCount')"></span>
                                </v-card-title>
                                <v-card-text v-if="isLoadingCounts" class="text-center">
                                    <v-progress-circular
                                        indeterminate
                                        :size="60"
                                        :width="6"
                                        color="primary"
                                    />
                                </v-card-text>
                                <template v-else-if="!hasErrorCountsOrders">
                                    <v-card-text class="display-1 font-weight-black">
                                        <span v-text="dataCounts.orders.thismonth"></span>
                                    </v-card-text>
                                    <v-card-actions class="caption py-1">
                                        <template v-if="dataCounts.orders.percent > 0">
                                            <v-icon small rounded color="success">mdi-trending-up</v-icon>
                                            <span class="success--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.orders.percent > 0">+</span><span v-text="dataCounts.orders.percent"></span>%
                                            </span>
                                        </template>
                                        <template v-else-if="dataCounts.orders.percent < 0">
                                            <v-icon small rounded color="error">mdi-trending-down</v-icon>
                                            <span class="error--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.orders.percent > 0">+</span><span v-text="dataCounts.orders.percent"></span>%
                                            </span>
                                        </template>
                                        <template v-else>
                                            <v-icon small rounded color="primary">mdi-trending-neutral</v-icon>
                                            <span class="primary--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.orders.percent > 0">+</span><span v-text="dataCounts.orders.percent"></span>%
                                            </span>
                                        </template>
                                        <span class="text--secondary d-inline-block text-truncate">depuis le mois dernier</span>
                                    </v-card-actions>
                                </template>
                                <template v-else>
                                    <v-card-text>
                                        <v-alert text type="error">
                                            <div v-html="hasErrorCountsOrders"></div>
                                        </v-alert>
                                    </v-card-text>
                                </template>
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-card style="height:100%">
                                <v-card-title class="caption text--secondary d-block text-truncate">
                                    <span v-text="$t('Incomes')"></span>
                                </v-card-title>
                                <v-card-text v-if="isLoadingCounts" class="text-center">
                                    <v-progress-circular
                                        indeterminate
                                        :size="60"
                                        :width="6"
                                        color="primary"
                                    />
                                </v-card-text>
                                <template v-else-if="!hasErrorCountsIncomes">
                                    <v-card-text class="headline font-weight-black">
                                        <span v-text="dataCounts.incomes.thismonth"></span>
                                    </v-card-text>
                                    <v-card-actions class="caption py-1">
                                        <template v-if="dataCounts.incomes.percent > 0">
                                            <v-icon small rounded color="success">mdi-trending-up</v-icon>
                                            <span class="success--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.incomes.percent > 0">+</span><span v-text="dataCounts.incomes.percent"></span>%
                                            </span>
                                        </template>
                                        <template v-else-if="dataCounts.incomes.percent < 0">
                                            <v-icon small rounded color="error">mdi-trending-down</v-icon>
                                            <span class="error--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.incomes.percent > 0">+</span><span v-text="dataCounts.incomes.percent"></span>%
                                            </span>
                                        </template>
                                        <template v-else>
                                            <v-icon small rounded color="primary">mdi-trending-neutral</v-icon>
                                            <span class="primary--text font-weight-black ml-1 mr-2">
                                                <span v-if="dataCounts.incomes.percent > 0">+</span><span v-text="dataCounts.incomes.percent"></span>%
                                            </span>
                                        </template>
                                        <span class="text--secondary d-inline-block text-truncate">depuis le mois dernier</span>
                                    </v-card-actions>
                                </template>
                                <template v-else>
                                    <v-card-text>
                                        <v-alert text type="error">
                                            <div v-html="hasErrorCountsIncomes"></div>
                                        </v-alert>
                                    </v-card-text>
                                </template>
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-card style="height:100%">
                                <v-card-title class="caption text--secondary d-block text-truncate">
                                    <span v-text="$t('AwaitingOrders')"></span>
                                </v-card-title>
                                <v-card-text v-if="isLoadingCounts" class="text-center">
                                    <v-progress-circular
                                        indeterminate
                                        :size="60"
                                        :width="6"
                                        color="primary"
                                    />
                                </v-card-text>
                                <template v-else-if="!hasErrorCountsAwaitings">
                                    <v-card-text class="display-1 font-weight-black pb-5">
                                        <span v-text="dataCounts.awaitings"></span>
                                    </v-card-text>
                                    <v-card-actions class="caption py-1 pb-5">&nbsp;</v-card-actions>
                                </template>
                                <template v-else>
                                    <v-card-text>
                                        <v-alert text type="error">
                                            <div v-html="hasErrorCountsAwaitings"></div>
                                        </v-alert>
                                    </v-card-text>
                                </template>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col cols="12" md="6" lg="7">
                    <v-card style="height:100%;min-height:300px">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate pb-0">
                            <span v-text="$t('MonthlyIncomes')"></span>
                        </v-card-title>
                        <v-progress-circular
                            v-if="isLoadingMonthlySales"
                            indeterminate
                            :size="60"
                            :width="6"
                            color="primary"
                        />
                        <dm-chart-bar v-else-if="!hasErrorMonthlySales" :data="chartMonthlySales" />
                        <v-card-text v-else>
                            <v-alert text type="error">
                                <div v-html="hasErrorMonthlySales"></div>
                            </v-alert>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12">
                    <v-card style="height:100%;min-height:300px">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">
                            <span v-text="$t('CurrentWeekIncomes')"></span>
                        </v-card-title>
                        <v-progress-circular
                            v-if="isLoadingWeeklySales"
                            indeterminate
                            :size="60"
                            :width="6"
                            color="primary"
                        />
                        <dm-chart-line v-else-if="!hasErrorWeeklySales" :data="chartWeeklySales" />
                        <v-card-text v-else>
                            <v-alert text type="error">
                                <div v-html="hasErrorMonthlySales"></div>
                            </v-alert>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col v-if="!demoNoLocation" cols="12" md="6" lg="4">
                    <v-card style="height:100%">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">
                            <span v-text="$t('IncomesByLocation')"></span>
                        </v-card-title>
                        <v-progress-circular
                            v-if="isLoadingByLocation"
                            indeterminate
                            :size="60"
                            :width="6"
                            color="primary"
                        />
                        <dm-chart-choropleth v-else-if="!hasErrorByLocation" :geoData="chartByLocation" />
                        <v-card-text v-else>
                            <v-alert text type="error">
                                <div v-html="hasErrorByLocation"></div>
                            </v-alert>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" lg="6">
                    <v-card style="height:100%">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">
                            <span v-text="$t('MonthBestsellers')"></span>
                        </v-card-title>
                        <v-progress-circular
                            v-if="isLoadingBestsellers"
                            indeterminate
                            :size="60"
                            :width="6"
                            color="primary"
                        />
                        <v-card-text v-else-if="!hasErrorBestsellers" class="dmadmin-bestsellers">
                            <v-data-table
                                :headers="headersBestsellers"
                                :items="listBestsellers"
                                :mobile-breakpoint="0"
                                hide-default-header
                                hide-default-footer
                                class="elevation-0"
                            >
                                <template v-slot:item.product_name="{ item }">
                                    <div>
                                        <a href=""><span v-text="item.product_name"></span></a>
                                    </div>
                                </template>
                                <template v-slot:item.product_price="{ item }">
                                    <div><span v-text="item.product_price"></span></div>
                                    <div class="caption text--secondary" v-text="$t('Price')"></div>
                                </template>
                                <template v-slot:item.product_quantity="{ item }">
                                    <div><span v-text="item.product_quantity"></span></div>
                                    <div class="caption text--secondary" v-text="$t('Quantity')"></div>
                                </template>
                                <template v-slot:item.product_amount="{ item }">
                                    <div><span v-text="item.product_amount"></span></div>
                                    <div class="caption text--secondary" v-text="$t('Income')"></div>
                                </template>
                            </v-data-table>
                        </v-card-text>
                        <v-card-text v-else>
                            <v-alert text type="error">
                                <div v-html="hasErrorBestsellers"></div>
                            </v-alert>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="12" md="6" lg="3">
                    <v-card style="height:100%">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">
                            <span v-text="$t('Stocks')"></span>
                        </v-card-title>
                        <v-progress-circular
                            v-if="isLoadingStocks"
                            indeterminate
                            :size="60"
                            :width="6"
                            color="primary"
                        />
                        <template v-else>
                            <div class="dmhover-cursor" @click="goTo('lowofstock')">
                                <dm-chart-donut v-if="!hasErrorStocksLow" :data="chartLowStocks" />
                                <v-card-text v-else>
                                    <v-alert text type="error">
                                        <div v-html="hasErrorStocksLow"></div>
                                    </v-alert>
                                </v-card-text>
                            </div>
                            <div class="dmhover-cursor" @click="goTo('outofstock')">
                                <dm-chart-donut v-if="!hasErrorStocksOut" :data="chartOutStocks" @click="goTo('outofstock')" />
                                <v-card-text v-else>
                                    <v-alert text type="error">
                                        <div v-html="hasErrorStocksOut"></div>
                                    </v-alert>
                                </v-card-text>
                            </div>
                        </template>
                    </v-card>
                </v-col>
                <v-col cols="12" md="6" lg="3">
                    <v-card class="dmvue-admin-activities">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">Activités récentes</v-card-title>
                        <v-card-text>
                            <v-timeline align-top clipped dense class="dmvue-admin-timeline-activities">
                                <v-timeline-item v-for="(item, n) in listLogs" :color="item.action == 1 ? 'primary' : item.action == 2 ? 'secondary' : item.action == 3 ? 'error' : 'grey'" fill-dot small :key="'logs-'+n">
                                    <strong class="d-block text-truncate" v-text="item.title"></strong>
                                    <div class="caption d-block text-truncate" v-text="item.content"></div>
                                    <div class="caption text--disabled d-block text-truncate">
                                        <span v-text="item.date"></span> <span v-text="item.user"></span>
                                    </div>
                                </v-timeline-item>
                            </v-timeline>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </template>
    </div>
</template>

<script>
    export default {
        name: "AdminDashboard",
        components: {
            dmChartBar: () => import('@/components/charts/chartBar.vue'),
            dmChartLine: () => import('@/components/charts/chartLine.vue'),
            dmChartDonut: () => import('@/components/charts/chartDonut.vue'),
            dmChartChoropleth: () => import('@/components/charts/chartChoropleth.vue')
        },
        data: () => ({
            demoNoLocation: true,
            isLoading: true,
            isLoadingCounts: true,
            isLoadingMonthlySales: true,
            isLoadingWeeklySales: true,
            isLoadingByLocation: true,
            isLoadingBestsellers: true,
            isLoadingStocks: true,
            isLoadingLogs: true,
            hasErrorCountsCustomers: null,
            hasErrorCountsOrders: null,
            hasErrorCountsIncomes: null,
            hasErrorCountsAwaitings: null,
            hasErrorMonthlySales: null,
            hasErrorWeeklySales: null,
            hasErrorByLocation: null,
            hasErrorBestsellers: null,
            hasErrorStocksLow: null,
            hasErrorStocksOut: null,
            hasErrorLogs: null,
            dataCounts: {
                customers: {},
                orders: {},
                incomes: {},
                awaitings: 0
            },
            chartMonthlySales: {
                labels: [],
                datasets: []
            },
            chartWeeklySales: {
                labels: [],
                datasets: []
            },
            chartByLocation: [
                {name:'Canada', amount:300},
                {name:'Brazil', amount:140},
                {name:'France', amount:66}
            ],
            headersBestsellers: [
                {
                    text: "Product",
                    value: "product_name",
                    align: "start",
                    sortable: false
                },
                {
                    text: "Price",
                    value: "product_price",
                    align: "start",
                    sortable: false
                },
                {
                    text: "Quantity",
                    value: "product_quantity",
                    align: "start",
                    sortable: false
                },
                {
                    text: "Amount",
                    value: "product_amount",
                    align: "start",
                    sortable: false
                }
            ],
            listBestsellers: [],
            chartLowStocks: {
                labels: [],
                datasets: []
            },
            chartOutStocks: {
                labels: [],
                datasets: []
            },
            listLogs: []
        }),
        mounted () {
            this.$set(this, "isLoading", false)
            this.getCounts()
            this.getMonthlySales()
            this.getWeeklySales()
            this.getByLocation()
            this.getBestsellers()
            this.getStocks()
            this.getLogs()
        },
        methods: {
            /* ============================================================ //
            // ===---   getCounts                                    ---=== //
            // ============================================================ */
            getCounts () {
                let self = this
                this.$set(this, "isLoadingCounts", true)
                this.$set(this.dataCounts, "customers", {})
                this.$set(this.dataCounts, "orders", {})
                this.$set(this.dataCounts, "incomes", {})
                this.$set(this.dataCounts, "awaitings", 0)
                this.$set(this, "hasErrorCountsCustomers", null)
                this.$set(this, "hasErrorCountsOrders", null)
                this.$set(this, "hasErrorCountsIncomes", null)
                this.$set(this, "hasErrorCountsAwaitings", null)
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url+"/dm-admin/counts/", {
                    headers: { "Content-Type": "application/json", "Accept": "application/json" }
                })
                .then((apiSuccess) => {
                    if (apiSuccess.data && apiSuccess.data.customers) {
                        self.$set(self.dataCounts, "customers", apiSuccess.data.customers)
                    } else {
                        self.$set(self, "hasErrorCountsCustomers", self.$t("Anerroroccured"))
                    }
                    if (apiSuccess.data && apiSuccess.data.orders) {
                        self.$set(self.dataCounts, "orders", apiSuccess.data.orders)
                    } else {
                        self.$set(self, "hasErrorCountsOrders", self.$t("Anerroroccured"))
                    }
                    if (apiSuccess.data && apiSuccess.data.incomes) {
                        self.$set(self.dataCounts, "incomes", apiSuccess.data.incomes)
                    } else {
                        self.$set(self, "hasErrorCountsIncomes", self.$t("Anerroroccured"))
                    }
                    if (apiSuccess.data && apiSuccess.data.awaitings) {
                        self.$set(self.dataCounts, "awaitings", apiSuccess.data.awaitings)
                    } else {
                        self.$set(self, "hasErrorCountsAwaitings", self.$t("Anerroroccured"))
                    }
                    self.$set(self, "isLoadingCounts", false)
                })
                .catch(() => {
                    self.$set(self, "hasErrorCountsCustomers", self.$t("Anerroroccured"))
                    self.$set(self, "hasErrorCountsOrders", self.$t("Anerroroccured"))
                    self.$set(self, "hasErrorCountsIncomes", self.$t("Anerroroccured"))
                    self.$set(self, "hasErrorCountsAwaitings", self.$t("Anerroroccured"))
                    self.$set(self, "isLoadingCounts", false)
                })
                // ===--- END: axios
            },
            /* ============================================================ //
            // ===---   getMonthlySales                              ---=== //
            // ============================================================ */
            getMonthlySales () {
                let self = this
                this.$set(this, "isLoadingMonthlySales", true)
                this.$set(this, "chartMonthlySales", {labels: [], datasets: []})
                this.$set(this, "hasErrorMonthlySales", null)
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url+"/dm-admin/monthly-sales/", {
                    headers: { "Content-Type": "application/json", "Accept": "application/json" }
                })
                .then((apiSuccess) => {
                    if (apiSuccess.data && apiSuccess.data.monthlysales) {
                        self.$set(self, "chartMonthlySales", apiSuccess.data.monthlysales)
                    } else {
                        self.$set(self, "hasErrorMonthlySales", self.$t("Anerroroccured"))
                    }
                    self.$set(self, "isLoadingMonthlySales", false)
                })
                .catch(() => {
                    self.$set(self, "hasErrorMonthlySales", self.$t("Anerroroccured"))
                    self.$set(self, "isLoadingMonthlySales", false)
                })
                // ===--- END: axios
            },
            /* ============================================================ //
            // ===---   getWeeklySales                               ---=== //
            // ============================================================ */
            getWeeklySales () {
                let self = this
                this.$set(this, "isLoadingWeeklySales", true)
                this.$set(this, "chartWeeklySales", {labels: [], datasets: []})
                this.$set(this, "hasErrorWeeklySales", null)
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url+"/dm-admin/weekly-sales/", {
                    headers: { "Content-Type": "application/json", "Accept": "application/json" }
                })
                .then((apiSuccess) => {
                    if (apiSuccess.data && apiSuccess.data.weeklysales) {
                        self.$set(self, "chartWeeklySales", apiSuccess.data.weeklysales)
                    } else {
                        self.$set(self, "hasErrorWeeklySales", self.$t("Anerroroccured"))
                    }
                    self.$set(self, "isLoadingWeeklySales", false)
                })
                .catch(() => {
                    self.$set(self, "hasErrorWeeklySales", self.$t("Anerroroccured"))
                    self.$set(self, "isLoadingWeeklySales", false)
                })
                // ===--- END: axios
            },
            /* ============================================================ //
            // ===---   getByLocation                                ---=== //
            // ============================================================ */
            getByLocation () {
                let self = this
                this.$set(this, "isLoadingByLocation", true)
                this.$set(this, "chartByLocation", [])
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url+"/dm-admin/bylocation/", {
                    headers: { "Content-Type": "application/json", "Accept": "application/json" }
                })
                .then((apiSuccess) => {
                    if (apiSuccess.data && apiSuccess.data.bylocation) {
                        self.$set(self, "chartByLocation", apiSuccess.data.bylocation)
                    } else {
                        self.$set(self, "hasErrorByLocation", self.$t("Anerroroccured"))
                    }
                    self.$set(self, "isLoadingByLocation", false)
                })
                .catch(() => {
                    self.$set(self, "hasErrorByLocation", self.$t("Anerroroccured"))
                    self.$set(self, "isLoadingByLocation", false)
                })
                // ===--- END: axios
            },
            /* ============================================================ //
            // ===---   getBestsellers                               ---=== //
            // ============================================================ */
            getBestsellers () {
                let self = this
                this.$set(this, "isLoadingBestsellers", true)
                this.$set(this, "listBestsellers", [])
                this.$set(this, "hasErrorBestsellers", null)
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url+"/dm-admin/bestsellers/", {
                    headers: { "Content-Type": "application/json", "Accept": "application/json" }
                })
                .then((apiSuccess) => {
                    if (apiSuccess.data && apiSuccess.data.bestsellers) {
                        self.$set(self, "listBestsellers", apiSuccess.data.bestsellers)
                    } else {
                        self.$set(self, "hasErrorBestsellers", self.$t("Anerroroccured"))
                    }
                    self.$set(self, "isLoadingBestsellers", false)
                })
                .catch(() => {
                    self.$set(self, "hasErrorBestsellers", self.$t("Anerroroccured"))
                    self.$set(self, "isLoadingBestsellers", false)
                })
                // ===--- END: axios
            },
            /* ============================================================ //
            // ===---   getStocks                                    ---=== //
            // ============================================================ */
            getStocks () {
                let self = this
                this.$set(this, "isLoadingStocks", true)
                this.$set(this, "chartLowStocks", {labels: [], datasets: []})
                this.$set(this, "chartOutStocks", {labels: [], datasets: []})
                this.$set(this, "hasErrorStocksLow", null)
                this.$set(this, "hasErrorStocksOut", null)
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url+"/dm-admin/stocks/", {
                    headers: { "Content-Type": "application/json", "Accept": "application/json" }
                })
                .then((apiSuccess) => {
                    if (apiSuccess.data && apiSuccess.data.lowofstock) {
                        self.$set(self, "chartLowStocks", apiSuccess.data.lowofstock)
                    } else {
                        self.$set(self, "hasErrorStocksLow", self.$t("Anerroroccured"))
                    }
                    if (apiSuccess.data && apiSuccess.data.outofstock) {
                        self.$set(self, "chartOutStocks", apiSuccess.data.outofstock)
                    } else {
                        self.$set(self, "hasErrorStocksOut", self.$t("Anerroroccured"))
                    }
                    self.$set(self, "isLoadingStocks", false)
                })
                .catch(() => {
                    self.$set(self, "hasErrorStocksLow", self.$t("Anerroroccured"))
                    self.$set(self, "hasErrorStocksOut", self.$t("Anerroroccured"))
                    self.$set(self, "isLoadingStocks", false)
                })
                // ===--- END: axios
            },
            /* ============================================================ //
            // ===---   getLogs                                      ---=== //
            // ============================================================ */
            getLogs () {
                let self = this
                this.$set(this, "isLoadingLogs", true)
                this.$set(this, "listLogs", [])
                this.$set(this, "hasErrorLogs", null)
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url+"/dm-admin/logs/", {
                    headers: { "Content-Type": "application/json", "Accept": "application/json" }
                })
                .then((apiSuccess) => {
                    if (apiSuccess.data && apiSuccess.data.logs) {
                        self.$set(self, "listLogs", apiSuccess.data.logs)
                    } else {
                        self.$set(self, "hasErrorLogs", self.$t("Anerroroccured"))
                    }
                    self.$set(self, "isLoadingLogs", false)
                })
                .catch(() => {
                    self.$set(self, "hasErrorLogs", self.$t("Anerroroccured"))
                    self.$set(self, "isLoadingLogs", false)
                })
                // ===--- END: axios
            },
            /* ============================================================ //
            // ===---   goTo                                         ---=== //
            // ============================================================ */
            goTo (k) {
                if (k == "lowofstock") {
                    window.location = window.location.origin + "/" + this.$i18n.locale + "/admindshop/product/?get_product_out_or_low=lowonstock"
                } else if (k == "outofstock") {
                    window.location = window.location.origin + "/" + this.$i18n.locale + "/admindshop/product/?get_product_out_or_low=outofstock"
                }
            }
            /* ============================================================ //
            // ===------------------------------------------------------=== //
            // ============================================================ */
        }
    }
</script>

<style>
    :root {
        --v-primary-base: #066bf9;
        --v-anchor-base: #066bf9;
    }
    .dmhover-cursor:hover {
        cursor: pointer;
    }
    .dmadmin-bestsellers > .v-data-table > .v-data-table__wrapper > table td {
        border-bottom: none;
    }
    .dmadmin-bestsellers > .v-data-table > .v-data-table__wrapper > table > tbody > tr:not(:last-child) > td:not(.v-data-table__mobile-row),
    .dmadmin-bestsellers > .v-data-table > .v-data-table__wrapper > table > tbody > tr:not(:last-child) > th:not(.v-data-table__mobile-row),
    .dmadmin-bestsellers > .v-data-table > .v-data-table__wrapper > table > tbody > tr:not(:last-child) > td:last-child,
    .dmadmin-bestsellers > .v-data-table > .v-data-table__wrapper > table > tbody > tr:not(:last-child) > th:last-child {
        border-bottom-color: #eee;
    }
</style>
