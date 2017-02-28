import gzip
import json
import glob
import elasticsearch
from elasticsearch import helpers
import os

import re

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

regex = re.compile(r"(&#\d*;)", re.IGNORECASE)

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
                    "fielddata": "true",

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
    actions = []
    for x in song_dict:
        x['lyrics'] = regex.sub('', x['lyrics'])
        if x['lyrics'].count(' a ') < 2:
            continue
        if x['lyrics'].count(' e ') > 0:
            continue
        if x['lyrics'].count(' un ') > 0 or x['lyrics'].count(' con ') or x['lyrics'].count(' en ') > 0:
            continue
        idfield = "%s:%s" % (x['artist']['unique_name'], x['href'])
        if idfield.count("%") + x['album']['title'].count("%") > 3:
            continue
        # try:
        #     detected_lang = detect(text=x['lyrics'][:10])
        # except LangDetectException as e:
        #     continue
        # if detected_lang != 'en':
        #     continue
        actions.append(dict(_index=ES_INDEX,
                            _type=ES_TYPE,
                            _id=idfield,
                            _source=x))
    helpers.bulk(es, actions)
