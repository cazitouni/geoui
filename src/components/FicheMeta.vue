<template> 
<v-container fluid v-if="projets._source.resourceTitleObject.default">
<v-row>
	<v-btn tile text color="green darken-3" class="white--text ma-4"  @click="$router.push('/')"> <v-icon dark>mdi-arrow-left</v-icon> Retour</v-btn>
</v-row>
<v-card outlined elevation="12" class="ma-4 pa-4" v-if="projets">
<v-row justify="center">
	<h1 class="text-center ma-4">{{projets._source.resourceTitleObject.default}}</h1>
</v-row>
<h2 class="ma-4" >Résumé :</h2>
<h4 class="word-break text-justify ma-4">{{projets._source.resourceAbstractObject.default}}</h4>
<h2 class="ma-4">Mise à jour:</h2>
<h4 class="word-break text-justify ma-4">{{projets._source.lineageObject.default}}</h4>
<h2 class="ma-4">Contact:</h2>
<h4 class="word-break text-justify ml-4 mr-4 ">{{projets._source.contact[0].individual}}</h4>
<h4 class="word-break text-justify ml-4 mr-4 ">{{projets._source.contact[0].position}}</h4>
<h4 class="word-break text-justify ml-4 mr-4 ">{{projets._source.contact[0].phone}}</h4>
<h4 class="word-break text-justify ml-4 mr-4 ">{{projets._source.contact[0].email}}</h4>
<h2 class="ma-4">Données:</h2>
<div v-for="element in projets._source.link" :key="element.id" class="word-break text-justify ml-4 mr-4 ">
<h4><a :href="element.url">{{element.description}}</a></h4>
</div>
</v-card>
</v-container>
</template>
<script>
import axios from 'axios'
var data = {
	"query": {
		"bool": {
			"must": [
				{
					"multi_match": {
						"query": "",
						"fields": [
							"id",
							"uuid"
						]
					}
				},
				{
					"terms": {
						"isTemplate": [
							"n",
							"y"
						]
					}
				},
				{
					"terms": {
						"draft": [
							"n",
							"y",
							"e"
						]
					}
				}
			]
		}
	}
}
export default {
    
  data () {
    return {
      projets : [],
      correct: false,
      id : this.$route.path.split('/')[1],
    }
  },
methods:{
  async getHit(){
	  data.query.bool.must[0].multi_match.query = this.id;
    axios
    .post("https://catalog.wpsiglw.cus.fr/geonetwork/srv/api/search/records/_search", data)
    .then(response => this.projets = response.data.hits.hits[0])
  },
},
computed:{
},
 beforeMount() {
  this.getHit();
}
  };
</script>
