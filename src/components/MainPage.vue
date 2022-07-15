<template>

<v-container>
<v-switch v-model="$vuetify.theme.dark" hint="This toggles the global state of the Vuetify theme" inset label="Vuetify Theme Dark" persistent-hint></v-switch>
<v-toolbar color="green darken-3"  dense elevation="4" rounded class="my-4 white--text" fixed></v-toolbar>
  <v-row justify="center">
<v-card  v-for="element in projets" :key="element.id" class=" ma-4" max-width="344" >
  <v-col>
  <v-row><v-img  :aspect-ratio="16/9"    :src ="element['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:graphicOverview']['gmd:MD_BrowseGraphic']['gmd:fileName']['gco:CharacterString']['#text']"></v-img></v-row>
  <v-row>
  <v-card-title class="text-center text-break" style="height:150px;" >{{element["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:title"]["gco:CharacterString"]["#text"]}}</v-card-title>
 <v-divider ></v-divider>
  <p class="text-justify" v-snip:js="3" style="max-height:150px;margin-bottom:75px;margin-left:18px;margin-right:18px;margin-top:18px;">{{element["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:abstract"]["gco:CharacterString"]["#text"]}}</p>

  <v-btn color="green darken-3" class="white--text"  block style="position:absolute;bottom:0;margin-top:75px;">Consulter</v-btn>

  </v-row>
  </v-col>

</v-card>
  </v-row>
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
