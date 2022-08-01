<template> 
<div v-if="info !== null"  align="center">
<v-row><v-btn tile text color="green darken-3" class="white--text ma-6"  @click="$router.push('/')"> <v-icon dark>mdi-arrow-left</v-icon> Retour</v-btn></v-row>
<h1  class=" mt-6 mx-2 text-center ">{{info['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:citation']['gmd:CI_Citation']['gmd:title']['gco:CharacterString']['#text']}}</h1>
<h2 align="left" class=" mt-12 ms-12">Résumé :</h2>
<h4 class="word-break text-justify ma-12">{{info["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:abstract"]["gco:CharacterString"]["#text"]}}</h4>
<h2 align="left" class=" mt-12 ms-12">Mise à jour:</h2>
<h4 class="word-break text-justify ma-12">{{info["gmd:dataQualityInfo"]["gmd:DQ_DataQuality"]["gmd:lineage"]["gmd:LI_Lineage"]["gmd:statement"]["gco:CharacterString"]["#text"]}}</h4>
<h2 align="left" class=" mt-12 ms-12">Contact:</h2>
<h4 class="word-break text-justify mt-4 ms-12">{{info["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:pointOfContact"][0]["gmd:CI_ResponsibleParty"]["gmd:individualName"]["gco:CharacterString"]["#text"]}}</h4>
<h4 class="word-break text-justify ms-12">{{info["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:pointOfContact"][0]["gmd:CI_ResponsibleParty"]["gmd:organisationName"]["gco:CharacterString"]["#text"]}}</h4>
<h4 class="word-break text-justify ms-12">{{info["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:pointOfContact"][0]["gmd:CI_ResponsibleParty"]["gmd:positionName"]["gco:CharacterString"]["#text"]}}</h4>
<h4 class="word-break text-justify ms-12">{{info["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:pointOfContact"][0]["gmd:CI_ResponsibleParty"]["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:address"]["gmd:CI_Address"]["gmd:electronicMailAddress"]["gco:CharacterString"]["#text"]}}
  - {{info["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:pointOfContact"][0]["gmd:CI_ResponsibleParty"]["gmd:contactInfo"]["gmd:CI_Contact"]["gmd:phone"]["gmd:CI_Telephone"]["gmd:voice"]["gco:CharacterString"]["#text"]}}
</h4>

<div class="ma-12" v-if="correct">
<l-map id="leaflet" class="mt-12 mx-2"  style="height: 500px; width=80%" :zoom="zoom" :center="center">
<l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
<l-wms-tile-layer :key="wmsLayer.name" :base-url="wmsLayer.url" :layers="wmsLayer.layers" :visible="wmsLayer.visible" :name="wmsLayer.name" :attribution="wmsLayer.attribution" :transparent="true" format="image/png" layer-type="base"></l-wms-tile-layer>
</l-map>
</div>
</div>
</template>

<style scoped>
#leaflet {
    background: white;
}
</style>

<script>
import axios from 'axios'
var convert = require('xml-js');

  export default {
    
  data () {
    return {
      correct: false,
      info: null,
      info_data : null,
      id : this.$route.path.split('/')[1],
      zoom: 13, 
      url: 'https://wgs-users.s3.amazonaws.com/cus/fonds/ems_gris/{z}/{x}/{y}.png',
      attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [48.5734053, 7.7521113],
      wmsLayer: {
        url: null,
        name: 'Couche',
        visible: true,
        layers: null,
        format: 'image/png',
      }
    }
  },

 beforeMount() {
   axios
    .get('https://wisiglw.cus.fr/geonetwork/srv/api/records/' + this.id + '/formatters/json'  )
    .then(response => (this.info = response.data))
    .then(() => 
      axios.get('https://viewer.wisiglw.cus.fr/qgis/WEB_totem?service=WMS&request=GetCapabilities&FORMAT=application/json')
      .then(response => this.info_data = convert.xml2js(response.data))
    )
    .then(() => this.wmsLayer.url ='https://viewer.wisiglw.cus.fr/qgis/' + this.info["gmd:distributionInfo"]["gmd:MD_Distribution"]["gmd:transferOptions"]["gmd:MD_DigitalTransferOptions"]["gmd:onLine"][1]["gmd:CI_OnlineResource"]["gmd:name"]["gco:CharacterString"]["#text"])
    .then(() => this.wmsLayer.layers = this.info["gmd:distributionInfo"]["gmd:MD_Distribution"]["gmd:transferOptions"]["gmd:MD_DigitalTransferOptions"]["gmd:onLine"][2]["gmd:CI_OnlineResource"]["gmd:name"]["gco:CharacterString"]["#text"])
    .then (() => this.correct = true)
 }

  };

  
</script>