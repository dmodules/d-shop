<template>
  <div class="checkout" id="app-checkout">
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
            <h2>Commander</h2>
          </div>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-stepper v-model="stepCheckout" alt-labels>
              <v-stepper-header>
                <v-stepper-step :complete="stepCheckout > 1" :step="1">
                  {{ $i18n.t("Client") }}
                </v-stepper-step>
                <v-divider />
                <v-stepper-step :complete="stepCheckout > 2" :step="2">
                  {{ $i18n.t("Livraison") }}
                </v-stepper-step>
                <v-divider />
                <v-stepper-step :complete="stepCheckout > 3" :step="3">
                  {{ $i18n.t("Facturation") }}
                </v-stepper-step>
                <v-divider />
                <v-stepper-step :complete="stepCheckout > 4" :step="4">
                  {{ $i18n.t("Paiement") }}
                </v-stepper-step>
              </v-stepper-header>
              <v-stepper-items>
                <v-stepper-content :step="1">
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
                        <v-col cols="12" class="text-right">
                          <v-btn
                            tile
                            color="primary"
                            :disabled="!formCustomer.valid"
                            @click="nextStep()"
                            >{{ $i18n.t("Suivant") }}</v-btn
                          >
                        </v-col>
                      </v-row>
                    </v-card-actions>
                  </v-card>
                </v-stepper-content>
                <v-stepper-content :step="2">
                  <v-card>
                    <v-card-title>
                      <h4>{{ $i18n.t("Methodesdexpedition") }}</h4>
                    </v-card-title>
                    <v-card-text>
                      <v-form v-model="formShippingMethod.valid">
                        <v-row>
                          <v-col
                            v-if="formChoix.shippingMethods.length > 0"
                            cols="12"
                          >
                            <v-radio-group
                              v-model="
                                formShippingMethod.shipping_method
                                  .shipping_modifier
                              "
                              :rules="[
                                (v) => !!v || $i18n.t('Cechampsesrrequis'),
                              ]"
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
                              {{ $i18n.t("Nomethodesdexpedition") }}
                            </v-alert>
                          </v-col>
                        </v-row>
                      </v-form>
                    </v-card-text>
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
                        <v-col cols="12" sm="6" class="text-left">
                          <v-btn tile color="primary" @click="prevStep()">{{
                            $i18n.t("Precedent")
                          }}</v-btn>
                        </v-col>
                        <v-col cols="12" sm="6" class="text-right">
                          <v-btn
                            tile
                            color="primary"
                            :disabled="
                              !formShippingMethod.shipping_method
                                .shipping_modifier || !formShipping.valid
                            "
                            @click="nextStep()"
                            >{{ $i18n.t("Suivant") }}</v-btn
                          >
                        </v-col>
                      </v-row>
                    </v-card-actions>
                  </v-card>
                </v-stepper-content>
                <v-stepper-content :step="3">
                  <v-card>
                    <v-card-title>
                      <h4>{{ $i18n.t("Methodesdepaiement") }}</h4>
                    </v-card-title>
                    <v-card-text>
                      <v-form v-model="formBillingMethod.valid">
                        <v-row>
                          <v-col cols="12">
                            <v-radio-group
                              v-model="
                                formBillingMethod.payment_method
                                  .payment_modifier
                              "
                              :rules="[
                                (v) => !!v || $i18n.t('Cechampsesrrequis'),
                              ]"
                              required
                            >
                              <v-radio
                                v-for="(item, n) in formChoix.billingMethods"
                                :key="n"
                                :label="item[1]"
                                :value="item[0]"
                              />
                            </v-radio-group>
                          </v-col>
                        </v-row>
                      </v-form>
                    </v-card-text>
                    <v-card-title>
                      <h4>{{ $i18n.t("Adressedefacturation") }}</h4>
                    </v-card-title>
                    <v-card-text>
                      <v-form v-model="formBilling.valid">
                        <v-row>
                          <v-col cols="12">
                            <v-checkbox
                              v-model="
                                formBilling.billing_address.use_primary_address
                              "
                              :label="$i18n.t('Utiliserladressedelivraison')"
                            />
                          </v-col>
                        </v-row>
                        <v-row
                          v-if="
                            !formBilling.billing_address.use_primary_address
                          "
                        >
                          <v-col cols="12">
                            <v-text-field
                              v-model="formBilling.billing_address.name"
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
                              v-model="formBilling.billing_address.address1"
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
                              v-model="formBilling.billing_address.address2"
                              :label="$i18n.t('Adressesuite')"
                              placeholder=" "
                              filled
                            />
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-autocomplete
                              v-model="formBilling.billing_address.country"
                              :label="$i18n.t('Pays')"
                              placeholder=" "
                              :rules="[
                                (v) => !!v || $i18n.t('Cechampsesrrequis'),
                              ]"
                              :items="formChoix.countries"
                              :item-text="'name'"
                              :item-value="'alpha2'"
                              :error-messages="
                                formError.shipping_address.country
                              "
                              required
                              filled
                              attach
                              @keydown="
                                formError.shipping_address.country = null
                              "
                            />
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-text-field
                              v-model="formBilling.billing_address.province"
                              :label="$i18n.t('Province')"
                              placeholder=" "
                              :rules="[
                                (v) => !!v || $i18n.t('Cechampsesrrequis'),
                              ]"
                              :error-messages="
                                formError.shipping_address.province
                              "
                              required
                              filled
                              @keydown="
                                formError.shipping_address.province = null
                              "
                            />
                          </v-col>
                          <v-col cols="12" md="6">
                            <v-text-field
                              v-model="formBilling.billing_address.city"
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
                              v-model="formBilling.billing_address.zip_code"
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
                        <v-col cols="12" sm="6" class="text-left">
                          <v-btn tile color="primary" @click="prevStep()">{{
                            $i18n.t("Precedent")
                          }}</v-btn>
                        </v-col>
                        <v-col cols="12" sm="6" class="text-right">
                          <v-btn
                            tile
                            color="primary"
                            :disabled="!formBilling.valid"
                            @click="nextStep()"
                            >{{ $i18n.t("Suivant") }}</v-btn
                          >
                        </v-col>
                      </v-row>
                    </v-card-actions>
                  </v-card>
                </v-stepper-content>
                <v-stepper-content :step="4">
                  <v-card>
                    <v-card-title>
                      <h4>{{ $i18n.t("Paiement") }}</h4>
                    </v-card-title>
                    <v-card-text>
                      <v-row>
                        <v-col cols="12" md="6" class="text-left">
                          <h5>{{ $i18n.t("Adressedelivraison") }}</h5>
                          <v-alert text color="primary">
                            <div
                              v-html="
                                tagShippingAddress.replace(/\n/g, '<br />')
                              "
                            ></div>
                          </v-alert>
                        </v-col>
                        <v-col cols="12" md="6" class="text-left">
                          <h5>{{ $i18n.t("Adressedefacturation") }}</h5>
                          <v-alert text color="primary">
                            <div
                              v-html="
                                tagBillingAddress.replace(/\n/g, '<br />')
                              "
                            ></div>
                          </v-alert>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" md="6" class="text-left">
                          <h5>{{ $i18n.t("Methodedelivraison") }}</h5>
                          <v-alert text color="primary">
                            <div
                              v-html="
                                tagShippingMethod.replace(/\n/g, '<br />')
                              "
                            ></div>
                          </v-alert>
                        </v-col>
                        <v-col cols="12" md="6" class="text-left">
                          <h5>{{ $i18n.t("Methodedepaiement") }}</h5>
                          <v-alert text color="primary">
                            <div
                              v-html="tagBillingMethod.replace(/\n/g, '<br />')"
                            ></div>
                          </v-alert>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" md="6" lg="8" class="text-left">
                          <h5>{{ $i18n.t("Resumedevotrecommande") }}</h5>
                          <v-list class="dm-payment-products">
                            <v-list-item class="dm-payment-header">
                              <v-list-item-content class="dm-payment-quantity">
                                <div>{{ $i18n.t("Quantite") }}</div>
                              </v-list-item-content>
                              <v-list-item-content class="text-center">
                                <div>{{ $i18n.t("Produit") }}</div>
                              </v-list-item-content>
                              <v-list-item-action class="dm-payment-price">
                                <div>{{ $i18n.t("Prix") }}</div>
                              </v-list-item-action>
                              <v-list-item-action class="dm-payment-price">
                                <div>{{ $i18n.t("Total") }}</div>
                              </v-list-item-action>
                            </v-list-item>
                            <template
                              v-for="(item, n) in formPayment.listProducts"
                            >
                              <v-divider v-if="n > 0" :key="'divider-' + n" />
                              <v-list-item :key="'product-' + n">
                                <v-list-item-content
                                  class="dm-payment-quantity"
                                >
                                  <div class="dm-payment-mobiletitle">
                                    {{ $i18n.t("Quantite") }}
                                  </div>
                                  <div>{{ item.quantity }} x</div>
                                </v-list-item-content>
                                <v-list-item-content class="dm-payment-produit">
                                  <div class="dm-payment-mobiletitle">
                                    {{ $i18n.t("Produit") }}
                                  </div>
                                  <div v-html="item.summary.media"></div>
                                </v-list-item-content>
                                <v-list-item-action class="dm-payment-price">
                                  <div class="dm-payment-mobiletitle">
                                    {{ $i18n.t("Prix") }}
                                  </div>
                                  <div v-html="item.unit_price"></div>
                                </v-list-item-action>
                                <v-list-item-action class="dm-payment-price">
                                  <div class="dm-payment-mobiletitle">
                                    {{ $i18n.t("Total") }}
                                  </div>
                                  <div v-html="item.line_total"></div>
                                </v-list-item-action>
                              </v-list-item>
                            </template>
                            <template v-if="listPromoCodes.length > 0">
                                <v-divider />
                                <v-subheader v-text="$i18n.t('AppliedPromoCodes')"></v-subheader>
                                <v-list-item v-for="(item, n) in listPromoCodes" :key="'promo'+n">
                                    <v-list-item-content>
                                        <v-list-item-title>
                                            {{item}}
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </template>
                            <v-list-item class="dm-payment-footer">
                              <v-list-item-content class="text-left">
                                <div>
                                  <span
                                    v-text="formPayment.productsQuantity"
                                  ></span>
                                  <span v-if="formPayment.productsQuantity > 1">
                                    {{ $i18n.t("produits") }}</span
                                  >
                                  <span v-else> {{ $i18n.t("produit") }}</span>
                                </div>
                              </v-list-item-content>
                              <v-list-item-action class="text-right">
                                <div>
                                  <span>{{ $i18n.t("Soustotal") }} </span>
                                  <span v-text="formPayment.subtotal"></span>
                                </div>
                              </v-list-item-action>
                            </v-list-item>
                          </v-list>
                        </v-col>
                        <v-col
                          cols="12"
                          md="6"
                          lg="4"
                          class="text-left text-md-right"
                        >
                          <h5>{{ $i18n.t("Resumedevotrefacture") }}</h5>
                          <v-form v-model="formAcceptCondition.valid">
                            <v-list class="dm-payment">
                              <v-list-item class="dm-payment-subtotal">
                                <v-list-item-content>
                                  <v-list-item-title>
                                    {{ $i18n.t("Soustotal") }}
                                  </v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-action>
                                  <v-list-item-title class="font-weight-bold">
                                    <span v-text="formPayment.subtotal"></span>
                                  </v-list-item-title>
                                </v-list-item-action>
                              </v-list-item>
                              <v-list-item
                                v-for="(item, n) in formPayment.listExtras"
                                :key="'extra-' + n"
                              >
                                <v-list-item-content>
                                  <v-list-item-title>
                                    {{ item.label }}
                                  </v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-action>
                                  <v-list-item-title class="font-weight-bold">
                                    <span v-text="item.amount"></span>
                                  </v-list-item-title>
                                </v-list-item-action>
                              </v-list-item>
                              <v-divider />
                              <v-list-item class="dm-payment-total">
                                <v-list-item-content>
                                  <v-list-item-title>
                                    {{ $i18n.t("Total") }}
                                  </v-list-item-title>
                                </v-list-item-content>
                                <v-list-item-action>
                                  <v-list-item-title class="font-weight-bold">
                                    <span v-text="formPayment.total"></span>
                                  </v-list-item-title>
                                </v-list-item-action>
                              </v-list-item>
                            </v-list>
                            <v-checkbox
                              v-model="
                                formAcceptCondition.accept_condition.plugin_1
                                  .accept
                              "
                              :label="$i18n.t('Jailuetjaccepte')"
                              hide-details
                              required
                              class="align-center justify-md-end mb-5"
                            />
                            <v-btn
                              tile
                              color="success"
                              :loading="isLoadingPayment"
                              :disabled="
                                !formAcceptCondition.accept_condition.plugin_1
                                  .accept
                              "
                              @click="setUpload()"
                              >{{ $i18n.t("Payeretcommander") }}</v-btn
                            >
                          </v-form>
                        </v-col>
                      </v-row>
                    </v-card-text>
                    <v-card-actions>
                      <v-row>
                        <v-col cols="12" class="text-left">
                          <v-btn tile color="primary" @click="prevStep()">{{
                            $i18n.t("Precedent")
                          }}</v-btn>
                        </v-col>
                      </v-row>
                    </v-card-actions>
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
  name: "Checkout",
  components: {
    dmAuth: () => import("@/components/Auth.vue"),
  },
  data: () => ({
    isAuth: false,
    isLoading: false,
    isLoadingPayment: false,
    hasEmptyCart: false,
    stepCheckout: 1,
    formChoix: {
      salutation: [],
      shippingAddress: [],
      countries: [],
      provincesCA: [],
      shippingMethods: [],
      billingMethods: [],
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
    formShippingMethod: {
      valid: false,
      shipping_method: {
        plugin_order: 1,
        shipping_modifier: null,
      },
    },
    formBilling: {
      valid: false,
      billing_address: {
        plugin_order: 1,
        active_priority: 1,
        use_primary_address: false,
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
    formBillingMethod: {
      valid: false,
      payment_method: {
        plugin_order: 1,
        payment_modifier: "",
      },
    },
    formAcceptCondition: {
      valid: false,
      accept_condition: {
        plugin_1: {
          accept: false,
          plugin_id: 1,
          plugin_order: 1,
        },
      },
    },
    formPayment: {
      productsCount: 0,
      productsQuantity: 0,
      subtotal: "C$ 0.00",
      total: "C$ 0.00",
      listExtras: [],
      listProducts: [],
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
      },
      billing_address: {
        name: null,
        address1: null,
        address2: null,
        city: null,
        province: null,
        country: null,
        zip_code: null,
      },
    },
    asCurrentAddress: false,
    tagCustomer: "",
    tagShippingAddress: "",
    tagBillingAddress: "",
    tagShippingMethod: "",
    tagBillingMethod: "",
    tagNote: "",
    listPromoCodes: []
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
    this.getShippingMethods();
    this.getBillingMethods();
    this.getPromoCodes();
  },
  methods: {
    setAuth() {
        this.$set(this, "isAuth", true);
        this.getCustomer();
        this.getShippingMethods();
        this.getBillingMethods();
        this.getPromoCodes();
    },
    /* =========================================================== //
    // ===---   getCustomer                                 ---=== //
    // =========================================================== */
    getCustomer() {
      let self = this;
      // ===--- BEGIN: axios
      this.$axios
        .get(this.$web_url + "/api/fe/customer/", {
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
            self.$set(
              self.formShipping,
              "shipping_address",
              apiSuccess.data.address_shipping
            );
          }
          // set billing address form
          if (apiSuccess.data.address_billing) {
            self.$set(
              self.formBilling,
              "billing_address",
              apiSuccess.data.address_billing
            );
          }
          self.getDigest();
        })
        .catch(() => {});
      // ===--- END: axios
    },
    /* =========================================================== //
    // ===---   getShippingMethods                          ---=== //
    // =========================================================== */
    getShippingMethods() {
      let self = this
      this.$set(this.formChoix, 'shippingMethods', [])
      // ===--- BEGIN: axios
      this.$axios
        .get(this.$web_url + "/api/fe/shipping-methods/", {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        })
        .then((apiSuccess) => {
          if (apiSuccess.data.shipping_methods.length > 0) {
            apiSuccess.data.shipping_methods.forEach((item) => {
              if (item[0] !== null && item[1] !== null) {
                self.formChoix.shippingMethods.push(item);
              }
            });
            if (self.formChoix.shippingMethods.length > 0) {
              self.$set(
                self.formShippingMethod.shipping_method,
                "shipping_modifier",
                self.formChoix.shippingMethods[0][0]
              );
            }
          }
        })
        .catch(() => {});
      // ===--- END: axios
    },
    /* =========================================================== //
    // ===---   getBillingMethods                           ---=== //
    // =========================================================== */
    getBillingMethods() {
      let self = this;
      this.$set(this.formChoix, 'billingMethods', [])
      // ===--- BEGIN: axios
      this.$axios
        .get(this.$web_url + "/api/fe/billing-methods/", {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        })
        .then((apiSuccess) => {
          if (apiSuccess.data.billing_methods.length > 0) {
            self.$set(
              self.formChoix,
              "billingMethods",
              apiSuccess.data.billing_methods
            );
            self.$set(
              self.formBillingMethod.payment_method,
              "payment_modifier",
              apiSuccess.data.billing_methods[0][0]
            );
          }
        })
        .catch(() => {});
      // ===--- END: axios
    },
    getPromoCodes(products = null) {
        let self = this;
        this.$set(this, "isLoading", false)
        this.$set(this, "listPromoCodes", [])
        // ===---
        let p = []
        if (products) {
            products.forEach((item) => {
                p.push({
                    product_code: item.product_code,
                    summary: {
                        product_model: item.summary.product_model
                    }
                })
            })
        } else {
            p = this.listProducts
        }
        let datas = {
            products: p
        }
        // ===---
        this.$axios.post(this.$web_url + "/discount/promocodes/?p="+JSON.stringify(datas), datas, {
            headers: { "Content-Type": "application/json", Accept: "application/json"}
        })
        .then((apiSuccess) => {
            apiSuccess.data.promolist.forEach((item) => {
                self.listPromoCodes.push(item.name)
            })
        })
    },
    /* =========================================================== //
    // ===---   setUpload                                   ---=== //
    // =========================================================== */
    setUpload(next = false) {
      let self = this;
      let datas = null;
      if (this.stepCheckout === 1) {
        datas = this.formCustomer;
      } else if (this.stepCheckout === 2) {
        datas = {
          shipping_address: this.formShipping.shipping_address,
          shipping_method: this.formShippingMethod.shipping_method,
        };
      } else if (this.stepCheckout === 3) {
        datas = {
          billing_address: this.formBilling.billing_address,
          payment_method: this.formBillingMethod.payment_method,
        };
      } else if (this.stepCheckout === 4) {
        datas = this.formAcceptCondition;
        this.$set(this, "isLoadingPayment", true);
      }
      // ===--- BEGIN: axios
      this.$axios
        .put(this.$api_url + "/checkout/upload/", datas, {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        })
        .then(() => {
          self.getDigest();
          if (next) {
            // if button 'next' was clicked, go to next step
            self.$vuetify.goTo(100);
            self.$set(self, "stepCheckout", self.stepCheckout + 1);
          } else if (self.stepCheckout === 4) {
            // if all is okay, purchase
            self.doPurchase();
          }
        })
        .catch((apiFail) => {
          self.$set(self, "isLoadingPayment", false);
          if (apiFail.response && apiFail.response.data) {
            if (apiFail.response.data.customer_form) {
              self.$set(
                self.formError.customer,
                "salutation",
                apiFail.response.data.customer_form.salutation
                  ? apiFail.response.data.customer_form.salutation
                  : null
              );
              self.$set(
                self.formError.customer,
                "first_name",
                apiFail.response.data.customer_form.first_name
                  ? apiFail.response.data.customer_form.first_name
                  : null
              );
              self.$set(
                self.formError.customer,
                "last_name",
                apiFail.response.data.customer_form.last_name
                  ? apiFail.response.data.customer_form.last_name
                  : null
              );
              self.$set(
                self.formError.customer,
                "email",
                apiFail.response.data.customer_form.email
                  ? apiFail.response.data.customer_form.email
                  : null
              );
            }
          }
        });
      // ===--- END: axios
    },
    /* =========================================================== //
    // ===---   getDigest                                   ---=== //
    // =========================================================== */
    getDigest() {
      let self = this;
      // ===--- BEGIN: axios
      this.$axios
        .get(this.$api_url + "/checkout/digest/", {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        })
        .then((apiSuccess) => {
          if (apiSuccess.data && apiSuccess.data.cart_summary) {
            if (apiSuccess.data.cart_summary.total_quantity > 0) {
              self.$set(
                self.formPayment,
                "productsCount",
                apiSuccess.data.cart_summary.num_items
              );
              self.$set(
                self.formPayment,
                "productsQuantity",
                apiSuccess.data.cart_summary.total_quantity
              );
              self.$set(
                self.formPayment,
                "subtotal",
                apiSuccess.data.cart_summary.subtotal
              );
              self.$set(
                self.formPayment,
                "total",
                apiSuccess.data.cart_summary.total
              );
              self.$set(
                self.formPayment,
                "listExtras",
                apiSuccess.data.cart_summary.extra_rows
              );
              self.$set(
                self.formPayment,
                "listProducts",
                apiSuccess.data.cart_summary.items
              );
              self.getPromoCodes(apiSuccess.data.cart_summary.items)
            } else {
              self.$set(self, "hasEmptyCart", true);
            }
          }
          if (apiSuccess.data && apiSuccess.data.checkout_digest) {
            self.$set(
              self,
              "tagCustomer",
              apiSuccess.data.checkout_digest.customer_tag
            );
            self.$set(
              self,
              "tagShippingAddress",
              apiSuccess.data.checkout_digest.shipping_address_tag
            );
            self.$set(
              self,
              "tagBillingAddress",
              apiSuccess.data.checkout_digest.billing_address_tag
            );
            self.$set(
              self,
              "tagShippingMethod",
              apiSuccess.data.checkout_digest.shipping_method_tag
            );
            self.$set(
              self,
              "tagBillingMethod",
              apiSuccess.data.checkout_digest.payment_method_tag
            );
            self.$set(
              self,
              "tagNote",
              apiSuccess.data.checkout_digest.extra_annotation_tag
            );
          }
        })
        .catch(() => {});
      // ===--- END: axios
    },
    /* =========================================================== //
    // ===---   doPurchase                                  ---=== //
    // =========================================================== */
    doPurchase() {
      let self = this;
      this.$set(this, "isLoading", true);
      this.$vuetify.goTo(0);
      // ===---
      let datas = {
        products: this.listPromoCodes
      }
      // ===--- BEGIN: axios
      this.$axios.post(this.$api_url + "/checkout/purchase/", {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        })
        .then((apiSuccess) => {
          self.$set(self, "isLoadingPayment", false)
          self.$axios.post(self.$web_url + "/discount/promocodesoff/?p="+JSON.stringify(datas), datas, { headers: { "Content-Type": "application/json", Accept: "application/json"}})
          eval(apiSuccess.data.expression)
        })
        .catch(() => {
          self.$set(self, "isLoadingPayment", false);
          self.$(self, "isLoading", false);
        });
      // ===--- END: axios
    },
    /* =========================================================== //
    // ===---   previous/next step button                   ---=== //
    // =========================================================== */
    prevStep() {
      this.$vuetify.goTo(100);
      this.$set(this, "stepCheckout", this.stepCheckout - 1);
    },
    nextStep() {
      this.setUpload(true);
    },
    /* =========================================================== //
    // ===-----------------------------------------------------=== //
    // =========================================================== */
  },
};
</script>

<style>
    #app .v-stepper--alt-labels .v-stepper__step {
    flex-basis: 130px;
    }
    #app .v-stepper--alt-labels .v-stepper__header .v-divider {
    margin-left: -25px;
    margin-right: -25px;
    }
    #app .theme--light.v-stepper .v-stepper__label {
    color: inherit;
    }
    #app .v-stepper,
    #app .v-stepper__header {
    box-shadow: none;
    }
    #app .v-stepper__step__step {
    width: 30px;
    min-width: 30px;
    height: 30px;
    }
    /*===*/
    #app .dm-payment-header,
    #app .dm-payment-footer {
    background-color: rgba(0, 0, 0, 0.03);
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    margin: 0 0 2rem;
    }
    #app .dm-payment-footer {
    margin: 2rem 0 0;
    }
    #app .dm-payment-header .dm-payment-price {
    margin: 0;
    }
    #app .dm-payment-header .dm-payment-price div {
    width: 100%;
    }
    #app .dm-payment-quantity {
    text-align: center;
    width: 80px;
    max-width: 80px;
    }
    #app .dm-payment-price {
    text-align: right;
    width: 150px;
    width: 150px;
    padding: 1rem 1.5rem;
    }
    #app .dm-payment .v-list-item__action {
    min-width: 120px;
    }
    #app .dm-payment-total .v-list-item__title {
    font-size: 1.5rem;
    }
    #app .dm-payment-products .dm-payment-mobiletitle {
        background-color: rgba(0, 0, 0, 0.03);
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        display: none;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    #app .dm-payment-products .media-body h5 {
        text-overflow: ellipsis;
        overflow:hidden;
        display:inline-block;
    }
    #app .dm-payment-products .media-body h5 + *{
        display:none;
    }
    @media (max-width: 1263px) {
        #app .dm-payment-products .v-list-item:not(.dm-payment-footer),
        #app
            .dm-payment-products
            .v-list-item:not(.dm-payment-footer)
            .v-list-item__content,
        #app
            .dm-payment-products
            .v-list-item:not(.dm-payment-footer)
            .v-list-item__action {
            text-align: left;
            display: block;
            width: 100%;
            max-width: none;
            padding: 0 0 1rem;
            margin: 0;
        }
        #app .dm-payment-products .dm-payment-header {
            display: none !important;
        }
        #app .dm-payment-products .dm-payment-mobiletitle {
            display: block;
        }
        #app .dm-payment-products .dm-payment-mobiletitle + div {
            padding: 0 1rem;
        }
    }
</style>
