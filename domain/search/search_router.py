from datetime import datetime
from typing import Optional
from fastapi import Query, HTTPException, APIRouter, Depends
from starlette import status

from domain.search import search_crud
from domain.search.search_schema import search_query

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

@router.get("/")
async def search(query : search_query = Depends(search_query)):

    # 요청 검색 데이터가 한 개도 없을 경우 400 오류를 반환한다.
    if any([
        query.productName, query.productNameEng, query.applicationNumber,
        query.publicationNumber, query.applicationDate, query.registerStatus,
        query.publicationDate, query.registrationNumber, query.registrationPubNumber,
        query.registrationDate, query.registrationPubDate,
        query.asignProductMainCodeList, query.asignProductSubCodeList
    ]) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="요청 데이터는 최소 1개 이상 존재해야 합니다.")

    result = search_crud.search(query)

    if result['hits']['hits'] :
        return result['hits']['hits']
    else :
        # 검색 결과가 없을 경우 404 오류를 반환한다.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="검색 결과가 없습니다.")


