import requests
import json

query = None

data = {
	"from": 0,
    "size": 40,
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
                            "query_string": {
                                "query": "(any:({}) resourceTitleObject.default:({})^2)".format(query, query)
                            }
                        },
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
				"caseInsensitiveInclude": True
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
				"keyed": True,
				"min_doc_count": 1
			},
			"meta": {
				"collapsed": True
			}
		},
		"creationYearForResource": {
			"histogram": {
				"field": "creationYearForResource",
				"interval": 5,
				"keyed": True,
				"min_doc_count": 1
			},
			"meta": {
				"collapsed": True
			}
		},
		"OrgForResource": {
			"terms": {
				"field": "OrgForResource",
				"include": ".*",
				"size": 15
			},
			"meta": {
				"caseInsensitiveInclude": True
			}
		},
		"cl_maintenanceAndUpdateFrequency.key": {
			"terms": {
				"field": "cl_maintenanceAndUpdateFrequency.key",
				"size": 10
			},
			"meta": {
				"collapsed": True
			}
		}
	},
	"_source": {
		"includes": [
			"uuid",
			"id",
			"creat*",
			"group*",
			"logo",
			"category",
			"topic*",
			"inspire*",
			"resource*",
			"origin*",
			"draft",
			"overview.*",
			"owner*",
			"link*",
			"image*",
			"status*",
			"rating",
			"tag*",
			"geom",
			"contact*",
			"*Org*",
			"hasBoundingPolygon",
			"isTemplate",
			"valid",
			"isHarvested",
			"dateStamp",
			"documentStandard",
			"cl_status*",
			"mdStatus*"
		]
	},
	"track_total_hits": True
}

headers = {"Content-Type": "application/json; charset=UTF-8"}

if query is None :
    del data["query"]["function_score"]["query"]["bool"]["must"][0]

x = requests.post("https://wisiglw.cus.fr/geonetwork/srv/api/search/records/_search?bucket=s101", headers=headers, json=data)


with open('json_data.json', 'w') as outfile:
    json.dump(x.json(), outfile)