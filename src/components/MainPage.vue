<template>

<v-container >
<v-switch v-model="$vuetify.theme.dark" hint="This toggles the global state of the Vuetify theme" inset label="Vuetify Theme Dark" persistent-hint></v-switch>

  <v-toolbar color="green" dense elevation="4" rounded class="my-4"></v-toolbar>

  <v-card  v-for="element in projets" :key="element.id" class="ma-4" >
{{element}}
  </v-card>

</v-container>

</template>

<script>
import axios from 'axios'
var convert = require('xml-js');
export default{
  
  data () {
    return {
      info: null,
      liste: [],
      projets: []
    }
  },

  mounted () {
  const requestOne = axios
  .get('https://wisiglw.cus.fr/geonetwork/srv/api/sitemap')
  .then(response => (this.info = convert.xml2js(response.data)))
  .then(() => this.info= this.info.elements[0].elements)
  .then(() => this.info.forEach((element) => {this.liste.push(element.elements[0].elements[0].text);}))
  .then(() => 
  this.liste.forEach((element, i) => 
  axios.get(this.liste[i])
  .then(response => (this.projets.push(response.data)))
  .then()
  ))
  }
}
</script>
