<template>
  <div id="frontend-soumission" class="checkout">
    <div v-if="isAuth && !hasEmptyCart" class="container">
      <v-row>
        <div class="col-12 text-left">
          <h2>Soumissionner</h2>
        </div>
      </v-row>
      <v-row v-if="!hasSuccessSoumission">
        <v-col cols="12">
          <v-stepper v-model="stepCheckout" alt-labels>
            <v-stepper-header>
              <v-stepper-step :complete="stepCheckout > 1" :step="1">
                {{$i18n.t('Client')}}
              </v-stepper-step>
              <v-divider />
              <v-stepper-step :complete="stepCheckout > 2" :step="2">
                {{$i18n.t('Livraison')}}
              </v-stepper-step>
              <v-divider />
              <v-stepper-step :complete="stepCheckout > 3" :step="3">
                {{$i18n.t('Soumission')}}
              </v-stepper-step>
            </v-stepper-header>
            <v-stepper-items>
              <v-stepper-content :step="1">
                <v-card>
                  <v-card-title>
                    <h4>{{$i18n.t('Detailsduclient')}}</h4>
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
                            v-model="formCustomer.customer.email"
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
                            v-model="formCustomer.customer.first_name"
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
                            v-model="formCustomer.customer.last_name"
                            :label="$i18n.t('Nomdefamille')"
                            placeholder=" "
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                            :error-messages="formError.customer.last_name"
                            required
                            filled
                            @keydown="formError.customer.last_name = null"
                          />
                        </v-col>
                        <v-col>
                          <v-text-field
                            v-model="formCustomer.customer.phone"
                            :label="$i18n.t('Telephone')"
                            placeholder="(facultatif)"
                            :error-messages="formError.customer.phone"
                            filled
                            @keydown="formError.customer.phone = null"
                          />
                        </v-col>
                      </v-row>
                    </v-form>
                  </v-card-text>
                  <v-card-actions>
                    <v-row>
                      <v-col cols="12" class="text-right">
                        <v-btn tile color="primary" :disabled="!formCustomer.valid" @click="nextStep()">{{$i18n.t('Suivant')}}</v-btn>
                      </v-col>
                    </v-row>
                  </v-card-actions>
                </v-card>
              </v-stepper-content>
              <v-stepper-content :step="2">
                <v-card>
                  <v-card-title>
                    <h4>{{$i18n.t('Methodesdexpedition')}}</h4>
                  </v-card-title>
                  <v-card-text>
                    <v-form v-model="formShippingMethod.valid">
                      <v-row>
                        <v-col v-if="formChoix.shippingMethods.length > 0" cols="12">
                          <v-radio-group
                            v-model="formShippingMethod.shipping_method.shipping_modifier"
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                            required
                          >
                            <v-radio
                              v-for="(item, n) in formChoix.shippingMethods"
                              :key="n"
                              :label="item[1]"
                              :value="item[0]"
                            />
                          </v-radio-group>
                        </v-col>
                        <v-col v-else cols="12">
                          <v-alert text color="error">
                            {{$i18n.t('Nomethodesdexpedition')}}
                          </v-alert>
                        </v-col>
                      </v-row>
                    </v-form>
                  </v-card-text>
                  <v-card-title>
                    <h4>{{$i18n.t('Adressedelivraison')}}</h4>
                  </v-card-title>
                  <v-card-text>
                    <v-form v-model="formShipping.valid">
                      <v-row>
                        <v-col cols="12">
                          <v-text-field
                            v-model="formShipping.shipping_address.name"
                            :label="$i18n.t('Nomcomplet')"
                            placeholder=" "
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
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
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                            :error-messages="formError.shipping_address.address1"
                            required
                            filled
                            @keydown="formError.shipping_address.address1 = null"
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
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                            :items="formChoix.countries"
                            :item-text="'name'"
                            :item-value="'alpha2'"
                            :error-messages="formError.shipping_address.country"
                            required
                            filled
                            attach
                            @keydown="formError.shipping_address.country = null"
                          />
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-text-field
                            v-model="formShipping.shipping_address.province"
                            :label="$i18n.t('Province')"
                            placeholder=" "
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
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
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
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
                            :rules="[v => !!v || $i18n.t('Cechampsesrrequis')]"
                            :error-messages="formError.shipping_address.zip_code"
                            required
                            filled
                            @keydown="formError.shipping_address.zip_code = null"
                          />
                        </v-col>
                      </v-row>
                    </v-form>
                  </v-card-text>
                  <v-card-actions>
                    <v-row>
                      <v-col cols="12" sm="6" class="text-left">
                        <v-btn tile color="primary" @click="prevStep()">{{$i18n.t('Precedent')}}</v-btn>
                      </v-col>
                      <v-col cols="12" sm="6" class="text-right">
                        <v-btn tile color="primary" :disabled="!formShippingMethod.shipping_method.shipping_modifier || !formShipping.valid" @click="nextStep()">{{$i18n.t('Suivant')}}</v-btn>
                      </v-col>
                    </v-row>
                  </v-card-actions>
                </v-card>
              </v-stepper-content>
              <v-stepper-content :step="3">
                <v-card>
                  <v-card-title>
                    <h4>{{$i18n.t('Soumission')}}</h4>
                  </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" class="text-left">
                        <v-list class="dm-payment-products">
                          <template v-for="(item, n) in formPayment.listProducts">
                            <v-divider v-if="n > 0" :key="'divider-'+n" />
                            <v-list-item :key="'product-'+n">
                              <v-list-item-content class="dm-payment-produit">
                                <div class="dm-payment-mobiletitle">{{$i18n.t('Produit')}}</div>
                                <div v-html="item.summary.media"></div>
                              </v-list-item-content>
                              <v-list-item-action class="dm-payment-price">
                                <div class="dm-payment-mobiletitle">{{$i18n.t('Prix')}}</div>
                                <div class="pb-3">À partir de <span v-html="item.summary.price"></span></div>
                                <div class="dm-payment-mobiletitle">{{$i18n.t('Quantity')}}</div>
                                <div class="dm-soumission-quantity">
                                  <span class="dm-minus" @click="updateQuantity('minus', n)">-</span>
                                  <span class="dm-quantity" v-html="item.quantity"></span>
                                  <span class="dm-plus" @click="updateQuantity('plus', n)">+</span>
                                </div>
                              </v-list-item-action>
                            </v-list-item>
                          </template>
                        </v-list>
                      </v-col>
                      <v-col cols="12" class="text-right">
                        <v-checkbox
                          v-model="formAcceptCondition.accept_condition.plugin_1.accept"
                          :label="$i18n.t('Jailuetjaccepte')"
                          hide-details
                          required
                          class="align-center justify-md-end mb-5"
                        />
                      </v-col>
                      <v-col v-if="hasErrorPayment" cols="12">
                        <v-alert text type="error">
                          <div v-html="hasErrorPayment"></div>
                        </v-alert>
                      </v-col>
                    </v-row>
                  </v-card-text>
                  <v-card-actions>
                    <v-row>
                      <v-col cols="12" sm="6" class="text-left">
                        <v-btn tile color="primary" @click="prevStep()">{{$i18n.t('Precedent')}}</v-btn>
                      </v-col>
                      <v-col cols="12" sm="6" class="text-right">
                        <v-btn tile color="primary" :loading="isLoadingSoumission" :disabled="!formAcceptCondition.accept_condition.plugin_1.accept" @click="setUpload()">{{$i18n.t('Soumissionner')}}</v-btn>
                      </v-col>
                    </v-row>
                  </v-card-actions>
                </v-card>
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
        </v-col>
      </v-row>
      <v-row v-else>
        <v-col cols="12">
          <v-alert text type="success">
            <p>Votre soumission à bien été envoyée.<br />Vous recevrez un courriel sous peu.</p>
            <p class="mb-0"><a href="/">{{$i18n.t('Retourneralaccueil')}}</a></p>
          </v-alert>
        </v-col>
      </v-row>
    </div>
    <div v-else-if="!isAuth && !hasEmptyCart">
      <dm-auth @is-auth="setAuth()" />
    </div>
    <div v-else>
      <v-row class="pa-6">
        <v-col cols="12" class="py-6">
          <h3 class="py-6">{{$i18n.t('Votrepanierestvide')}}</h3>
          <p><a href="/">{{$i18n.t('Retourneralaccueil')}}</a></p>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
  import countries from '@/data/countries'
  export default {
    name: 'Soumission',
    components: {
      dmAuth: () => import('@/components/Auth.vue')
    },
    data: () => ({
      isAuth: false,
      isLoadingSoumission: false,
      hasEmptyCart: false,
      hasErrorPayment: null,
      hasSuccessSoumission: false,
      stepCheckout: 1,
      formChoix: {
        salutation: [],
        shippingAddress: [],
        countries: [],
        provinces: [],
        shippingMethods: [],
        billingMethods: []
      },
      formCustomer: {
        valid: false,
        customer: {
          plugin_order: 1,
          salutation: null,
          first_name: null,
          last_name: null,
          email: null,
          phone: ''
        }
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
          siblings_summary: []
        },
      },
      formShippingMethod: {
        valid: false,
        shipping_method: {
          plugin_order: 1,
          shipping_modifier: null
        }
      },
      formAcceptCondition:{
        valid: false,
        accept_condition: {
          plugin_1: {
            accept: false,
            plugin_id: 1,
            plugin_order: 1
          }
        }
      },
      formPayment: {
        productsCount: 0,
        productsQuantity: 0,
        subtotal: "C$ 0.00",
        total: "C$ 0.00",
        listExtras: [],
        listProducts: []
      },
      formError: {
        customer: {
          salutation: null,
          first_name: null,
          last_name: null,
          email: null,
          phone: null
        },
        shipping_address: {
          name: null,
          address1: null,
          address2: null,
          city: null,
          province: null,
          country: null,
          zip_code: null
        }
      },
      asCurrentAddress: false,
      tagCustomer: '',
      tagShippingAddress: '',
      tagBillingAddress: '',
      tagShippingMethod: '',
      tagBillingMethod: '',
      tagNote: ''
    }),
    mounted () {
      if (this.$vuetify.lang.current === 'fr') {
        this.$set(this.formChoix, 'countries', countries[0][this.$vuetify.lang.current])
      } else {
        this.$set(this.formChoix, 'countries', countries[1][this.$vuetify.lang.current])
      }
      this.$set(this.formChoix, 'salutation', [
        {text: this.$i18n.t('Madame'),value: 'mrs'},
        {text: this.$i18n.t('Monsieur'),value: 'mr'},
        {text: this.$i18n.t('Preferepasrepondre'),value: 'na'}
      ])
      this.getCustomer()
      this.getShippingMethods()
    },
    methods: {
      setAuth () {
        this.$set(this, 'isAuth', true)
      },
      /* =========================================================== //
      // ===---   getCustomer                                 ---=== //
      // =========================================================== */
      getCustomer () {
        let self = this
        // ===--- BEGIN: axios
        this.$axios.get(this.$web_url+'/api/fe/customer/', {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then((apiSuccess) => {
          // set customer form
          if (apiSuccess.data.customer) {
            self.$set(self.formCustomer.customer, 'salutation', apiSuccess.data.customer.salutation ? apiSuccess.data.customer.salutation : '')
            self.$set(self.formCustomer.customer, 'first_name', apiSuccess.data.customer.first_name ? apiSuccess.data.customer.first_name : '')
            self.$set(self.formCustomer.customer, 'last_name', apiSuccess.data.customer.last_name ? apiSuccess.data.customer.last_name : '')
            self.$set(self.formCustomer.customer, 'email', apiSuccess.data.customer.email ? apiSuccess.data.customer.email : '')
          }
          // set shipping address form
          if (apiSuccess.data.address_shipping) {
            self.$set(self.formShipping, 'shipping_address', apiSuccess.data.address_shipping)
          }
          self.getDigest()
        })
        .catch(() => {})
        // ===--- END: axios
      },
      /* =========================================================== //
      // ===---   getShippingMethods                          ---=== //
      // =========================================================== */
      getShippingMethods () {
        let self = this
        // ===--- BEGIN: axios
        this.$axios.get(this.$web_url+'/api/fe/shipping-methods/', {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then((apiSuccess) => {
          if (apiSuccess.data.shipping_methods.length > 0) {
            apiSuccess.data.shipping_methods.forEach((item) => {
              if (item[0] !== null && item[1] !== null) {
                self.formChoix.shippingMethods.push(item)
              }
            })
            if (self.formChoix.shippingMethods.length > 0) {
              self.$set(self.formShippingMethod.shipping_method, 'shipping_modifier', self.formChoix.shippingMethods[0][0])
            }
          }
        })
        .catch(() => {})
        // ===--- END: axios
      },
      /* =========================================================== //
      // ===---   setUpload                                   ---=== //
      // =========================================================== */
      setUpload (next = false) {
        let self = this
        let datas = null
        if (this.stepCheckout === 1) {
          datas = this.formCustomer
        } else if (this.stepCheckout === 2) {
          datas = {
            shipping_address: this.formShipping.shipping_address,
            shipping_method: this.formShippingMethod.shipping_method
          }
        } else if (this.stepCheckout === 3) {
          datas = this.formAcceptCondition
        }
        // ===--- BEGIN: axios
        this.$axios.put(this.$api_url+'/checkout/upload/', datas, {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then(() => {
          self.getDigest()
          if (next) {
            // if button 'next' was clicked, go to next step
            self.$vuetify.goTo(100)
            self.$set(self, 'stepCheckout', self.stepCheckout + 1)
          } else if (self.stepCheckout === 3) {
            // if all is okay, purchase
            self.doSoumission()
          }
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
        })
        // ===--- END: axios
      },
      /* =========================================================== //
      // ===---   getDigest                                   ---=== //
      // =========================================================== */
      getDigest () {
        let self = this
        // ===--- BEGIN: axios
        this.$axios.get(this.$api_url+'/checkout/digest/', {
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        })
        .then((apiSuccess) => {
          self.getWatch()
          if (apiSuccess.data && apiSuccess.data.checkout_digest) {
            self.$set(self, 'tagCustomer', apiSuccess.data.checkout_digest.customer_tag)
            self.$set(self, 'tagShippingAddress', apiSuccess.data.checkout_digest.shipping_address_tag)
            self.$set(self, 'tagBillingAddress', apiSuccess.data.checkout_digest.billing_address_tag)
            self.$set(self, 'tagShippingMethod', apiSuccess.data.checkout_digest.shipping_method_tag)
            self.$set(self, 'tagBillingMethod', apiSuccess.data.checkout_digest.payment_method_tag)
            self.$set(self, 'tagNote', apiSuccess.data.checkout_digest.extra_annotation_tag)
          }
        })
        .catch(() => {})
        // ===--- END: axios
      },
      getWatch () {
        if (this.formPayment.listProducts.length == 0) {
          let self = this
          // ===--- BEGIN: axios
          this.$axios.get(this.$api_url+'/watch/', {
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
          })
          .then((apiSuccess) => {
            if (apiSuccess.data && apiSuccess.data.items) {
              if (apiSuccess.data.items.length > 0) {
                self.$set(self.formPayment, 'productsCount', apiSuccess.data.items.length)
                self.$set(self.formPayment, 'productsQuantity', apiSuccess.data.items.length)
                self.$set(self.formPayment, 'subtotal', 0)
                self.$set(self.formPayment, 'total', 0)
                self.$set(self.formPayment, 'listExtras', "")
                self.$set(self.formPayment, 'listProducts', apiSuccess.data.items)
              } else {
                self.$set(self, 'hasEmptyCart', true)
              }
            }
          })
          .catch(() => {})
          // ===--- END: axios
        }
      },
      /* =========================================================== //
      // ===---   doPurchase                                  ---=== //
      // =========================================================== */
      doSoumission () {
        let self = this
        // ===--- reset
        this.$set(this, 'isLoadingSoumission', true)
        this.$set(this, 'hasErrorPayment', null)
        // ===---
        let items = []
        this.formPayment.listProducts.forEach((item) => {
          if (item.quantity > 0) {
            items.push({
              product_id: item.summary.id,
              product_name: item.summary.product_name,
              product_code: item.product_code,
              unit_price: item.summary.price,
              quantity: item.quantity
            })
          }
        })
        let datas = {
          customer: {
            phone: this.formCustomer.customer.phone,
          },
          shipping: {
            name: this.formShipping.shipping_address.name,
            address1: this.formShipping.shipping_address.address1,
            address2: this.formShipping.shipping_address.address2,
            country: this.formShipping.shipping_address.country,
            province: this.formShipping.shipping_address.province,
            city: this.formShipping.shipping_address.city,
            zip_code: this.formShipping.shipping_address.zip_code
          },
          items: items
        }
        // ===---
        if (datas.items.length > 0) {
          // ===--- BEGIN: axios
          this.$axios.post(this.$web_url+'/api/fe/create-soumission/', datas, {
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
          })
          .then((apiSuccess) => {
            self.$set(self, 'isLoadingSoumission', false)
            if (apiSuccess.data.valid === 'ok') {
              self.$vuetify.goTo(0)
              self.$set(self, 'hasSuccessSoumission', true)
              self.formPayment.listProducts.forEach((item) => {
                self.$axios.delete(this.$api_url + '/watch/'+item.url.split("/cart/")[1])
                .then(()=>{})
                .catch(()=>{})
              })
            } else {
              self.$set(self, 'hasErrorPayment', 'Une erreur est survenue, veuillez réessayer plus tard.')
            }
          })
          .catch(() => {
            self.$set(self, 'hasErrorPayment', 'Une erreur est survenue, veuillez réessayer plus tard.')
            self.$set(self, 'isLoadingSoumission', false)
          })
          // ===--- END: axios
        } else {
          self.$set(self, 'hasErrorPayment', 'Vous n\'avez aucun produit à soumissionner, vérifiez les quantités.')
          self.$set(self, 'isLoadingSoumission', false)
        }
      },
      /* =========================================================== //
      // ===---   updateQuantity                              ---=== //
      // =========================================================== */
      updateQuantity (action, item) {
        let quantity = this.formPayment.listProducts[item].quantity
        if (action === 'minus') {
          if (quantity > 0) {
            this.$set(this.formPayment.listProducts[item], 'quantity', quantity - 1)
          }
        } else if (action === 'plus') {
          this.$set(this.formPayment.listProducts[item], 'quantity', quantity + 1)
        }
      },
      /* =========================================================== //
      // ===---   previous/next step button                   ---=== //
      // =========================================================== */
      prevStep () {
        this.$vuetify.goTo(100)
        this.$set(this, 'stepCheckout', this.stepCheckout - 1)
      },
      nextStep () {
        this.setUpload(true)
      }
      /* =========================================================== //
      // ===-----------------------------------------------------=== //
      // =========================================================== */
    }
  }
</script>

<style>
  #app .v-stepper--alt-labels .v-stepper__step{
    flex-basis:130px;
  }
  #app .v-stepper--alt-labels .v-stepper__header .v-divider{
    margin-left:-25px;
    margin-right:-25px;
  }
  #app .theme--light.v-stepper .v-stepper__label{
    color:inherit;
  }
  #app .v-stepper,
  #app .v-stepper__header{
    box-shadow: none;
  }
  #app .v-stepper__step__step{
    width:30px;
    min-width:30px;
    height:30px;
  }
  /*===*/
  #app .dm-payment-header,
  #app .dm-payment-footer{
    background-color:rgba(0,0,0,0.03);
    font-size:0.8rem;
    font-weight:700;
    text-transform:uppercase;
    margin:0 0 2rem;
  }
  #app .dm-payment-footer{
    margin:2rem 0 0;
  }
  #app .dm-payment-header .dm-payment-price{
    margin:0;
  }
  #app .dm-payment-header .dm-payment-price div{
    width:100%;
  }
  #app .dm-payment-quantity{
    text-align:center;
    width:80px;
    max-width:80px;
  }
  #app .dm-payment-price{
    text-align:right;
    width:150px;
    width:150px;
    padding:1rem 1.5rem;
  }
  #app .dm-payment .v-list-item__action{
    min-width:120px;
  }
  #app .dm-payment-total .v-list-item__title{
    font-size:1.5rem;
  }
  #app .dm-payment-products .dm-payment-mobiletitle{
    background-color:rgba(0,0,0,0.03);
    font-size:0.8rem;
    font-weight:700;
    text-transform:uppercase;
    display:none;
    padding:1rem;
    margin-bottom:1rem;
  }
  .dm-soumission-quantity{
    padding:1rem 0;
  }
  .dm-soumission-quantity .dm-minus,
  .dm-soumission-quantity .dm-plus{
    background-color:rgba(0,0,0,0.03);
    color:#758987;
    line-height:24px;
    text-align:center;
    display:inline-block;
    width:24px;
    height:24px;
    cursor:pointer;
  }
  .dm-soumission-quantity .dm-minus:hover,
  .dm-soumission-quantity .dm-plus:hover{
    background-color:#48a89e;
    color:#fff;
  }
  .dm-soumission-quantity .dm-quantity{
    background-color:rgba(0,0,0,0.03);
    color:#758987;
    font-weight:800;
    line-height:24px;
    text-align:center;
    display:inline-block;
    width:64px;
    height:24px;
  }
  @media (max-width: 1263px) {
    #app .dm-payment-products .v-list-item:not(.dm-payment-footer),
    #app .dm-payment-products .v-list-item:not(.dm-payment-footer) .v-list-item__content,
    #app .dm-payment-products .v-list-item:not(.dm-payment-footer) .v-list-item__action{
      text-align:left;
      display:block;
      width:100%;
      max-width:none;
      padding:0 0 1rem;
      margin:0;
    }
    #app .dm-payment-products .dm-payment-header{
      display:none!important;
    }
    #app .dm-payment-products .dm-payment-mobiletitle{
      display:block;
    }
    #app .dm-payment-products .dm-payment-mobiletitle + div{
      padding:0 1rem;
    }
    .dm-soumission-quantity{
      padding:1rem;
    }
  }
</style>
