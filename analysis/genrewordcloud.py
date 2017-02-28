import elasticsearch
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from analysis import ES_INDEX, ES_TYPE
from spacy import en

# Stopwords and other words we don't want to appear in the word cloud:
stopwords = set(
    list(en.STOP_WORDS) + ["i'm", "it's", "you're", "don't", "i've", "there's", "we're", "that's", "ain't", "i'll",
                           "she's"])
es = elasticsearch.Elasticsearch()

# Bring 8 most common genres from the index:
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
# Generate word cloud for each genre
for genre in res['aggregations']['genres']['buckets']:
    # Get list of 100 top "important" terms for the genre from years 1950 to 2006
    cloud_per_genre = {
        "query": {"bool": {"must": [
            {"match": {
                "album.genre.keyword": genre['key']
            }}, {"range": {
                "album.year": {
                    "gte": 1950,
                    "lte": 2006
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
