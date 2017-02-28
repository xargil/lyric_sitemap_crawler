import numpy as np
import elasticsearch
import random
from langdetect import detect

ES_INDEX = 'allsonglyrics'
ES_TYPE = 'song'

es = elasticsearch.Elasticsearch()
q = {
    "size": 1,
    "query": {
        "function_score": {
            "query": {
                "match": {
                    "album.genre": "Hip Hop"
                }
            },
            "random_score": {"seed": 1376773391128418000}
        }
    }
}


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    # Do this to avoid division by zero when calculating log
    preds += 1e-20
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def get_rand_song():
    while True:
        q['query']['function_score']['random_score']['seed'] = random.randint(10, 10000)
        res = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=q)
        song = res['hits']['hits'][0]['_source']['lyrics']
        if detect(song) == 'en':
            break
    return song
