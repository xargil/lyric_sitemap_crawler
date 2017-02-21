from elasticsearch import Elasticsearch


class ElasticSeachHandler:
    ES_INDEX = "allsonglyrics"
    ES_TYPE = "song"

    def __init__(self):
        self.es = Elasticsearch()

    def index_song(self, song, song_id):
        res = self.es.index(index=self.ES_INDEX, doc_type=self.ES_TYPE, id=song_id, body=song)

        return res["created"]
