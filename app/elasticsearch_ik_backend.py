from haystack.backends.elasticsearch7_backend import Elasticsearch7SearchBackend, Elasticsearch7SearchEngine

DEFAULT_FIELD_MAPPING = {
    "type": "text",
    "analyzer": "ik_max_word",
    "search_analyzer": "ik_max_word"
}


class Elasticsearc7IkSearchBackend(Elasticsearch7SearchBackend):
    def __init__(self, *args, **kwargs):
        self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['ik_analyzer'] = {
            "type": "custom",
            "tokenizer": "ik_max_word",
        }
        super(Elasticsearc7IkSearchBackend, self).__init__(*args, **kwargs)


class Elasticsearch7IkSearchEngine(Elasticsearch7SearchEngine):
    backend = Elasticsearc7IkSearchBackend
