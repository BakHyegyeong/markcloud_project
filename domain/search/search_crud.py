from datetime import datetime
from typing import Optional

from elasticsearch import Elasticsearch
from fastapi.params import Depends

import elastic_search_config
from domain.search.search_schema import search_query

es : Elasticsearch = elastic_search_config.get_es()

# elastic search 검색
def search(query : search_query):

    # Query문 생성
    json_query = {"bool" : { "filter" : [] }}

    # 상표명(한글) or 상표명(영문) or 출원 번호 or 공고 번호 query문 추가
    if query.productName or query.productNameEng or query.applicationNumber or query.publicationNumber:
        json_query = filtering_default(query, json_query)
        print(json_query)

    # 출원일 or 상표 등록 상태 or 공고일 query문 추가
    if query.applicationDate or query.registerStatus or query.publicationDate :
        json_query = filtering_add(query, json_query)
        print(json_query)

    # 등록 번호 or 등록일 or 상품 주 분류 코드 리스트 or 상품 유사군 코드 리스트 query문 추가
    if query.registrationNumber or query.registrationPubNumber or query.registrationDate or query.registrationPubDate\
            or query.asignProductMainCodeList or query.asignProductSubCodeList:
        json_query = filtering_list(query, json_query)
        print(json_query)

    result = es.search(index="markcloud", query=json_query)

    return result

# 상표명(한글) or 상표명(영문) or 출원 번호 or 공고 번호 query문 추가
def filtering_default(query, json_query : dict):

    if query.productName:
        json_query["bool"]["filter"].append({"match" : {"productName": query.productName}})

    if query.productNameEng:
        json_query["bool"]["filter"].append({"match": {"productNameEng": query.productNameEng}})

    if query.applicationNumber:
        json_query["bool"]["filter"].append({"match": {"applicationNumber": query.applicationNumber}})

    if query.publicationNumber:
        json_query["bool"]["filter"].append({"match": {"publicationNumber": query.publicationNumber}})

    return json_query

# 출원일 or 상표 등록 상태 or 공고일 query문 추가
def filtering_add(query, json_query : dict) :

    if query.applicationDate:
        json_query["bool"]["filter"].append({"term" : {"applicationDate": query.applicationDate}})

    if query.registerStatus:
        json_query["bool"]["filter"].append({"term": {"registerStatus": query.registerStatus}})

    if query.publicationDate:
        json_query["bool"]["filter"].append({"term": {"publicationDate": query.publicationDate}})

    return json_query

# 등록 번호 or 등록일 or 상품 주 분류 코드 리스트 or 상품 유사군 코드 리스트 query문 추가
def filtering_list(query : search_query, json_query : dict):

    if query.registrationNumber:
        json_query["bool"]["filter"].append({"term": {"registrationNumber": query.registrationNumber}})

    if query.registrationPubNumber:
        json_query["bool"]["filter"].append({"term": {"registrationPubNumber": query.registrationPubNumber}})

    if query.registrationDate:
        json_query["bool"]["filter"].append({"term": {"registrationDate": query.registrationDate}})

    if query.registrationPubDate:
        json_query["bool"]["filter"].append({"term": {"registrationPubDate": query.registrationPubDate}})

    if query.asignProductMainCodeList:
        json_query["bool"]["filter"].append({"match": {"asignProductMainCodeList": query.asignProductMainCodeList}})

    if query.asignProductSubCodeList:
        json_query["bool"]["filter"].append({"match": {"asignProductSubCodeList": query.asignProductSubCodeList}})

    return json_query