'''
- 평가를 해야하는 고객 데이터 구조 (요청/응답)
    - [ {}, {}, ...]
'''

# 1. 모듈 가져오기
from fastapi import FastAPI     # app
from pydantic import BaseModel  # 요청/응답 클래스 구성시 슈퍼클래스 역할
from typing import List         # 요청/응답 데이터 구성시 구조 정의시 사용
import random                   # 신용 평가 시 활용

# 2. FastAPI 객체 생성

# 3. 요청/응답 구조 정의 -> class

# 4. 라우팅: url, 처리함수 매핑