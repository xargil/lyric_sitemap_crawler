import elasticsearch
# from pytagcloud import create_tag_image, make_tags
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

from analysis import ES_INDEX, ES_TYPE
from spacy import en

stopwords = set(list(en.STOP_WORDS) + ["i'm", "it's", "you're", "don't", "i've", "there's", "we're", "that's", "ain't"])

es = elasticsearch.Elasticsearch()
get_all_genres = {
    "query": {
        "query_string": {
            "query": "album.genre:*"
        }
    },
    "size": 0,
    "aggs": {
        "genres": {
            "terms": {
                "field": "album.genre.keyword",
                "size": 8
            }
        }
    }
}

res = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=get_all_genres)
print("%s\t%s" % ("Genre", "Vocabulary Size"))
for genre in res['aggregations']['genres']['buckets']:
    vocab_per_genre = {
        "query": {"bool": {"must": [
            {"match": {
                "album.genre.keyword": genre['key']
            }}, {"range": {
                "album.year": {
                    "gte": 1950,
                    "lte": 2006
                }
            }}
        ]}}, "size": 0, "terminate_after": 1000,
        "aggs": {
            "uniquecounts": {
                "cardinality": {
                    "field": "lyrics"
                }
            },
            "counts": {
                "value_count": {
                    "field": "lyrics"
                }
            }
        }
    }
    vocabsize = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=vocab_per_genre)
    print("%s\t%s" % (
    genre['key'], vocabsize['aggregations']['uniquecounts']['value'] / vocabsize['aggregations']['counts']['value']))
