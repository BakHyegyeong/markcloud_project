from typing import Optional, List

from pydantic import BaseModel, Field
from datetime import datetime


class search_query(BaseModel):
    productName: Optional[str] = Field(None, description="상표명(한글)")
    productNameEng: Optional[str] = Field(None, description="상표명(영문)")
    applicationNumber: Optional[int] = Field(None, description="출원 번호")
    publicationNumber: Optional[int] = Field(None, description="공고 번호")
    applicationDate: Optional[datetime] = Field(None, description="출원일 (YYYYMMDD 형식)")
    registerStatus: Optional[str] = Field(None, description="상표 등록 상태")
    publicationDate: Optional[datetime] = Field(None, description="공고일 (YYYYMMDD 형식)")
    registrationNumber : Optional[int] = Field(None, description="등록 번호")
    registrationPubNumber : Optional[int] = Field(None, description="등록 번호")
    registrationDate : Optional[datetime] = Field(None, description="등록일 (YYYYMMDD 형식)")
    registrationPubDate : Optional[datetime] = Field(None, description="등록일 (YYYYMMDD 형식)")
    asignProductMainCodeList : Optional[int] = Field(None, description="상품 주 분류 코드 리스트")
    asignProductSubCodeList : Optional[str] = Field(None, description="상품 주 분류 코드 리스트")