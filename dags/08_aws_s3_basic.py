'''
- airflow에서 aws를 access -> operator등 도구 제공 -> 패키지 설치 필요
- docker-compose.yaml apache-airflow-providers-amazon 추가
    - _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-} ... apache-airflow-providers-amazon

- 로컬 설치: pip install apache-airflow-providers-amazon
- 원격 PC에서 AWS s3의 특정 버킷(본인 소유)에 간단하게 데이터 업로드 테스트 DAG
'''
# 1. 모듈 가져오기
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import logging
import pendulum

# 2. 환경변수(전역변수)
BUCKET_NAME = "de-ai-08-infra-827913617635"
UPLOAD_FILE_NAME = "133779567923420003.jpg"
LOCAL_PATH = f"/opt/airflow/dags/data/{UPLOAD_FILE_NAME}" # 컨테이너에서 업로드

# 4-1. 콜백 함수
def _check_s3(**kwargs):
    #S3Hooks를 이용하여 실제 업로드 되었는지 확인
    # 1. 훅 생성
    hook = S3Hook(aws_conn_id = "aws_default")
    # 2. 훅을 이용해 키 확인 -> 모든 키 조회 (임시 방편)
    keys = hook.list_keys(bucket_name = BUCKET_NAME)
    # 3. 키 확인
    if not keys:
        raise ValueError("버킷 내부에 키가 없다, 업로드 실패") # 1회성(데이터 업로드 후 사용 불가)
    # 4. 확인
    for key in keys:
        logging.info(f'키{keys}')
    pass

# 3. DAG 정의
with DAG( 
  dag_id      = "08_aws_s3_basic",
  description = "s3 단순 업로드",
  default_args= {
    "owner"           : "aic-de1-admin",    
    "retries"         : 1,
    "retry_delay"     : timedelta(minutes=1)
  },
  schedule_interval = "@daily", # 00시 01분 00초에 참고용
  start_date  = pendulum.datetime( 2026,6,29, tz=pendulum.timezone("Asia/Seoul") ),
  catchup     = False,
  tags        = ['aws', 's3']
) as dag:
    # 4. task
    # 업로드(put)
    task_upload_to_s3 = LocalFilesystemToS3Operator(
        task_id = "upload_to_s3",
        filename =  LOCAL_PATH, # 실제 local pc에 존재하는 파일의 풀 경로
        dest_key = UPLOAD_FILE_NAME, # 버킷 내부에서 객체간 구분하는 key -> 파일명으로 대체
        dest_bucket = BUCKET_NAME,
        aws_conn_id = "aws_default", # aws 접속 정보
        replace = True # key가 동일하면(동일 파일이면) -> 대체
    )
    # 체크
    task_check_s3 = PythonOperator(
        task_id = "check",
        python_callable = _check_s3
    )

    # 5. 의존성
    task_upload_to_s3 >> task_check_s3