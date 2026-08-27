# 목표
- Silver layer -> Gold Layer로 데이터 파이프라인 연결
- 실시간 x, 배치작업 o
    - 매일 00시 5분 00초에 airflow에 등록된 DAG에 의해 집계처리, Gold에 필요로 하는 형태로 데이터 처리
        - Pandas/polars/spark를 활용 처리
        - athena/opensearch/redshit등 aws 서비스 활용 처리 
            - SQL 사용 -> athena (서버리스)
            - 인덱스 검색 -> opensearch
            - redshit 엔터프라이즈 대용량 데이터 처리용, 열검색

# 인프라 구성
- s3.tf : 보정(기존 s3 버킷 사용, 이름, 태그 조정, 삭제 여부 조정)

# 인프라 구성 후 확인
- 아테나 > 본인 작업 그룹 선택 > db 선택 > 쿼리 편집기 아래 쿼리 실행
```
-- 데이터의 총개수 조회
select count(*) as cnt
from silver_logs_tbl
where year = '2026'
	and month = '08'
	and day = '26'
	and hour = '21'
;
```

# 시나리오
- 데이터가 계속 데이터 파이프라인을 통해서 저장되고 있다
    - 파티션 기준 1시간 단위로 파티션이 분리되고 있음(24시간 풀 가동 계속 저장중)
```
00:00 ~ 01:00 → Silver 저장 (1시간내에 수십~수천회 저장, firehose등 확인)
01:00 ~ 02:00 → Silver 저장
02:00 ~ 03:00 → Silver 저장
...
22:00 ~ 23:00 → Silver 저장
23:00 ~ 24:00 → Silver 저장
```
- 미션
    - 8월 27일 00:05이 되면 Airflow에 등록된 DAG가 작동
    - 8월 26일 하루치 데이터가 모두 수집되었으므로, 일별 Gold 데이터를 생성하라
    - 방식
        - 과거의 일별 집계 Gold가 모두 필요한가? (운영 -> 일별 집계 데이터 보관)
        - 오직 집계된 전날 데이터만 필요한가? (CTAS: Create Table As Select)

    - 집계 데이터 샘플
    ```
    
    ```