<template> 
<div v-if="info !== null"  align="center">

<h1 class=" mt-12 mx-2 text-center ">{{info['gmd:identificationInfo']['gmd:MD_DataIdentification']['gmd:citation']['gmd:CI_Citation']['gmd:title']['gco:CharacterString']['#text']}}</h1>
<v-card  class=" mt-12 pa-1" width="80%" tiled outlined elevation="12">
<h3 class="word-break text-justify ma-12" >{{info["gmd:identificationInfo"]["gmd:MD_DataIdentification"]["gmd:abstract"]["gco:CharacterString"]["#text"]}}</h3>
</v-card>
</div>
</template>
<script>
import axios from 'axios'
  export default {
    
  data () {
    return {
      info: null,
      id : this.$route.path.split('/')[1]

    }
  },

 mounted() {
   axios
    .get('https://wisiglw.cus.fr/geonetwork/srv/api/records/' + this.id + '/formatters/json'  )
    .then(response => (this.info = response.data))
 }

  };

  
</script>