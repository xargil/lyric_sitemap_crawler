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
for f in glob.glob(os.path.join(DATA_BASEPATH, "*")):
    with open(f, "rb") as f:
        song_dict = json.loads(gzip.decompress(f.read()).decode())
    actions = [dict(_index=ES_INDEX,
                    _type=ES_TYPE,
                    _id="%s:%s" % (x['artist']['unique_name'], x['href']),
                    _source=x) for x in song_dict]
    helpers.bulk(es, actions)
