'''
- 기본 DAG 연습
- DAG 기본 형태가 갖춰지지 않으면 대시보드상에 등록되지 않음
- 필수 구성을 갖춘다면 잠시 후 대시보드 상에 등록이 됨

- 목표
    - bash Operator test, DAG 인식, DAG 작동 확인, DAG 기본 구성
    - 작동 확인
        - 시각적: 대시보드
        - 로그
    - 본 작성 파일은 xxx-worker 컨테이너에 /opt/airflow/dags/ 하위에 동기화
    - 실제는 xxx-worker 컨테이너에서 가동됨
        - 작성은 host pc
'''
# 1. 필요한 모듈, 패키지 가져오기
# DAG 클래스 
from airflow import DAG
# 오퍼레이터 2.x -> 3.x 에서는 패키지 경로가 변경됨
from airflow.operators.bash import BashOperator
# 스케줄 -> 시간
from datetime import datetime, timedelta


# 2-1. default_args, 편의성 바깥에서 정의, 향후 내부에서 정의
default_args = {
    "owner"             : "aic-de1-admin", # DAG 소유주
    "depends_on_past"   : False, # 과거 데이터(가동 시간 대비) 소급 처리 금지
    "retries"           : 1, # 작업 실패시 재시도 회수 1회 설정
    "retry_delay"      : timedelta(minutes= 5), # 재시도 5분 간격
    # 시나리오
    # 작업 성공 -> 완료
    # 작업 실패 -> 5분 대기 -> 1회 재시도 -> 성공 -> 완료
    # 작업 실패 -> 5분 대기 -> 1회 재시도 -> 실패 -> 실패
}

# 2. DAG 정의
with DAG (
    dag_id = "01_basics_bash", # DAG간 구분하는 용도
    description = "DE 업무중 Batch Pipeline 구성중 데이터 프로세싱 Ochestration 담당 airflow의 DAG 작성 기본형", # DAG 설명
    default_args = default_args, # 기본 인자값
    schedule_interval = "@daily", # 하루에 한번 00시00분00초, 문자열, cron 표현
    start_date = datetime(2026,6,29), # 현재기준 갭이 발생 -> 소급처리 x (위 설정 처리)
    catchup = False, # 과거에 대한 소급 처리 실행 방지
    tags = ["bash", "basic"]

) as dag:

# 3. Operator 정의
    t1 = BashOperator(
        task_id = "date-print",
        bash_command = "date"
    ) # task 정의됨
    t2 = BashOperator(
        task_id = "sleep",
        bash_command = "sleep 5"
    )
    t3 = BashOperator(
        task_id = "echo-print",
        bash_command = "echo 'hello'"
    )

# 4. 의존성 정의, 구동 순서 정의
# t1 실행 -> t2 실행 -> t3 실행
t1 >> t2 >> t3
pass