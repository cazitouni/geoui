<template>
<v-toolbar color="green darken-3"  dense elevation="12"  class="fixed-bar">
  <v-text-field @keyup.enter="onEnter()" v-model="searchText" label="Rechercher dans le catalogue" dark hide-details color="light-blue accent-3" prepend-icon="mdi-magnify" single-line></v-text-field>
</v-toolbar>
</template>

<style scoped>
.fixed-bar {
  width : 100%;
  position: sticky;
  position: -webkit-sticky;
  top: 0em;
  z-index: 3;
}
</style>
<script>

import MainPage from "./MainPage";


export default{

  data () {
    return {

	  searchText : '',
    }
  },

methods:{

},
  
computed: {

},

components: {
    MainPage
  },

  mounted () {

  },

}
</script>
