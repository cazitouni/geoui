
<template>
<v-sheet align="center">
<AppBar/>

<v-container>
<v-row justify="center">
<v-card  v-for="element in orderProjets" :key="element['gmd:fileIdentifier']['gco:CharacterString']['#text']" class="  ma-4" max-width="344" >
  <v-col>
  <v-row v-if="element['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:graphicOverview'] !== undefined">
    <v-img :aspect-ratio="16/9"    :src ="element['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:graphicOverview']['gmd:MD_BrowseGraphic']['gmd:fileName']['gco:CharacterString']['#text']"></v-img>
  </v-row>
  <v-row v-else>
    <v-img :aspect-ratio="16/9"    :src ="'https://cdn.vuetifyjs.com/images/parallax/material.jpg'"></v-img>
  </v-row>
  <v-row>
    <v-card-title  class="text-center text-break"  v-snip="{ lines: 4}" style="height:150px;" >{{element["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:citation"]["gmd:CI_Citation"]["gmd:title"]["gco:CharacterString"]["#text"]}}</v-card-title>
    <v-divider ></v-divider>
    <p  class="mt-5" v-snip="{ lines: 5 }"  style="margin-bottom:46px;max-height:150px;word-wrap: break-word;margin-left:10px;margin-right:10px;">{{element["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:abstract"]["gco:CharacterString"]["#text"]}}</p>
    <v-btn @click="$router.push({ path: element['gmd:fileIdentifier']['gco:CharacterString']['#text'] })" tile text color="green darken-3" class="white--text"  block style="position:absolute;bottom:0;">Consulter</v-btn>
  </v-row>
  </v-col>
</v-card>

</v-row>
</v-container>
</v-sheet>

</template>


<script>
import axios from 'axios'
import AppBar from './AppBar'

var convert = require('xml-js');


export default{


  data () {
    return {
      info: null,
      liste: [],
      projets: [],
      pos: 8,

    }
  },

methods:{
  getInitialResults(){
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
    axios
    .get('https://wmsiglw.cus.fr/geonetwork/srv/api/sitemap')
    .then(response => (this.info = convert.xml2js(response.data)))
    .then(() => this.info= this.info.elements[0].elements)
    .then(() => this.info.forEach((element) => {this.liste.push(element.elements[0].elements[0].text.split('/')[7].split('?')[0]);}))
    .then(() => this.liste.forEach((element)  =>  axios.get('https://wmsiglw.cus.fr/geonetwork/srv/api/records/' + element + '/formatters/json'   ).then(response => (this.projets.push(response.data)))))

  },
  getNextResults(){
    window.onscroll = () =>{
      let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
      if(bottomOfWindow && this.pos < this.liste.length){
        this.liste.slice(this.pos, this.pos + 8).forEach((element)  =>  axios.get('https://wmsiglw.cus.fr/geonetwork/srv/api/records/' + element + '/formatters/json'   )
        .then(response => (this.projets.push(response.data))))
        this.pos = this.pos + 8
        console.log(this.pos)
      }
    }
  }
},
  
computed: {
  orderProjets: function () {
     return [...this.projets].sort( (a, b) => a['gmd:fileIdentifier']['gco:CharacterString']['#text'].localeCompare(b['gmd:fileIdentifier']['gco:CharacterString']['#text']))
  },
},
components: {
    AppBar
  },

  beforeMount() {
    this.getInitialResults();
  },

  mounted () {

    this.getNextResults();
  

  },

  

}
</script>
