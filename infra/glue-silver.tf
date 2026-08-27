resource "aws_glue_catalog_database" "silver" {
  name = "${lower(replace(var.project_name, "-", "_"))}_silver_glue_db"
  description = "Silver parquet 데이터를 athena/airflow에서 조회하기 위한 Glue DB"
  # 향후 실습을 위해 실수 삭제 방지
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_glue_catalog_table" "silver" {
  name = "silver_logs_tbl"
  database_name = aws_glue_catalog_database.silver.name
  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL = "TRUE"
    "parquet.compression" = "SNAPPY"
    "projection.enabled" = "true"
    "projection.year.type"  = "integer"
    "projection.year.range" = "2026,2040" 

    "projection.month.type"   = "integer"
    "projection.month.range"  = "1,12"
    "projection.month.digits" = "2" 

    "projection.day.type"   = "integer"
    "projection.day.range"  = "1,31"
    "projection.day.digits" = "2" 

    "projection.hour.type"   = "integer"
    "projection.hour.range"  = "0,23"
    "projection.hour.digits" = "2"

    "storage.location.template" = "s3://${aws_s3_bucket.data.bucket}/silver/year=$${year}/month=$${month}/day=$${day}/hour=$${hour}"
  }

  storage_descriptor {
    location = "s3://${aws_s3_bucket.data.bucket}/silver/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    compressed = true

    ser_de_info {
      name = "silver-parquet"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    columns {
      name = "schema_version"
      type = "string"
    }
    columns {
      name = "record_type"
      type = "string"
    }
    columns {
      name = "event_id"
      type = "string"
    }
    columns {
      name = "trace_id"
      type = "string"
    }
    columns {
      name = "run_id"
      type = "string"
    }
    columns {
      name = "occurred_at"
      type = "string"
    }
    columns {
      name = "generated_at_utc"
      type = "string"
    }
    columns {
      name = "domain"
      type = "string"
    }
    columns {
      name = "event_type"
      type = "string"
    }

    columns {
      name = "service"
      type = "struct<name:string,environment:string,instance_id:string>"
    }

    columns {
      name = "client"
      type = "struct<ip:string,user_agent:string,device_id:string>"
    }

    columns {
      name = "request"
      type = "struct<method:string,path:string,request_bytes:bigint>"
    }

    columns {
      name = "response"
      type = "struct<status_code:int,latency_ms:bigint,response_bytes:bigint>"
    }

    # 모든 도메인의 데이터를 받을 수 있또록 슈퍼셋 구성
    # data 중첩 스키마 -> 도메인별로 상이 -> 모든 도메인의 키를 등록
    columns {
      name = "data"
      type = "struct<user_id:string,session_id:string,product_id:string,category:string,quantity:bigint,unit_price:bigint,currency:string,campaign:string,keyword:string,result_count:bigint,order_id:string,total_amount:bigint,payment_method:string,payment_result:string,transaction_id:string,customer_id:string,account_id:string,channel:string,risk_score:double,amount:bigint,merchant_id:string,merchant_category:string,authorization_result:string,destination_bank:string,destination_account_token:string,transfer_result:string,balance:bigint,auth_method:string,login_result:string,player_id:string,server_region:string,player_level:bigint,ping_ms:bigint,platform:string,match_id:string,mode:string,party_size:bigint,result:string,score:bigint,duration_seconds:bigint,item_id:string,currency_type:string,purchase_result:string,quest_id:string,reward_xp:bigint,reward_gold:bigint,plant_id:string,line_id:string,equipment_id:string,equipment_type:string,message_id:string,temperature_c:double,vibration_mm_s:double,pressure_bar:double,rpm:bigint,state:string,runtime_seconds:bigint,lot_id:string,sample_size:bigint,defect_count:bigint,quality_result:string,alarm_code:string,severity:string,acknowledged:boolean,maintenance_type:string,technician_id:string,downtime_minutes:bigint>"
    }

    columns {
      name = "_silver"
      type = "struct<layer:string,processor:string,schema_version:string,processed_at:string>"
    }

  }

  partition_keys {
    name = "year"
    type = "string"
  }
  partition_keys {
    name = "month"
    type = "string"
  }
  partition_keys {
    name = "day"
    type = "string"
  }
  partition_keys {
    name = "hour"
    type = "string"
  }
}