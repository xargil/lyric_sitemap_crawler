import elasticsearch
import os

es = elasticsearch.Elasticsearch()
DATA_BASEPATH = os.environ.get('DATA_BASEPATH')
ES_INDEX = 'allsonglyrics'
ES_TYPE = 'song'
