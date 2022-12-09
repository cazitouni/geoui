
<template>
	<v-sheet align="center">
		<AppBar/>
		<v-container >
			<v-row justify="center">
				<v-card v-for="element in projets" :key="element.id" outlined elevation="2" class="  ma-4" max-width="344" style="height:600px;width: 344px;" >    
					<v-img style="height: 200px;" v-if="(element._source.overview)" :aspect-ratio="16/9"   :src ="element._source.overview[0].url"></v-img>
					<v-img v-else :aspect-ratio="16/9"    :src ="'https://cdn.vuetifyjs.com/images/parallax/material.jpg'"></v-img>
					<v-card-title   class="text-break"   style="height:150px;text-align:inherit;"> {{element._source.resourceTitleObject.default}}</v-card-title>
					<v-divider ></v-divider>
					<div v-if="element._source.resourceAbstractObject !== undefined" style="height:150px;margin-left: 2px;margin-right: 2px;margin-top:30px;text-align:inherit;"><p v-snip="{ lines: 6 }" style="max-height: 150px;">{{element._source.resourceAbstractObject.default}}</p></div>
					<v-btn style="height: 40px;margin-top: 20px;position: absolute;bottom: 0;" @click="$router.push({ path: element._source.metadataIdentifier})" tile text color="green darken-3" class="white--text"  block>Consulter</v-btn>
				</v-card>
			</v-row>
			<ObServer @intersect="getNextResults"/>
		</v-container>
	</v-sheet>
</template>

<script>
import axios from 'axios'
import AppBar from './AppBar'
import ObServer from "./ObServer";

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
      projets: {},
    }
  },

methods:{
  async getInitialResults(){
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
    axios
    .post("https://catalog.wpsiglw.cus.fr/geonetwork/srv/api/search/records/_search?bucket=s101", data)
    .then(response => (this.projets = response.data.hits.hits))
  },
  async getNextResults(){
	data.from  += 8;
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
    axios
    .post("https://catalog.wpsiglw.cus.fr/geonetwork/srv/api/search/records/_search?bucket=s101", data)
    .then(response => this.projets = [...this.projets, ...response.data.hits.hits])
  },
},
  
computed: {

},

components: {
    AppBar,
    ObServer
  },
  beforeMount() {
    this.getInitialResults();
  },
  mounted () {

  },

}
</script>
