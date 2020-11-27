<template>
  <v-app>
    <router-view/>
  </v-app>
</template>

<script>
  export default {
    name: 'App'
  }
</script>


<style>
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color:#758987;
    padding:0;
    margin:0;
  }
  #app.v-application{
    font-family:inherit;
  }
  #app.theme--light.v-application,
  #app.theme--light .v-list{
    background:transparent;
    color:#48a89e;
  }
  #app.theme--light .v-menu__content{
    background:#fff;
  }
  #app .v-application--wrap{
    min-height:0;
  }
  @media (min-width: 960px) {
    #app .v-input--selection-controls.justify-md-end .v-input__slot{
      justify-content:flex-end;
    }
    #app .v-input--selection-controls.justify-md-end .v-input__slot .v-label{
      flex:none;
    }
  }
  #app .v-input--selection-controls__input + .v-label{
    margin-bottom:0;
  }
  #app.theme--light .v-list-item:not(.v-list-item--active):not(.v-list-item--disabled),
  #app.theme--light .v-select .v-select__selection--comma,
  #app.theme--light .v-input,
  #app.theme--light .v-input input,
  #app.theme--light .v-input textarea,
  #app.theme--light .v-card,
  #app .v-card__subtitle,
  #app .v-card__text,
  #app.theme--light.v-card > .v-card__text,
  #app.theme--light.v-card .v-card__subtitle{
    color:#48a89e!important;
  }
  #app .v-btn--tile{
    box-shadow:none;
    min-width:230px;
    height:auto;
    padding:18px 30px;
  }
  #app .v-btn__content{
    font-weight:900;
    transition:color 0.3s;
  }
  #app .v-btn__content:hover{
    color:#f0592b;
  }
  #app .v-btn.success{
    background-color:#f0592b!important;
    border-color:#f0592b!important;
  }
  #app .v-btn.success .v-btn__content:hover{
    color:#48a89e;
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
</style>
