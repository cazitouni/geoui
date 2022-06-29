<template>
  <v-container>
    <v-card
  elevation="12"
  outlined
  tile
>
    <h1>Bitcoin Price Index</h1>
    <div v-for="currency in info" class="currency" :key="currency.id">
    {{ currency.description }}:
    <span class="lighten">
    <span v-html="currency.symbol"></span>{{ currency.rate_float | currencydecimal }}
    </span>
    </div>
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
