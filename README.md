# markcloud_project
마크클라우드 백엔드 개발자 채용 과제 - 간단한 상표 검색 API 구현

## API 사용법 및 실행 방법

1. 설치 
   - FastAPI 설치 : `pip install fastapi`
   - uvicorn 설치 : `pip install "uvicorn[standard]”`
   - [Elasticsearch 서버 설치](https://www.elastic.co/kr/downloads/elasticsearch) : 운영체제에 따라 설치
   - Elasticsearch client 설치 : `pip install elasticsearch`
   - nori 설치 : `./elasticsearch-plugin install analysis-nori` → bin 폴더에서 입력
   - elasticdump 설치 : `npm install elasticdump`

2. index 생성
   ```json
   {
      "settings": {
        "analysis": {  
           "analyzer": {
             "nori" : {
                "tokenizer" : "nori_tokenizer"
              }
           }
        }
      },
      "mappings": {
        "properties": {
          "productName": {
            "type": "text",
            "analyzer": "nori",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "productNameEng": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "applicationNumber": {
            "type": "keyword"
          },
          "applicationDate": {
            "type": "date",
            "format": "yyyyMMdd"
          },
          "registerStatus": {
            "type": "keyword"
          },
          "publicationNumber": {
            "type": "keyword"
          },
          "publicationDate": {
            "type": "date",
            "format": "yyyyMMdd"
          },
          "registrationNumber": {
            "type": "keyword"
          },
          "registrationDate": {
            "type": "date",
            "format": "yyyyMMdd"
          },
          "registrationPubNumber": {
            "type": "keyword"
          },
            "registrationPubDate": {
            "type": "date",
            "format": "yyyyMMdd"
          },
          "internationalRegDate": {
            "type": "date",
            "format": "yyyyMMdd"
          },
          "internationalRegNumbers": {
            "type": "keyword"
          },
          "priorityClaimNumList": {
            "type": "keyword"
          },
          "priorityClaimDateList": {
            "type": "date",
            "format": "yyyyMMdd"
          },
          "asignProductMainCodeList": {
            "type": "keyword"
          },
          "asignProductSubCodeList": {
            "type": "keyword"
          },
          "viennaCodeList": {
            "type": "keyword"
          }
        }
      }
    }
   ```

3. Elasticdump로 json 데이터 저장하기

    ```shell
    elasticdump \
      --type=data \
      --input="C:\Users\Administrator\Desktop\trademark_sample.json" \
      --output="http://localhost:9200/markcloud" \
      --transform="doc._source=Object.assign({},doc)"
      
    elasticdump --type=data --input="C:\Users\Administrator\Desktop\trademark_sample.ndjson" --output="http://localhost:9200/markcloud" --transform="doc._source=Object.assign({},doc)"
   
   // 테스트용
    elasticdump --type=data --input="C:\Users\Administrator\Desktop\trademark_sample.json" --output="C:\Users\Administrator\Desktop\transformed_output.json" --transform="doc._source=Object.assign({},doc)"  
   
   ```

    > 🔔 오류 해결 : failed to parse: Limit of total fields [1000] has been exceeded while adding new fields [982]

## 구현된 기능 설명

- 서버 작동 : `uvicorn main:app --reload`
- 테스트 : `http://localhost:8000/docs`  

1. request (`/search/`) : 사용자는 search_schema에 정의된 항목들 중 **선택해 QueryString 형태로 입력**할 수 있다. 
   ```python
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
   ```
    다만 위의 항목들 중 사용자가 아무것도 보내지 않을 경우 400에러를 반환한다.
   `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="요청 데이터는 최소 1개 이상 존재해야 합니다.")`


2. response : json안의 list형식으로 반환된다. 사용자는 각 list에서 "_source"항목으로 데이터를 얻을 수 있다.
   ```json
    [
      {
        "_index": "markcloud",
        "_id": "atomq5YBSmI-KqvsQ8VF",
        "_score": 0,
        "_source": {
          "productName": "프레스카",
          "productNameEng": "FRESCA",
          "applicationNumber": "4019950043843",
          "applicationDate": "19951117",
          "registerStatus": "등록",
          "publicationNumber": "4019970001364",
          "publicationDate": "19970129",
          "registrationNumber": [
            "4003600590000"
          ],
          "registrationDate": [
            "19970417"
          ],
          "registrationPubNumber": null,
          "registrationPubDate": null,
          "internationalRegDate": null,
          "internationalRegNumbers": null,
          "priorityClaimNumList": null,
          "priorityClaimDateList": null,
          "asignProductMainCodeList": [
            "30"
          ],
          "asignProductSubCodeList": [
            "G0301",
            "G0303",
            "G0302"
          ],
          "viennaCodeList": null
        }
      }
    ]
    ```
   다만 결괏값이 없을 경우 404에러를 반환한다. <br>
    `raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="검색 결과가 없습니다.")`

### 파일 구조 설명

- domain/search : search의 router, crud, schema파일이 저장된다.
  - search_router : 사용자가 요청할 API를 정의
  - search_crud : Elastic Search에서 데이터를 조회하는 로직
    - elastic search서버에 요청할 때 elastic search의 query항목에 검색 query문을 저장하므로 **bool, filter 안에 검색 조건들이 저장된다.** 
    - 사용자의 요청에 따라 filtering할 항목의 query문을 추가한다.
    - 각 데이터가 가지고 있는 고유한 값을 제외하고는 형태소를 분석할 필요가 없고 정확히 일치하는 값만 반환해야하기에 term 방식으로 데이터를 조회한다.
  - search_schema : 사용자에게 받을 Query의 Pydantic 모델

- elastic_search_config : elastic search 연결 객체를 생성하고 반환한다.
- main.py : search_router 등록

## 기술적 의사결정에 대한 설명

1. Elastic Search
    - 키워드가 정확하게 일치하지 않더라도 데이터베이스에서 값을 찾는 방법은 like 연산을 사용하는 방법이 있다.
    - 하지만 이 방법은 모든 row를 full scan방식으로 데이터를 탐색하기에 데이터의 양이 많을수록 그에 비례해 시간이 오래 걸리게 된다.
    - 이는 대량의 데이터에서 치명적인 약점이 된다.
    - 따라서 Elastic Search를 도입해 **Inverted Index**를 통한 빠른 속도의 검색 기능을 구현하고자 하였다.   


2. Elasticdump : Json 데이터를 Elastic Search에 저장
    - Elastic Search Client : 적은 양의 데이터를 넣을 때는 가장 간단하고 쉬운 방법이지만 json 파일이기도 하고 양이 많아 적합하지 않다.
    - Bulk REST API : curl이나 HTTP 요청을 통해 데이터를 넣는 방법이지만 위와 마찬가지로 파일에는 적합하지 않다.
    - Logstash : 기존에 이미 Logstash를 사용하고 있었다면 가장 좋은 방법이었겠지만 데이터 저장만을 위해 도입하기에는 무거운 프로그램이다.
    - Elastic Search Client, Bulk REST API 등의 방법도 있지만 데이터가 json 파일이기도 하고 양이 많아 파일 단위로 json 데이터를 저장할 수 있는 Elasticdump가 가장 유리한 조건에 있었다.


3. 상표 검색 API를 최소 1개 이상 구현할 것 & 최소한 하나 이상의 필터링 기능을 구현할 것
    - 각각의 분류에 따라 필터링마다 API를 구현하는 방법도 생각했었지만 이는 프론트엔드에서 사용자의 값마다 if문으로 api를 선택하고 요청하는 등 별도의 과정을 거쳐야했기에 <u>API를 1개로 구현하기로 하였다.</u>
    - 필터링 조건마다 쿼리문을 따로 정의한 후 사용자의 요청에 따라 쿼리문 내용을 추가하는 방식으로 구현하고자 한다.


4. 검색조건 : 기본값 , 추가값, 리스트, NULL값
    - 기본값 : 아래의 항목은 데이터마다 고유한 값으로 식별자로 사용될 수 있다.

        - productName: 상표명(한글)
        - productNameEng: 상표명(영문
        - applicationNumber: 출원 번호
        - publicationNumber: 공고 번호
    - 추가값 : 아래의 항목은 다른 데이터와 동일할 수 있는 값이기에 추가 조건으로 설계하였다.
        - applicationDate: 출원일 (YYYYMMDD 형식)
        - registerStatus: 상표 등록 상태 (등록, 실효, 거절, 출원 등)
        - publicationDate: 공고일 (YYYYMMDD 형식)
    - 리스트 : List형식으로 값을 가지고 있는 column
        - registrationNumber: 등록 번호
        - **registrationPubNumber**
        - registrationDate: 등록일 (YYYYMMDD 형식)
        - **registrationPubDate**
        - asignProductMainCodeList: 상품 주 분류 코드 리스트
        - asignProductSubCodeList: 상품 유사군 코드 리스트
    - NULL : 값이 NULL일수도 있는 column
        - internationalRegNumbers: 국제 출원 번호
        - internationalRegDate: 국제출원일 (YYYYMMDD 형식)
        - priorityClaimNumList: 우선권 번호
        - priorityClaimDateList: 우선권 일자 (YYYYMMDD 형식)
    - viennaCodeList: 비엔나 코드 리스트 : 리스트 또는 NULL 값을 가질 수 있는 column


5. QueryString : Naver 같은 사이트에서도 검색에서는 QueryString을 사용하는 경우가 대부분이고 
   검색 정보는 body안에 담을 정도로 민감한 정보가 아니다. <br>
   ex) `https://mail.naver.com/v2/folders/0/search?detail=true&from=%EB%A7%88%ED%81%AC%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C&body=%EB%B0%B1%EC%97%94%EB%93%9C&bodyCond=5&exceptTrash=true&type=all`


6. Depends : FastAPI에서 제공하는 의존성 주입 도구이다. param에서 사용하면 param의 값에 맞게 Pydantic 모델의 인스턴스를 생성하고, 
    반환한다. 이는 param의 값이 많을수록 더 효율적이게 된다. <br>
    → 추후 필터링할 조건이 추가된다면 router파일은 변경 없이 crud, schema 파일만 수정하면 된다.

## 문제 해결 과정에서 고민했던 점

> 🔔 오류 해결 : failed to parse: Limit of total fields [1000] has been exceeded while adding new fields [982]

limit가 1000으로 제한되어있고 이를 초과해서 발생한 오류였다. 

기존에 transformed_output.json으로 transform된 결과를 확인했을 때 데이터가 `{"_source":{ "field1" : "value1" }}`의
형태로 **올바르게 저장된 것을 확인했었고 주어진 데이터에서 필드의 개수는 총 18개**로 List가 있다고 하더라도
발생하기 어려운 오류였다.

어떤 문제인지 확인하기 위해 일단 데이터가 어떤 형태로 저장되는지를 확인했어야 했다. 
따라서 한번에 저장하는 데이터의 양을 10으로 제한한 후 limit를 늘리면서 저장을 시도하였다.

limit를 30000으로 설정한 후 결과를 보니 아래처럼 하나의 document 안에 모든 데이터가 다 들어가는 오류가 발생했었다.

```json
"_score": 1,
"_source": {
"0": {
	"productName": "프레스카",
	"productNameEng": "FRESCA",
	"applicationNumber": "4019950043843",
	"applicationDate": "19951117",
	...
	"asignProductSubCodeList": [
		"G0301",
		"G0303",
		"G0302"
	],
	"viennaCodeList": null
	},
"1": {
	"productName": "간호사 타이쿤",
	"productNameEng": null,
	"applicationNumber": "4520070002566",
	"applicationDate": "20070629",
	"registerStatus": "실효",
	"publicationNumber": "4520080005620",
	"publicationDate": "20080131",
	...
	"asignProductMainCodeList": [
		"41",
		"09"
	],
	"asignProductSubCodeList": [
	"S121002",
	"G390802"
	],
	"viennaCodeList": null
	},
"2": {
	"productName": "제이케",
	"productNameEng": "JK",
	"applicationNumber": "4019630000130",
	"applicationDate": "19630214",
	"registerStatus": "실효",
	"publicationNumber": "4019630007648",
	"publicationDate": "19630308",
	"registrationNumber": [
		"4000076480000"
	],
        ...
```

Elasticdump 사용예시를 검색해보던 중 데이터가 `{“key”:"value", “key”:"value"},{“key”:"value", “key”:"value"}`형태인 것을 보고 
해결방법을 떠올릴 수 있었다.

기존의 json데이터가 []형태이다보니 하나의 객체로 인식하고 parsing하다보니 저런 오류가 발생한 것 같았다.

따라서 기존의 json데이터를 ndjson형태로 바꾸었다. <br>
→ json데이터가 `[ “key” : “value”, “key” : “value” ]` 형태라면 ndjson은 `{“key”:"value"}, {“key”:"value"}`형태로 []항목이 없다.

## 개선하고 싶은 부분

1. Kibana, Logstash로 연계해서 로그를 수집하고 이를 기반으로 유의미한 통계 결과를 추출할 수 있도록 한다.
2. Redis를 활용한 캐싱 기능을 구현해 자주 검색되는 데이터의 경우 빠르게 제공될 수 있도록 한다.
