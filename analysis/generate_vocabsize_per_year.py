import elasticsearch
from analysis import ES_INDEX, ES_TYPE

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
print("%s\t%s" % ("Genre", "Lexical Richness"))

# Generate Lexical Richness ratio per year:
for y in range(1970, 2008, 1):
    vocab_per_genre = {
        "query": {"bool": {"must": [
            {"range": {
                "album.year": {
                    "gte": y,
                    "lte": y + 1
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
    print("%s\t%s" % (
        y, vocabsize['aggregations']['uniquecounts']['value'] / vocabsize['aggregations']['counts']['value']))
