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
            <div v-if="isAuth && !hasEmptyCart" class="container">
                <v-row>
                    <div class="col-12 text-left">
                        <h2>{{ $i18n.t("YourQuotation") }}</h2>
                    </div>
                </v-row>
                <v-row>
                    <v-col cols="12">
                        <v-stepper v-model="hasStep" alt-labels>
                            <v-stepper-header>
                                <v-stepper-step :complete="hasStep > 1" :step="1">
                                    {{ $i18n.t("Cart") }}
                                </v-stepper-step>
                                <v-divider />
                                <v-stepper-step :complete="hasStep > 2" :step="2">
                                    {{ $i18n.t("Client") }}
                                </v-stepper-step>
                                <v-divider />
                                <v-stepper-step :complete="hasStep > 3" :step="3">
                                    {{ $i18n.t("Adresse") }}
                                </v-stepper-step>
                                <v-divider />
                                <v-stepper-step :complete="hasStep > 4" :step="4">
                                    {{ $i18n.t("Soumettre") }}
                                </v-stepper-step>
                            </v-stepper-header>
                            <v-stepper-items>
                                <v-stepper-content :step="1">
                                    <v-card>
                                        <v-card-title>
                                            <h4>{{ $i18n.t("Cart") }}</h4>
                                        </v-card-title>
                                        <v-card-text>
                                            <v-list>
                                                <v-list-item v-if="false">
                                                    <v-row class="align-items-center">
                                                        <v-col cols="12" md="6" class="text-left">
                                                            {{ $i18n.t("Product") }}
                                                        </v-col>
                                                        <v-col cols="10" md="3" class="text-center">
                                                            {{ $i18n.t("Quantity") }}
                                                        </v-col>
                                                        <v-col cols="2" md="3" class="text-right">
                                                            {{ $i18n.t("Remove") }}
                                                        </v-col>
                                                    </v-row>
                                                </v-list-item>
                                                <template v-for="(item, n) in listProducts">
                                                    <v-divider v-if="n > 0" :key="'divider-'+item.product_code+'-' + n" />
                                                    <v-list-item :key="'product-' + n">
                                                        <v-row class="align-items-center">
                                                            <v-col cols="2" md="1" class="text-center">
                                                                <a :href="item.product_url">
                                                                    <v-img :src="item.product_image" :alt="item.product_name" />
                                                                </a>
                                                            </v-col>
                                                            <v-col cols="10" md="5" class="text-left">
                                                                <a :href="item.product_url">
                                                                    <span v-text="item.product_name"></span>
                                                                </a>
                                                            </v-col>
                                                            <v-col cols="10" md="3" class="text-center">
                                                                <v-text-field
                                                                    v-model="item.quantity"
                                                                    :rules="[
                                                                        (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                                    ]"
                                                                    hide-details="auto"
                                                                    dense
                                                                    required
                                                                    filled
                                                                >
                                                                    <template v-slot:prepend>
                                                                        <v-btn tile icon outlined x-small color="primary" @click="doMinus(n)">
                                                                            <v-icon x-small>mdi-minus</v-icon>
                                                                        </v-btn>
                                                                    </template>
                                                                    <template v-slot:append-outer>
                                                                        <v-btn tile icon outlined x-small color="primary" @click="doPlus(n)">
                                                                            <v-icon x-small>mdi-plus</v-icon>
                                                                        </v-btn>
                                                                    </template>
                                                                </v-text-field>
                                                            </v-col>
                                                            <v-col cols="2" md="3" class="text-right">
                                                                <v-btn small icon color="error" @click="setQuotationDelete(item.id)">
                                                                    <v-icon>mdi-delete</v-icon>
                                                                </v-btn>
                                                            </v-col>
                                                        </v-row>
                                                    </v-list-item>
                                                </template>
                                            </v-list>
                                        </v-card-text>
                                        <v-card-actions>
                                            <v-row>
                                                <v-col cols="12" class="text-right">
                                                    <v-btn tile color="primary" @click="doStepNext()">
                                                        <v-icon v-if="$vuetify.breakpoint.name == 'sm' || $vuetify.breakpoint.name == 'xs'">mdi-chevron-right</v-icon>
                                                        <span v-else>{{ $i18n.t("Suivant") }}</span>
                                                    </v-btn>
                                                </v-col>
                                            </v-row>
                                        </v-card-actions>
                                    </v-card>
                                </v-stepper-content>
                                <v-stepper-content :step="2">
                                    <v-card>
                                        <v-card-title>
                                            <h4>{{ $i18n.t("Detailsduclient") }}</h4>
                                        </v-card-title>
                                        <v-card-text>
                                            <v-form v-model="formCustomer.valid">
                                                <v-row>
                                                    <v-col cols="12" md="6">
                                                        <v-select
                                                        v-model="formCustomer.customer.salutation"
                                                        :label="$i18n.t('Salutation')"
                                                        placeholder=" "
                                                        :items="formChoix.salutation"
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="formError.customer.salutation"
                                                        required
                                                        filled
                                                        attach
                                                        @keydown="formError.customer.salutation = null"
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formCustomer.customer.email"
                                                        :label="$i18n.t('Courriel')"
                                                        placeholder=" "
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="formError.customer.email"
                                                        required
                                                        filled
                                                        @keydown="formError.customer.email = null"
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formCustomer.customer.first_name"
                                                        :label="$i18n.t('Prenom')"
                                                        placeholder=" "
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="formError.customer.first_name"
                                                        required
                                                        filled
                                                        @keydown="formError.customer.first_name = null"
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formCustomer.customer.last_name"
                                                        :label="$i18n.t('Nomdefamille')"
                                                        placeholder=" "
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="formError.customer.last_name"
                                                        required
                                                        filled
                                                        @keydown="formError.customer.last_name = null"
                                                        />
                                                    </v-col>
                                                </v-row>
                                            </v-form>
                                        </v-card-text>
                                        <v-card-actions>
                                            <v-row>
                                                <v-col cols="6" class="text-left">
                                                    <v-btn tile color="primary" @click="doStepPrev()">
                                                        <v-icon v-if="$vuetify.breakpoint.name == 'sm' || $vuetify.breakpoint.name == 'xs'">mdi-chevron-left</v-icon>
                                                        <span v-else>{{ $i18n.t("Precedent") }}</span>
                                                    </v-btn>
                                                </v-col>
                                                <v-col cols="6" class="text-right">
                                                    <v-btn
                                                        tile
                                                        color="primary"
                                                        :disabled="!formCustomer.valid"
                                                        @click="doStepNext()"
                                                    >
                                                        <v-icon v-if="$vuetify.breakpoint.name == 'sm' || $vuetify.breakpoint.name == 'xs'">mdi-chevron-right</v-icon>
                                                        <span v-else>{{ $i18n.t("Suivant") }}</span>
                                                    </v-btn>
                                                </v-col>
                                            </v-row>
                                        </v-card-actions>
                                    </v-card>
                                </v-stepper-content>
                                <v-stepper-content :step="3">
                                    <v-card>
                                        <v-card-title>
                                            <h4>{{ $i18n.t("Adressedelivraison") }}</h4>
                                        </v-card-title>
                                        <v-card-text>
                                            <v-form v-model="formShipping.valid">
                                                <v-row>
                                                    <v-col cols="12">
                                                        <v-text-field
                                                        v-model="formShipping.shipping_address.name"
                                                        :label="$i18n.t('Nomcomplet')"
                                                        placeholder=" "
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="formError.shipping_address.name"
                                                        required
                                                        filled
                                                        @keydown="formError.shipping_address.name = null"
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formShipping.shipping_address.address1"
                                                        :label="$i18n.t('Adresse')"
                                                        placeholder=" "
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="
                                                            formError.shipping_address.address1
                                                        "
                                                        required
                                                        filled
                                                        @keydown="
                                                            formError.shipping_address.address1 = null
                                                        "
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formShipping.shipping_address.address2"
                                                        :label="$i18n.t('Adressesuite')"
                                                        placeholder=" "
                                                        filled
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-autocomplete
                                                        v-model="formShipping.shipping_address.country"
                                                        :label="$i18n.t('Pays')"
                                                        placeholder=" "
                                                        :rules="[(v) => !!v || $i18n.t('Cechampsesrrequis')]"
                                                        :items="formChoix.countries"
                                                        :item-text="'name'"
                                                        :item-value="'alpha2'"
                                                        :error-messages="formError.shipping_address.country"
                                                        required
                                                        filled
                                                        attach
                                                        @keydown="formError.shipping_address.country = null"
                                                        @change="formShipping.shipping_address.province = null"
                                                        />
                                                    </v-col>
                                                    <v-col v-if="formShipping.shipping_address.country == 'CA'" cols="12" md="6">
                                                        <v-autocomplete
                                                        v-model="formShipping.shipping_address.province"
                                                        :label="$i18n.t('Province')"
                                                        placeholder=" "
                                                        :rules="[(v) => !!v || $i18n.t('Cechampsesrrequis')]"
                                                        :items="formChoix.provincesCA"
                                                        :item-text="'name'"
                                                        :item-value="'alpha2'"
                                                        :error-messages="formError.shipping_address.province"
                                                        required
                                                        filled
                                                        attach
                                                        @keydown="formError.shipping_address.province = null"
                                                        />
                                                    </v-col>
                                                    <v-col v-else cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formShipping.shipping_address.province"
                                                        :label="$i18n.t('Province')"
                                                        placeholder=" "
                                                        :rules="[(v) => !!v || $i18n.t('Cechampsesrrequis'),]"
                                                        :error-messages="formError.shipping_address.province"
                                                        required
                                                        filled
                                                        @keydown="formError.shipping_address.province = null"
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formShipping.shipping_address.city"
                                                        :label="$i18n.t('Ville')"
                                                        placeholder=" "
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="formError.shipping_address.city"
                                                        required
                                                        filled
                                                        @keydown="formError.shipping_address.city = null"
                                                        />
                                                    </v-col>
                                                    <v-col cols="12" md="6">
                                                        <v-text-field
                                                        v-model="formShipping.shipping_address.zip_code"
                                                        :label="$i18n.t('Codepostal')"
                                                        placeholder=" "
                                                        :rules="[
                                                            (v) => !!v || $i18n.t('Cechampsesrrequis'),
                                                        ]"
                                                        :error-messages="
                                                            formError.shipping_address.zip_code
                                                        "
                                                        required
                                                        filled
                                                        @keydown="
                                                            formError.shipping_address.zip_code = null
                                                        "
                                                        />
                                                    </v-col>
                                                </v-row>
                                            </v-form>
                                        </v-card-text>
                                        <v-card-actions>
                                            <v-row>
                                                <v-col cols="6" class="text-left">
                                                    <v-btn tile color="primary" @click="doStepPrev()">
                                                        <v-icon v-if="$vuetify.breakpoint.name == 'sm' || $vuetify.breakpoint.name == 'xs'">mdi-chevron-left</v-icon>
                                                        <span v-else>{{ $i18n.t("Precedent") }}</span>
                                                    </v-btn>
                                                </v-col>
                                                <v-col cols="6" class="text-right">
                                                    <v-btn
                                                        tile
                                                        color="primary"
                                                        :disabled="!formShipping.valid"
                                                        @click="doStepNext()"
                                                    >
                                                        <v-icon v-if="$vuetify.breakpoint.name == 'sm' || $vuetify.breakpoint.name == 'xs'">mdi-chevron-right</v-icon>
                                                        <span v-else>{{ $i18n.t("Suivant") }}</span>
                                                    </v-btn>
                                                </v-col>
                                            </v-row>
                                        </v-card-actions>
                                    </v-card>
                                </v-stepper-content>
                                <v-stepper-content :step="4">
                                    <v-card>
                                        <v-card-text>
                                            <template v-if="isLoadingSubmit">
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
                                                    <v-col v-if="isCompleted" cols="12">
                                                        <h4>{{ $i18n.t("Thanksforquotation") }}</h4>
                                                        <h3>{{ $i18n.t("Thanks") }}</h3>
                                                        <p>
                                                            <a href="/">{{ $i18n.t("Retourneralaccueil") }}</a>
                                                        </p>
                                                    </v-col>
                                                    <v-col v-else cols="12">
                                                        <v-btn x-large color="primary" @click="doQuotationSubmit()">
                                                            Soumettre
                                                        </v-btn>
                                                    </v-col>
                                                </v-row>
                                                <v-row v-if="hasError || hasSuccess">
                                                    <v-col cols="12">
                                                        <v-alert v-if="!hasError && hasSuccess" text type="success">
                                                            <div v-html="hasSuccess"></div>
                                                        </v-alert>
                                                        <v-alert v-else-if="hasError" text type="error">
                                                            <div v-html="hasError"></div>
                                                        </v-alert>
                                                    </v-col>
                                                </v-row>
                                            </template>
                                        </v-card-text>
                                    </v-card>
                                </v-stepper-content>
                            </v-stepper-items>
                        </v-stepper>
                    </v-col>
                </v-row>
            </div>
            <div v-else-if="!isAuth && !hasEmptyCart">
                <dm-auth @is-auth="setAuth()" />
            </div>
            <div v-else>
                <v-row class="pa-6">
                    <v-col cols="12" class="py-6">
                        <h3 class="py-6">{{ $i18n.t("Votrepanierestvide") }}</h3>
                        <p>
                            <a href="/">{{ $i18n.t("Retourneralaccueil") }}</a>
                        </p>
                    </v-col>
                </v-row>
            </div>
        </template>
    </div>
</template>

<script>
    import countries from "@/data/countries";
    import provincesCA from "@/data/provincesCA";
    export default {
        name: "Quotation",
        components: {
            dmAuth: () => import("@/components/Auth.vue"),
        },
        data: () => ({
            isAuth: false,
            isLoading: true,
            isLoadingSubmit: false,
            isCompleted: false,
            hasError: null,
            hasSuccess: null,
            hasEmptyCart: false,
            hasStep: 1,
            isGuest: false,
            tosLink: "/",
            quotationID : null,
            quotationNumber : null,
            currentQuotation: null,
            listProducts: [],
            formChoix: {
                salutation: [],
                shippingAddress: [],
                countries: [],
                provincesCA: [],
            },
            formCustomer: {
                valid: false,
                customer: {
                    plugin_order: 1,
                    salutation: null,
                    first_name: null,
                    last_name: null,
                    email: null,
                },
            },
            formShipping: {
                valid: false,
                shipping_address: {
                    plugin_order: 1,
                    active_priority: 1,
                    name: null,
                    address1: null,
                    address2: null,
                    city: null,
                    province: null,
                    country: null,
                    zip_code: null,
                    siblings_summary: [],
                },
            },
            formError: {
                customer: {
                    salutation: null,
                    first_name: null,
                    last_name: null,
                    email: null,
                },
                shipping_address: {
                    name: null,
                    address1: null,
                    address2: null,
                    city: null,
                    province: null,
                    country: null,
                    zip_code: null,
                }
            },
        }),
        mounted() {
            // ===--- hide toggle cart
            if (document.getElementById("dshop-toggle-cart")) {
                document.getElementById("dshop-toggle-cart").style.display = "none"
            }
            // ===---
            if (this.$vuetify.lang.current === "fr") {
                this.$set(this.formChoix, "countries", countries[0][this.$vuetify.lang.current])
                this.$set(this.formChoix, "provincesCA", provincesCA[0][this.$vuetify.lang.current])
            } else {
                this.$set(this.formChoix, "countries", countries[1][this.$vuetify.lang.current])
                this.$set(this.formChoix, "provincesCA", provincesCA[1][this.$vuetify.lang.current])
            }
            this.$set(this.formChoix, "salutation", [
                { text: this.$i18n.t("Madame"), value: "mrs" },
                { text: this.$i18n.t("Monsieur"), value: "mr" },
                { text: this.$i18n.t("Preferepasrepondre"), value: "na" },
            ]);
            this.getCustomer();
        },
        methods: {
            setAuth() {
                this.$set(this, "isAuth", true);
                this.getCustomer();
            },
            /* =========================================================== //
            // ===---   getCustomer                                 ---=== //
            // =========================================================== */
            getCustomer () {
                let self = this;
                this.$set(this, "isLoading", true)
                // ===--- BEGIN: axios
                this.$axios.get(this.$web_url + "/api/fe/customer/", {
                        headers: {
                            "Content-Type": "application/json",
                            Accept: "application/json",
                        },
                    })
                    .then((apiSuccess) => {
                        // set customer form
                        if (apiSuccess.data.customer) {
                            self.$set(
                            self.formCustomer.customer,
                            "salutation",
                            apiSuccess.data.customer.salutation
                                ? apiSuccess.data.customer.salutation
                                : ""
                            );
                            self.$set(
                            self.formCustomer.customer,
                            "first_name",
                            apiSuccess.data.customer.first_name
                                ? apiSuccess.data.customer.first_name
                                : ""
                            );
                            self.$set(
                            self.formCustomer.customer,
                            "last_name",
                            apiSuccess.data.customer.last_name
                                ? apiSuccess.data.customer.last_name
                                : ""
                            );
                            self.$set(
                            self.formCustomer.customer,
                            "email",
                            apiSuccess.data.customer.email
                                ? apiSuccess.data.customer.email
                                : ""
                            );
                        }
                        // set shipping address form
                        if (apiSuccess.data.address_shipping) {
                            self.$set(self.formShipping, "shipping_address", apiSuccess.data.address_shipping);
                        }
                        // ===---
                        self.$set(self, "isGuest", apiSuccess.data.customer.guest ? true : false);
                        self.$set(self, "tosLink", apiSuccess.data.tos ? apiSuccess.data.tos : "/")
                        // ===---
                        self.getQuotationCart();
                    })
                    .catch(() => {
                        self.$set(self, "isLoading", false)
                    });
                // ===--- END: axios
            },
            /* =========================================================== //
            // ===---   getQuotationCart                            ---=== //
            // =========================================================== */
            getQuotationCart () {
                let self = this;
                // ===--- BEGIN: axios
                this.$axios
                    .get(this.$web_url + "/quotation/current/", {
                        headers: {
                            "Content-Type": "application/json",
                            Accept: "application/json",
                        },
                    })
                    .then((apiSuccess) => {
                        if (apiSuccess.data && apiSuccess.data && apiSuccess.data.quotation) {
                            self.$set(self, "listProducts", apiSuccess.data.quotation.items)
                            self.$set(self, "quotationID", apiSuccess.data.quotation.id)
                            self.$set(self, "quotationNumber", apiSuccess.data.quotation.number)
                        } else {
                            self.$set(self, "hasEmptyCart", true)
                        }
                        self.$set(self, "isLoading", false)
                    })
                    .catch(() => {
                        self.$set(self, "hasEmptyCart", true)
                        self.$set(self, "isLoading", false)
                    });
                // ===--- END: axios
            },
            /* =========================================================== //
            // ===---   doProcess                                   ---=== //
            // =========================================================== */
            doProcess () {
                let self = this
                this.$set(this, "hasError", null)
                this.$set(this, "hasSuccess", null)
                // ===---
                let datas = null
                // ===---
                if (this.hasStep === 1) {
                    this.listProducts.forEach((item) => {
                        self.setQuotationQuantity(item.id, item.quantity)
                    })
                    this.$set(this, "hasStep", this.hasStep + 1)
                } else if (this.hasStep === 2) {
                    datas = this.formCustomer
                    this.doPreUpload(datas)
                } else if (this.hasStep === 3) {
                    datas = {
                        shipping_address: this.formShipping.shipping_address
                    }
                    this.doPreUpload(datas)
                }
                this.$vuetify.goTo(100)
            },
            /* =========================================================== //
            // ===---   setQuotationQuantity                        ---=== //
            // =========================================================== */
            setQuotationQuantity (id, quantity) {
                let self = this
                this.$set(this, "hasError", null)
                // ===---
                let datas = {
                    "quantity": quantity
                }
                // ===--- BEGIN: axios
                this.$axios.patch(this.$web_url + "/quotation/item/"+id, datas, {
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                })
                .then(() => {})
                .catch(() => {
                    self.$set(self, "hasError", self.$i18n.t("Anerroroccured"))
                })
                // ===--- END: axios
            },
            /* =========================================================== //
            // ===---   setQuotationQuantity                        ---=== //
            // =========================================================== */
            setQuotationDelete (id) {
                let self = this
                this.$set(this, "hasError", null)
                // ===--- BEGIN: axios
                this.$axios.delete(this.$web_url + "/quotation/item/"+id, {
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                })
                .then(() => {
                    self.getQuotationCart()
                })
                .catch(() => {
                    self.$set(self, "hasError", self.$i18n.t("Anerroroccured"))
                })
                // ===--- END: axios
            },
            /* =========================================================== //
            // ===---   doPreUpload & doUpload                      ---=== //
            // =========================================================== */
            doPreUpload (datas) {
                let self = this
                // ===--- check user email
                if (this.hasStep === 1 && this.isGuest) {
                    let data_email = {
                        email: this.formCustomer.customer.email
                    }
                    // ===--- BEGIN: axios
                    this.$axios.post(this.$web_url+'/api/fe/customer-check/', data_email, {
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
                    })
                    .then((apiSuccess) => {
                        if (apiSuccess.data.exist) {
                            self.$set(self.formError.customer, 'email', self.$i18n.t("Thisemailexist"))
                        } else {
                            self.doUpload(datas)
                        }
                    })
                    .catch(() => {
                        self.$set(self.formError.customer, 'email', self.$i18n.t("Anerroroccured"))
                    })
                    // ===--- END: axios
                } else {
                    this.doUpload(datas)
                }
            },
            doUpload (datas) {
                let self = this
                // ===--- BEGIN: axios
                this.$axios.put(this.$api_url+'/checkout/upload/', datas, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                })
                .then(() => {
                    self.$set(self, 'hasStep', self.hasStep + 1)
                })
                .catch((apiFail) => {
                    self.$set(self, 'isLoadingPayment', false)
                    if (apiFail.response && apiFail.response.data) {
                        if (apiFail.response.data.customer_form) {
                            self.$set(self.formError.customer, 'salutation', apiFail.response.data.customer_form.salutation ? apiFail.response.data.customer_form.salutation : null)
                            self.$set(self.formError.customer, 'first_name', apiFail.response.data.customer_form.first_name ? apiFail.response.data.customer_form.first_name : null)
                            self.$set(self.formError.customer, 'last_name', apiFail.response.data.customer_form.last_name ? apiFail.response.data.customer_form.last_name : null)
                            self.$set(self.formError.customer, 'email', apiFail.response.data.customer_form.email ? apiFail.response.data.customer_form.email : null)
                        }
                    }
                })
                // ===--- END: axios
            },
            /* =========================================================== //
            // ===---   doQuotationSubmit                           ---=== //
            // =========================================================== */
            doQuotationSubmit () {
                let self = this
                this.$set(this, "hasError", null)
                this.$set(this, "isCompleted", false)
                this.$set(this, "isLoadingSubmit", true)
                // ===---
                let datas = {
                    "id": this.quotationID,
                    "status": 2
                }
                // ===---
                if (this.quotationID && this.quotationNumber) {
                    // ===--- BEGIN: axios
                    this.$axios.patch(this.$web_url + "/quotation/number/"+this.quotationID, datas, {
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        }
                    })
                    .then(() => {
                        self.$set(self, "isCompleted", true)
                        self.$set(self, "isLoadingSubmit", false)
                    })
                    // ===--- END: axios
                } else {
                    this.$set(this, "hasError", this.$i18n.t("Anerroroccured"))
                    this.$set(this, "isLoadingSubmit", false)
                }
            },
            /* =========================================================== //
            // ===---   doMinus & doPlus                            ---=== //
            // =========================================================== */
            doMinus (item) {
                if (this.listProducts[item].quantity > 1) {
                    this.$set(this.listProducts[item], "quantity", this.listProducts[item].quantity - 1)
                }
            },
            doPlus (item) {
                this.$set(this.listProducts[item], "quantity", this.listProducts[item].quantity + 1)
            },
            /* =========================================================== //
            // ===---   doStepPrev & doStepNext                     ---=== //
            // =========================================================== */
            doStepPrev () {
                this.$set(this, "hasError", null)
                this.$set(this, "hasSuccess", null)
                this.$set(this, "hasStep", this.hasStep - 1)
            },
            doStepNext () {
                this.doProcess()
            }
            /* =========================================================== //
            // ===-----------------------------------------------------=== //
            // =========================================================== */
        }
    }
</script>
