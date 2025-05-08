from elasticsearch import Elasticsearch

es : Elasticsearch = None

def create_es() :
    global es
    es = Elasticsearch('http://localhost:9200')
    # print(es.info())

def get_es() :
    global es
    if es is not None :
        return es
    else :
        print("elastic search 생성합니다")
        create_es()
        return es