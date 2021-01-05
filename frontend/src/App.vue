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
    #app .v-input--selection-controls.justify-md-end .v-input__slot .v-label{
      flex:none;
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
</style>
