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
                                <v-card-title class="caption text--secondary d-block text-truncate">Nombre de nouveaux clients</v-card-title>
                                <v-card-text class="display-1 font-weight-black">27</v-card-text>
                                <v-card-actions class="caption py-1">
                                    <v-icon small rounded color="success">mdi-trending-up</v-icon>
                                    <span class="success--text font-weight-black ml-1 mr-2">+100%</span>
                                    <span class="text--secondary d-inline-block text-truncate">depuis le mois dernier</span>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-card style="height:100%">
                                <v-card-title class="caption text--secondary d-block text-truncate">Nombre de commandes</v-card-title>
                                <v-card-text class="display-1 font-weight-black">346</v-card-text>
                                <v-card-actions class="caption py-1">
                                    <v-icon small rounded color="success">mdi-trending-up</v-icon>
                                    <span class="success--text font-weight-black ml-1 mr-2">+67%</span>
                                    <span class="text--secondary d-inline-block text-truncate">depuis le mois dernier</span>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-card style="height:100%">
                                <v-card-title class="caption text--secondary d-block text-truncate">Revenus</v-card-title>
                                <v-card-text class="display-1 font-weight-black">3 467$</v-card-text>
                                <v-card-actions class="caption py-1">
                                    <v-icon small rounded color="success">mdi-trending-up</v-icon>
                                    <span class="success--text font-weight-black ml-1 mr-2">+14%</span>
                                    <span class="text--secondary d-inline-block text-truncate">depuis le mois dernier</span>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                        <v-col cols="6">
                            <v-card style="height:100%">
                                <v-card-title class="caption text--secondary d-block text-truncate">Commandes en attente</v-card-title>
                                <v-card-text class="display-1 font-weight-black pb-5">3</v-card-text>
                                <v-card-actions class="caption py-1 pb-5">&nbsp;</v-card-actions>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col cols="12" md="6" lg="7">
                    <v-card style="max-height:300px">
                        <dm-chart-bar :data="chartMonthlySales" />
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" md="6" lg="8">
                    <v-card style="height:100%">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">Revenues</v-card-title>
                        <dm-chart-line :data="chartWeeklySales" />
                    </v-card>
                </v-col>
                <v-col cols="12" md="6" lg="4">
                    <v-card style="height:100%">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">Revenus par localisation</v-card-title>
                        <dm-chart-choropleth :geoData="chartByLocation" />
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" lg="6">
                    <v-card style="height:100%">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">Meilleures ventes du mois</v-card-title>
                        <v-card-text>
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
                                    <div class="caption text--secondary">Prix</div>
                                </template>
                                <template v-slot:item.product_quantity="{ item }">
                                    <div><span v-text="item.product_quantity"></span></div>
                                    <div class="caption text--secondary">Quantité</div>
                                </template>
                                <template v-slot:item.product_amount="{ item }">
                                    <div><span v-text="item.product_amount"></span></div>
                                    <div class="caption text--secondary">Revenu</div>
                                </template>
                            </v-data-table>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="12" md="6" lg="3">
                    <v-card style="height:100%">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">Inventaire</v-card-title>
                        <dm-chart-donut :data="chartLowStocks" />
                        <dm-chart-donut :data="chartOutStocks" />
                    </v-card>
                </v-col>
                <v-col cols="12" md="6" lg="3">
                    <v-card class="dmvue-admin-activities">
                        <v-card-title class="text-left caption text--secondary d-block text-truncate">Activités récentes</v-card-title>
                        <v-card-text>
                            <v-timeline align-top clipped dense class="dmvue-admin-timeline-activities">
                                <v-timeline-item color="secondary" fill-dot small>
                                    <strong class="d-block text-truncate">Produit ajouté</strong>
                                    <div class="caption d-block text-truncate">"T-shirt rayé" ajouté aux produits</div>
                                    <div class="caption text--disabled d-block text-truncate">22 avril 2021 à 11:12</div>
                                </v-timeline-item>
                                <v-timeline-item color="primary" fill-dot small>
                                    <strong class="d-block text-truncate">Catégorie modifiée</strong>
                                    <div class="caption d-block text-truncate">"Vêtements d'été" a été modifiée</div>
                                    <div class="caption text--disabled d-block text-truncate">22 avril 2021 à 11:09</div>
                                </v-timeline-item>
                                <v-timeline-item color="error" fill-dot small>
                                    <strong class="d-block text-truncate">Produit supprimé</strong>
                                    <div class="caption d-block text-truncate">"Manteau polaire" a été supprimé</div>
                                    <div class="caption text--disabled d-block text-truncate">22 avril 2021 à 9:23</div>
                                </v-timeline-item>
                                <v-timeline-item color="primary" fill-dot small>
                                    <strong class="d-block text-truncate">Produit modifié</strong>
                                    <div class="caption d-block text-truncate">"Pantalon léger" a été modifié</div>
                                    <div class="caption text--disabled d-block text-truncate">22 avril 2021 à 10:10</div>
                                </v-timeline-item>
                                <v-timeline-item color="primary" fill-dot small>
                                    <strong class="d-block text-truncate">Produit modifié</strong>
                                    <div class="caption d-block text-truncate">"Robe soleil" a été modifié</div>
                                    <div class="caption text--disabled d-block text-truncate">22 avril 2021 à 9:56</div>
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
            isLoading: true,
            chartMonthlySales: {
                labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jui", "Aoû", "Sep", "Oct", "Nov", "Déc"],
                datasets: [
                    {
                        label: "Ventes du mois",
                        data: [0, 10, 200, 256, 10, 49, 244, 10, 229, 10, 66, 146],
                        backgroundColor: "#066bf9",
                        barPercentage: 0.25
                    },
                    {
                        label: "Ventes du mois dernier",
                        data: [0, 22, 65, 1, 221, 11, 65, 45, 87, 111, 23, 31],
                        backgroundColor: "#eee",
                        barPercentage: 0.25
                    }
                ]
            },
            chartWeeklySales: {
                labels: ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
                datasets: [
                    {
                        label: "Revenus de cette semaine",
                        data: [0, 10, 200, 256, 10, 49, 244, 10, 229, 10, 66, 146],
                        borderColor: "#066bf9",
                        backgroundColor: "#066bf9",
                        barPercentage: 0.25,
                        fill: false
                    },
                    {
                        label: "Revenus de la semaine dernière",
                        data: [0, 22, 65, 1, 221, 11, 65, 45, 87, 111, 23, 31],
                        borderColor: "#eee",
                        backgroundColor: "#eee",
                        barPercentage: 0.25,
                        fill: false
                    }
                ]
            },
            chartByLocation: [
                {name:'Canada', amount:300},
                {name:'Brazil', amount:140},
                {name:'France', amount:66}
            ],
            chartLowStocks: {
                labels: ["Stock Faible", "Total"],
                datasets: [
                    {
                        label: "Revenus de cette semaine",
                        data: [10, 90],
                        backgroundColor: ["#066bf9", "#eee"],
                        fill: true
                    }
                ]
            },
            chartOutStocks: {
                labels: ["Stock Épuisé", "Total"],
                datasets: [
                    {
                        label: "Revenus de cette semaine",
                        data: [2, 98],
                        backgroundColor: ["#066bf9", "#eee"],
                        fill: true
                    }
                ]
            },
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
            listBestsellers: [
                {
                    product_name: "Pull Geek & Félin",
                    product_price: "C$ 100.50",
                    product_quantity: 5,
                    product_amount: "C$ 502.50"
                },
                {
                    product_name: "Bombers Space No-Limit",
                    product_price: "C$ 50.00",
                    product_quantity: 4,
                    product_amount: "C$ 200.00"
                },
                {
                    product_name: "Coupe-vent mi-automne",
                    product_price: "C$ 10.00",
                    product_quantity: 3,
                    product_amount: "C$ 30.00"
                },
                {
                    product_name: "Sac à dos galaxie",
                    product_price: "C$ 100.00",
                    product_quantity: 2,
                    product_amount: "C$ 200.00"
                },
                {
                    product_name: "Manteau polaire",
                    product_price: "C$ 11.99",
                    product_quantity: 1,
                    product_amount: "C$ 11.99"
                },
                {
                    product_name: "Robe soleil",
                    product_price: "C$ 10.99",
                    product_quantity: 1,
                    product_amount: "C$ 10.99"
                },
                {
                    product_name: "Collier demi-lune",
                    product_price: "C$ 8.99",
                    product_quantity: 1,
                    product_amount: "C$ 8.99"
                },
                {
                    product_name: "Souvenirs d'outre-mer",
                    product_price: "C$ 3.99",
                    product_quantity: 1,
                    product_amount: "C$ 3.99"
                }
            ]
        }),
        mounted () {
            this.$set(this, "isLoading", false)
        }
    }
</script>