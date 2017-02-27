import gzip
import json
import glob
import elasticsearch
from elasticsearch import helpers
import os

es = elasticsearch.Elasticsearch()
DATA_BASEPATH = os.environ.get('DATA_BASEPATH')
ES_INDEX = 'allsonglyrics'
ES_TYPE = 'song'

mapping = {
    "mappings": {
        ES_TYPE: {
            "properties": {
                "album": {
                    "properties": {
                        "title": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "year": {
                            "type": "long"
                        }
                    }
                },
                "artist": {
                    "properties": {
                        "unique_name": {
                            "type": "keyword"
                        }
                    }
                },
                "lyrics": {
                    "type": "text",
                    "fields": {
                        "text": {
                            "type": "text",
                        }
                    }
                },
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }
            }
        }
    }
}

es.indices.delete(index=ES_INDEX, ignore=404)
es.indices.create(index=ES_INDEX, body=mapping)

for f in glob.glob(os.path.join(DATA_BASEPATH, "*")):
    with open(f, "rb") as f:
        song_dict = json.loads(gzip.decompress(f.read()).decode())
    actions = [dict(_index=ES_INDEX,
                    _type=ES_TYPE,
                    _id="%s:%s" % (x['artist']['unique_name'], x['href']),
                    _source=x) for x in song_dict]
    helpers.bulk(es, actions)
