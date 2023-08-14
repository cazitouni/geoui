<template>
	<v-container fluid v-if="projets && projets.resourceTitleObject.default" class="fill-height">
<!-- Boutton retour -->
		<v-row>
			<v-btn tile text color="green darken-3" class="white--text ma-4" @click="$router.push('/')">
				<v-icon dark>mdi-arrow-left</v-icon> Retour
			</v-btn>
		</v-row>
<!-- Titre -->
		<v-row justify="center">
			<h1 class="text-center ma-4">{{ projets.resourceTitleObject.default }}</h1>
		</v-row>
<!-- Menu Mobile-->
		<v-row justify="center" class="d-md-none">
			<v-menu offset-y >
				<template v-slot:activator="{ on }">
					<v-btn tile text color="green darken-3" class="ma-4 white--text" v-on="on" style="width:70%;font-weight: bold;">
						<v-icon dark>mdi-menu</v-icon> {{ activeSection }}
					</v-btn>
				</template>
				<v-list>
					<v-list-item @click="activeSection = 'Résumé'">
						<v-list-item-title>Résumé</v-list-item-title>
					</v-list-item>
					<v-list-item v-for="(section, index) in sections" :key="index" @click="activeSection = section" v-if="section !== 'Résumé'">
						<v-list-item-title>{{ section }}</v-list-item-title>
					</v-list-item>
				</v-list>
			</v-menu>
		</v-row>
<!-- Sélecteur Desktop -->
		<v-row justify="center" class="d-none d-md-flex">
			<v-btn-toggle class="mb-4">
				<v-btn
					v-for="(section, index) in sections" :key="index" @click="activeSection = section" :outlined="activeSection !== section" :class="{ 'green--text text--darken-2': activeSection === section }" :style="{ fontWeight: activeSection === section ? 'bold' : 'normal' }">
					{{ section }}
				</v-btn>
			</v-btn-toggle>
		</v-row>
<!-- Feuille -->
<v-row justify="center" class="fill-height">
			<v-sheet elevation="12" :class="[{'pa-2 ma-2': $vuetify.breakpoint.xsOnly}, {'pa-6 ma-4 w-100 ': !$vuetify.breakpoint.mdOnly}]" align="center">
				<h2 class="ma-4" v-if="activeSection === 'Résumé'">Résumé :</h2>
				<h4 class="word-break text-justify ma-4" v-if="activeSection === 'Résumé'">{{ projets.resourceAbstractObject.default }}</h4>
				<h2 class="ma-4" v-if="activeSection === 'Méthodologie'">Méthodologie:</h2>
				<h4 class="word-break text-justify ma-4" v-if="activeSection === 'Méthodologie'">{{ projets.lineageObject.default }}</h4>
				<h2 class="ma-4" v-if="activeSection === 'Contact'">Contact:</h2>
				<h4 class="word-break text-justify ml-4 mr-4" v-if="activeSection === 'Contact'">{{ projets.contact[0].individual }}</h4>
				<h4 class="word-break text-justify ml-4 mr-4" v-if="activeSection === 'Contact'">{{ projets.contact[0].position }}</h4>
				<h4 class="word-break text-justify ml-4 mr-4" v-if="activeSection === 'Contact'">{{ projets.contact[0].phone }}</h4>
				<h4 class="word-break text-justify ml-4 mr-4" v-if="activeSection === 'Contact'">{{ projets.contact[0].email }}</h4>
				<h2 class="ma-4" v-if="activeSection === 'Données'">Données:</h2>
				<div v-for="element in projets.link" :key="element.id" class="word-break text-justify ml-4 mr-4" v-if="activeSection === 'Données'">
					<h4><a :href="element.url">{{ element.description }}</a></h4>
				</div>
			</v-sheet>
		</v-row>
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
      projets : null,
      correct: false,
      id : this.$route.path.split('/')[1],
	  sections: ['Résumé', 'Méthodologie', 'Contact', 'Données'],
      activeSection: 'Résumé',
    }
  },
methods:{
	async getHit() {
    data.query.bool.must[0].multi_match.query = this.id;
    try {
      const response = await axios.post("https://catalog.wpsiglw.cus.fr/geonetwork/srv/api/search/records/_search", data);
      const hit = response.data.hits.hits[0]._source;
      if (hit) {
        this.projets = {
            resourceTitleObject: hit.resourceTitleObject || { default: '' },
            resourceAbstractObject: hit.resourceAbstractObject || { default: '' },
            lineageObject: hit.lineageObject || { default: '' },
            contact: hit.contact || [
              {
                individual: '',
                position: '',
                phone: '',
                email: ''
              }
            ],
            link: hit.link || []
        };
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
},
computed:{
},
 beforeMount() {
  this.getHit();
}
  };
</script>
