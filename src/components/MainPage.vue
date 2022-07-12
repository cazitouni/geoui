<template>

<v-container>
<v-switch v-model="$vuetify.theme.dark" hint="This toggles the global state of the Vuetify theme" inset label="Vuetify Theme Dark" persistent-hint></v-switch>
<v-toolbar color="green" dense elevation="4" rounded class="my-4"></v-toolbar>
<v-card  v-for="element in projets" :key="element.id" class=" ma-4">
  <v-row align="center">
  <v-col class=" col-3"><v-img  :aspect-ratio="4/3"  max-width = "344"  :src ="element['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:graphicOverview']['gmd:MD_BrowseGraphic']['gmd:fileName']['gco:CharacterString']['#text']"></v-img></v-col>
  <v-col>
  <v-card-title>{{element["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:title"]["gco:CharacterString"]["#text"]}}</v-card-title>
  <v-card-text>{{element["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:abstract"]["gco:CharacterString"]["#text"]}}</v-card-text>
  <v-card-actions>{{element["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:pointOfContact"][0]["gmd:CI_ResponsibleParty"]["gmd:organisationName"]["gco:CharacterString"]["#text"]}}</v-card-actions>
  </v-col>
  </v-row>

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
  .then(() => this.info.forEach((element) => {this.liste.push(element.elements[0].elements[0].text.split('/')[7].split('?')[0]);}))
  .then(() => 
  this.liste.forEach((element, i) => 
  axios.get('https://wisiglw.cus.fr/geonetwork/srv/api/records/' + element + '/formatters/json')
  .then(response => (this.projets.push(response.data)))
  .then()
  ))
  }
}
</script>
