variable "aws_region" {
  description = "AWS 리전"
  type        = string
  default     = "ap-northeast-2"
}

variable "project_name" {
  description = "데이터 엔지니어 프로젝트 연습용"
  type        = string
  default     = "de-ai-08-loggen"
}

variable "environment" {
  description = "환경 구분"
  type        = string
  default     = "dev"
}

# s3 버킷을 삭제할 때 버킷 내부에 객체가 있을 경우 삭제 허용, 불가 처리
variable "s3_force_destroy" {
  description = "True면 버킷 내부 데이터를 모두 삭제하고 버킷까지 삭제"
  type        = bool
  default     = false
}

# s3.tf가 없다면 -> 기존에 존재하는 버킷을 사용하여 처리하는 방식
variable "silver_bucket_name" {
  description = "기존 silver parquet 데이터가 실제 저장하고 있는 s3 bucket 입력 이름"
  type        = string
  # default 생략 -> apply시 사용자에게 질문(입력 대기, 사용자와 인터렉션 가능)
}