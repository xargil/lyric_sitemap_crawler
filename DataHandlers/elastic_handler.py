from elasticsearch import Elasticsearch


class ElasticSeachHandler:
    ES_INDEX = "allsonglyrics"
    ES_TYPE = "song"

    def __init__(self):
        self.es = Elasticsearch()

    def index_song(self, song):
        res = self.es.index(index=self.ES_INDEX, doc_type=self.ES_TYPE, body=song)

        return res["created"]
