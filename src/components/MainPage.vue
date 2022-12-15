<template>
	<v-sheet align="center">
		<v-toolbar color="green darken-3"  dense elevation="12"  class="fixed-bar">
  			<v-text-field lazy @keyup="onEnter()" v-model="searchText" label="Rechercher dans le catalogue" dark hide-details color="light-blue accent-3" prepend-icon="mdi-magnify" single-line></v-text-field>
		</v-toolbar>
		<v-container>
			<v-row justify="center">
				<v-card id="card" v-for="element in projets" :key="element._source.metadataIdentifier" outlined elevation="2" class="ma-4">    
					<v-img v-if="element._source.overview" :aspect-ratio="16/9"   :src ="element._source.overview[0].url"></v-img>
					<v-img v-else :aspect-ratio="16/9"    :src ="'https://cdn.vuetifyjs.com/images/parallax/material.jpg'"></v-img>
					<v-card-title class="text-break">{{element._source.resourceTitleObject.default}}</v-card-title>
					<v-btn id="cardBtn" @click="onClickConsulter(element._source.metadataIdentifier)" tile text color="green darken-3" class="white--text" block>Consulter</v-btn>
				</v-card>
			</v-row>
			<ObServer @intersect="getNextResults"/>
		</v-container>
	</v-sheet>
</template>
<script>
import axios from 'axios'
import ObServer from "./ObServer";
var text = '';
var data = {
	"from": 0,
    "size": 8,
	"sort": [
		"_score"
	],
	"query": {
		"function_score": {
			"boost": "5",
			"functions": [
				{
					"filter": {
						"exists": {
							"field": "parentUuid"
						}
					},
					"weight": 0.3
				},
				{
					"filter": {
						"match": {
							"cl_status.key": "obsolete"
						}
					},
					"weight": 0.3
				},
				{
					"gauss": {
						"dateStamp": {
							"scale": "365d",
							"offset": "90d",
							"decay": 0.5
						}
					}
				}
			],
			"score_mode": "multiply",
			"query": {
				"bool": {
					"must": [
						{
							"terms": {
								"isTemplate": [
									"n"
								]
							}
						}
					]
				}
			}
		}
	},
	"aggregations": {
		"cl_hierarchyLevel.key": {
			"terms": {
				"field": "cl_hierarchyLevel.key"
			},
			"aggs": {
				"format": {
					"terms": {
						"field": "format"
					}
				}
			}
		},
		"cl_spatialRepresentationType.key": {
			"terms": {
				"field": "cl_spatialRepresentationType.key",
				"size": 10
			}
		},
		"availableInServices": {
			"filters": {
				"filters": {
					"availableInViewService": {
						"query_string": {
							"query": "+linkProtocol:/OGC:WMS.*/"
						}
					},
					"availableInDownloadService": {
						"query_string": {
							"query": "+linkProtocol:/OGC:WFS.*/"
						}
					}
				}
			}
		},
		"th_gemet_tree.default": {
			"terms": {
				"field": "th_gemet_tree.default",
				"size": 100,
				"order": {
					"_key": "asc"
				},
				"include": "[^^]+^?[^^]+"
			}
		},
		"th_httpinspireeceuropaeumetadatacodelistPriorityDataset-PriorityDataset_tree.default": {
			"terms": {
				"field": "th_httpinspireeceuropaeumetadatacodelistPriorityDataset-PriorityDataset_tree.default",
				"size": 100,
				"order": {
					"_key": "asc"
				}
			}
		},
		"tag.default": {
			"terms": {
				"field": "tag.default",
				"include": ".*",
				"size": 10
			},
			"meta": {
				"caseInsensitiveInclude": true
			}
		},
		"th_regions_tree.default": {
			"terms": {
				"field": "th_regions_tree.default",
				"size": 100,
				"order": {
					"_key": "asc"
				}
			}
		},
		"resolutionScaleDenominator": {
			"histogram": {
				"field": "resolutionScaleDenominator",
				"interval": 10000,
				"keyed": true,
				"min_doc_count": 1
			},
			"meta": {
				"collapsed": true
			}
		},
		"creationYearForResource": {
			"histogram": {
				"field": "creationYearForResource",
				"interval": 5,
				"keyed": true,
				"min_doc_count": 1
			},
			"meta": {
				"collapsed": true
			}
		},
		"OrgForResource": {
			"terms": {
				"field": "OrgForResource",
				"include": ".*",
				"size": 15
			},
			"meta": {
				"caseInsensitiveInclude": true
			}
		},
		"cl_maintenanceAndUpdateFrequency.key": {
			"terms": {
				"field": "cl_maintenanceAndUpdateFrequency.key",
				"size": 10
			},
			"meta": {
				"collapsed": true
			}
		}
	},
}
export default{
  data () {
    return {
      projets: [],
	  searchText : ''
    }
  },
methods:{
	onClickConsulter(metadataIdentifier) {
    this.$router.push({ path: metadataIdentifier });
  },
  async getInitialResults(){
	data.from = 0
	try{
		delete data.query.function_score.query.bool.must[1]
		data.query.function_score.query.bool.must.splice(1,1)
	}catch(error){}
    axios
    .post("https://catalog.wpsiglw.cus.fr/geonetwork/srv/api/search/records/_search?bucket=s101", data)
    .then(response => (this.projets = response.data.hits.hits))
  },
  async getNextResults(){
	data.size += 8;
    axios
    .post("https://catalog.wpsiglw.cus.fr/geonetwork/srv/api/search/records/_search?bucket=s101", data)
    .then(response => this.projets = response.data.hits.hits)
  },
   async onEnter(){
	data.from = 0
	if (this.searchText !== ''){
		if(this.searchText.endsWith(" ")){text = this.searchText.replace(/\s/g, '');}
		else{text = this.searchText}
		data.query.function_score.query.bool.must[1] = { ...data.query.function_score.query.bool.must[1], query_string: { query: `(any:(*${text}*)resourceTitleObject.default:(*${text}*)^3)` }}
	}
	else
	{
		data.from = 0
		delete data.query.function_score.query.bool.must[1]
		data.query.function_score.query.bool.must.splice(1,1)
	}
		axios
		.post("https://catalog.wpsiglw.cus.fr/geonetwork/srv/api/search/records/_search?bucket=s101", data)
		.then(response => this.projets = response.data.hits.hits)
  }  
},
components: {
    ObServer
  },
  beforeMount() {
    this.getInitialResults();
  },
}
</script>
<style scoped>
.fixed-bar {
	width : 100%;
	position: sticky;
	position: -webkit-sticky;
	top: 0em;
	z-index: 3;
}
#cardBtn{
	height: 50px;
	margin-top: 20px;
	position: absolute;
	bottom: 0;
}
#card{
	height:400px;
	width: 344px;
	border-radius: 0;
	max-width:344px;
}
</style>
