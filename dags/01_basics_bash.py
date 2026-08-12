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
# 2. DAG 정의
# 3. Operator 정의
# 4. 의존성 정의, 구동 순서 정의