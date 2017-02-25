import os

import elasticsearch

es = elasticsearch.Elasticsearch()
DATA_BASEPATH = os.environ.get('DATA_BASEPATH')
ES_INDEX = 'allsonglyrics'
ES_TYPE = 'song'

q = {
    "size": 1000,
    "query": {
        "match": {
            "album.genre": "Rock"
        }
    }
}

page = es.search(index=ES_INDEX, doc_type=ES_TYPE, body=q, params={"scroll": "10m"})

sid = page['_scroll_id']
scroll_size = page['hits']['total']

# Start scrolling
while scroll_size > 0:
    print("Scrolling...")
    page = es.scroll(scroll_id=sid, scroll='2m')
    # Update the scroll ID
    sid = page['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(page['hits']['hits'])

    print("scroll size: " + str(scroll_size))
