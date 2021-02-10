<template>
  <v-app>
    <router-view/>
  </v-app>
</template>

<script>
  export default {
    name: 'App',
    data: () => ({
      langManual: false
    }),
    mounted () {
      this.setLanguage()
    },
    methods: {
      setLanguage () {
        this.$set(this.$vuetify.lang, 'current', document.documentElement.lang)
        this.$set(this.$i18n, 'locale', document.documentElement.lang)
      },
    }
  }
</script>


<style>
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    padding:0;
    margin:0;
  }
  #app.v-application{
    font-family:inherit;
  }
  #app .v-application--wrap{
    min-height:0;
  }
  #app .v-menu__content.menuable__content__active{
      max-height: 153px!important;
  }
  @media (min-width: 960px) {
    #app .v-input--selection-controls.justify-md-end .v-input__slot{
      justify-content:flex-end;
    }
    #app .v-input--selection-controls.justify-md-end .v-input__slot .v-input--selection-controls__input{
      order: 2;
    }
    #app .v-input--selection-controls.justify-md-end .v-input__slot .v-label{
      text-align: right;
      order: 1;
      margin-right: 13px;
    }
  }
  #app .v-input--selection-controls__input + .v-label{
    margin-bottom:0;
  }
  #app .v-btn--tile{
    box-shadow:none;
    min-width:230px;
    height:auto;
    padding:18px 30px;
  }
  #app .v-btn--tile.dmbtn-nowidth{
      min-width: 0;
      padding:18px;
  }
  @media (max-width: 959px) {
      #app .v-btn--tile:not(.v-btn--icon) {
          min-width: 0;
          height: 50px;
          padding: 11px 13px;
      }
  }
  #app .v-btn--tile.v-size--small{
    min-width:140px;
    padding:8px 20px;
  }
  #app .v-btn--tile.v-size--x-small{
    min-width:100px;
    padding:5px 10px;
  }
  #app .v-btn--tile.v-size--x-small.v-btn--icon{
    min-width: 30px;
    padding:5px;
    margin: -3px 0 0px;
  }
  #app .v-btn__content{
    transition:all 0.3s;
  }
  @media (min-width:1200px) {
    #app .container{
      max-width:1170px;
    }
  }
  @media (min-width:1264) {
    #app .container{
      max-width:1170px;
    }
  }
  @media (min-width:1904) {
    #app .container{
      max-width:1170px;
    }
  }
  .v-input--selection-controls__input input[role=checkbox],
  .v-input--selection-controls__input input[role=radio],
  .v-input--selection-controls__input input[role=switch]{
    opacity:1;
  }
      #app .v-stepper--alt-labels .v-stepper__step {
        flex-basis: 130px;
    }
    @media (max-width: 959px) {
        #app .v-stepper--alt-labels .v-stepper__step {
            flex-basis: 100px;
        }
        #app .v-stepper__content {
            padding: 24px 14px 16px 14px;
        }
    }
    #app .v-stepper .v-stepper__step--active .v-stepper__label{
        text-shadow: none;
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
</style>
