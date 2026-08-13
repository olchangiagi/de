'''
DAG -> DAG 작동 시키는 트리거 오퍼레이터 사용
'''

# 1. 모듈
from airflow import DAG
from airflow.operators.python import PythonOperator
# 핵심 클레스
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
import logging
import pendulum
import json
import random
import pandas as pd
import os

# 2. 전역 변수
KST = pendulum.timezone("Asia/Seoul")

DATA_PATH = "/opt/airflow/dags/data"
os.makedirs(DATA_PATH, exist_ok=True)

def _extract(**kwargs):
  data = [
    {
      "sensor_id"   : f"SENSOR_{i+1}",      
      "timestamp"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
      "temperature" : round( random.uniform(20.0, 150.0), 2),      
      "status"      : "on"                 
    }
    for i in range(10)
  ]
  file_full_path = f"{DATA_PATH}/sensor_data_{kwargs['ds_nodash']}.json"
  with open(file_full_path, 'w') as f:
    json.dump( data, f )
  
  logging.info( f'extract 한 데이터 {data}'  )
  logging.info( f'extract 한 데이터 파일 경로 {file_full_path}'  )
  return file_full_path

# 3. DAG
with DAG( 
  dag_id      = "06_multi_dag_1_extract",
  description = "extract 전용 DAG",
  default_args= {
    "owner"           : "aic-de1-admin",    
    "retries"         : 1,
    "retry_delay"     : timedelta(minutes=1)
  },
  schedule_interval = "@daily",
  start_date  = pendulum.datetime( 2026,6,29, tz=KST ),
  catchup     = False,
  tags        = ['etl', 'extract']
) as dag:

# 4. Operator
  task_extract      = PythonOperator(
      task_id         = "extract",
      python_callable = _extract
    )
  # 신규 추가 부분
  task_trigger_transform_dag_run = TriggerDagRunOperator(

  )

  #5. 의존성
  task_extract >> task_trigger_transform_dag_run