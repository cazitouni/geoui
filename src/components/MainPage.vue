<template>

<v-container >
<v-switch v-model="$vuetify.theme.dark" hint="This toggles the global state of the Vuetify theme" inset label="Vuetify Theme Dark" persistent-hint></v-switch>

  <v-toolbar color="green" dense elevation="4" rounded class="my-4"></v-toolbar>

  <v-card  class="mx-auto" >
    <v-card-title>Bitcoin Price Index</v-card-title>
    <v-card-text>
    <div v-for="currency in info" class="currency" :key="currency.id">
    {{ currency.description }}:
    <span v-html="currency.symbol"></span>{{ currency.rate_float | currencydecimal }}
    </div>
    </v-card-text>
  </v-card>

</v-container>

</template>

<script>
import axios from 'axios'
export default{
  
  data () {
    return {
      info: null
    }
  },
  filters: {
  currencydecimal (value) {
    return value.toFixed(2)
  }
},
  mounted () {
axios
  .get('https://api.coindesk.com/v1/bpi/currentprice.json')
  .then(response => (this.info = response.data.bpi))
  }
}
</script>
