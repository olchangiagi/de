'''
- airflow 내부 정보 접근, 출력시 jinja 활용, 내부 정보 접근시 macro 활용
- 콜백함수 내부는 kwargs를 인자를 통해 접근, 기타 일반적인 상황은 jinja를 이용하여 접근
'''

# 1. 모듈
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import logging
import pendulum

# 1-1. 전역변수
KST = pendulum.timezone("Asia/Seoul")

# 1-2. 콜백 함수
def _print(**kwargs):
    logging.info(f"ds 출력 {kwargs["ds"]}")
    pass

# 2. DAG
with DAG (
    dag_id = "03_basics_context_jinja", 
    description = "macro를 이용하여 context 접근, jinja를 통해 표현", 
    default_args = {
    "owner"             : "aic-de1-admin",
    "retries"           : 1, 
    "retry_delay"       : timedelta(minutes= 1), 
    },
    # 매일 오전 9시 00분에 스케줄 작동
    schedule_interval = "0 9 * * *", # cron 표기 (분, 시, 일, 월, 주)
    # 수행 시작 시간 서울 시간대 타임존 조정
    start_date = pendulum.datetime(2026,6,29, tz = KST), 
    catchup = False, 
    tags = ["macro", "context", "jinja"]

) as dag:

# 3. 오퍼레이터를 이용하여 task를 정의
    t1 = BashOperator(
        task_id = "jinja_used_task",
        bash_command = "echo 'DAG의 t1 task 수행시간 {{ds}}, {{ti}}"
    )
    t2 = BashOperator(
        task_id = "jinja_macro_task",
        # macro를 통해 준비된 함수 활용
        bash_command = "echo 'DAG의 t1 task 일주일전 수행시간(임시) {{macro.ds_add(ds - 7)}}, {{macro.random()}}"
    )
    t3 = PythonOperator(
        task_id = "jinja_python_task",
        python_callable = _print
    )

# 4. 의존성(수행순서)
t1 >> t2 >> t3