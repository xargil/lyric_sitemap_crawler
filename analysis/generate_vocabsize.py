import elasticsearch
from nltk import collections
from analysis import ES_INDEX, ES_TYPE
import nltk
from nltk.corpus import stopwords
import pickle

NUM_OF_SONGS = 1000

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
                "size": 8
            }
        }
    }
}

res = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=get_all_genres)
print("%s\t%s\t%s\t%s" % ("Genre", "Lexical Richness", "Num words in songs", "Num distinct words in songs"))
# Generate vocab ratio per genre:
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
        ]}}, "size": 0, "terminate_after": 100,
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
    unq = vocabsize['aggregations']['uniquecounts']['value']
    total = vocabsize['aggregations']['counts']['value']
    print("%s\t%s\t%s\t%s" % (genre['key'], unq / total, total, unq))

for genre in res['aggregations']['genres']['buckets']:
    curr_gnere = genre["key"]
    genre_songs_list = []

    songs_by_genre = {
      "query": {
        "match": {
          "album.genre": curr_gnere
        }
      },
      "size": NUM_OF_SONGS
    }
    res = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=songs_by_genre)
    for song in res["hits"]["hits"]:
        lyrics = song["_source"]["lyrics"]
        tokens = nltk.word_tokenize(lyrics)
        filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
        tokens_counter = collections.Counter(filtered_tokens)
        tuple_list = list(tokens_counter.items())
        genre_songs_list.append(tuple_list)

    with open('/home/omri/Dev/Python/IntroToDS/Data/pickle_list/' + curr_gnere + '.pickle', 'wb') as handle:
        pickle.dump(genre_songs_list, handle, protocol=pickle.HIGHEST_PROTOCOL)