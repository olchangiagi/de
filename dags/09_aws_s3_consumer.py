'''
- 활용 분야
    - 소카: 렌터카 반납 -> 사진 촬영 업로드(s3) -> 트리거(변화) -> 이미지 판독(파손///) : 분석 -> 판정
- 동작
    - 버킷내 특정 공간 감시(sensor) -> 파일 업로드 동작 -> 감지 -> DAG의 TASK가 작동
'''

# 1. 모듈 
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor # 키 감시용
from airflow.providers.amazon.aws.operators.s3 import S3DeleteObjectsOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import pendulum

# 2. 환경 변수
BUCKET_NAME = "de-ai-08-infra-827913617635"
UPLOAD_FILE_NAME = "sensor_data.csv" # 현재 시간등 인식/구분 정보 누락
S3_KEY = f"airflow/{UPLOAD_FILE_NAME}"  # s3상 위치 조정

# 3. DAG
with DAG( 
  dag_id      = "09_aws_s3_consumer",
  description = "s3 특정 버킷내 특정 위치 감시, 감지된 이후 처리",
  default_args= {
    "owner"           : "aic-de1-admin",    
    "retries"         : 1,
    "retry_delay"     : timedelta(minutes=1)
  },
  schedule_interval = '@daily', #최소한의 스케줄 필요 -> 구동중이여야 작동 가능
  start_date  = pendulum.datetime( 2026,6,29, tz=pendulum.timezone("Asia/Seoul") ),
  catchup     = False,
  tags        = ['aws', 's3', 'consumer']
) as dag:
    
    # 4. task
    # 감시자, 센서
    task_wait_for_trigger = S3KeySensor(
        task_id = "wait_for_trigger",
        # 감시 대상 설정
        bucket_name = BUCKET_NAME,
        bucket_key = S3_KEY,        # 디렉토리 내 key(향후 키가 전달되어야 일반화)
        aws_conn_id = "aws_default", # 접속 정보
        # 감시 방법 -> 지속적(주기적 - 인터벌) 감시 -> 서비스 방식, 구성에 따라 설계 필요
        mode = "reschedule", # 감시 대기중 자원 반납
        poke_interval = 10, # 10초 간격으로 확인
        timeout = 60*10 # 10분 넘게 서비스 가동 후 감지가 안되면 종료
    )

    task_reading_data = PythonOperator(
        task_id = "reading_data",
        python_callable = _reading_data
    )

    task_delete_data = S3DeleteObjectsOperator( # 실제로는 백업 처리
        task_id = "delete_data"
    )
    # 5. 의존성
    task_wait_for_trigger >> task_reading_data >> task_delete_data