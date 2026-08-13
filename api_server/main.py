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
app = FastAPI()

# 3. 요청/응답 구조 정의 -> class
class ReqData(BaseModel):
    # column 나열
    user_id:str
    income:int
    loan_amt:int

class ResData(BaseModel):
    # column 나열
    user_id:str # 사용자 id
    credit_score:int # 0점~1000점
    grade:str # A급, B급, ...

# 4. 라우팅: url, 처리함수 매핑
@app.get("/")
def home():
    return{"status":"AI 신용평가 서비스 API"}

@app.post("/predict", response_model=List[ResData]) # 응답 구조 정의
def predict(users:List[ReqData]): # 요청 구조 정의
    # 고객 1명씩 신용평가 -> 응답 구조 작성 -> 응답
    result = list()
    for user in users: # 고객 1명씩 추출
        '''
            가상 공식
            사전 반영식 = (소득//1000) * 10
            credit_score = min(난수 (300, 600) = 사전반영식, 990)
            grade = credit_score가 800 이상이면 A, 600 이상이면 B, 나머지 C
        '''
        # 고객 1명 평가
        사전반영식 = (user.income//1000) * 10
        credit_score = min(random.randint(300, 600) + 사전반영식, 990)
        grade = "A" if credit_score >= 800 else "B" if credit_score >= 600 else "C"
        # 평가한 고객 정보 담기
        result.append({
            "user_id": user.user_id,
            "credit_score": credit_score,
            "grade": grade
        })
        pass

    # 응답
    return result
