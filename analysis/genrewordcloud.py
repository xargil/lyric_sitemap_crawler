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
                "size": 10
            }
        }
    }
}

res = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=get_all_genres)
for genre in res['aggregations']['genres']['buckets']:
    cloud_per_genre = {
        "query": {"bool": {"must": [
            {"match": {
                "album.genre.keyword": genre['key']
            }}, {"range": {
                "album.year": {
                    "gte": 1950,
                    "lte": 2017
                }
            }}
        ]}}, "size": 0,
        "aggs": {
            "wordcloud": {
                "significant_terms": {
                    "field": "lyrics",
                    "size": 100
                }
            }
        }
    }
    wcloud = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=cloud_per_genre)
    termandcounts = [(x['key'], x['doc_count']) for x in wcloud['aggregations']['wordcloud']['buckets'] if
                     x['key'].lower() not in stopwords]
    cloud = WordCloud(width=600, height=600, scale=0.5, stopwords=stopwords).generate_from_frequencies(termandcounts)
    plt.imsave('analysis/wordcloud/wordcloud_%s.png' % genre['key'], cloud)
