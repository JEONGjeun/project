import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import configparser

df = pd.read_csv("./filename.csv", encoding='utf-8')

# params
user = 'taka',
password = '1004',
host = '127.0.0.1',
port = '3306',
database ='vist'

# 실행 시작 시간
start_time = time.time()

# DB 접속 엔진 객체 생성
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', encoding='utf-8')

# DB 테이블 명
table_name = "vistp"

# DB에 DataFrame 적재
df.to_sql(index = False,
          name = table_name,
          con = engine,
          if_exists = 'append',
          method = 'multi', 
          chunksize = 10000)

# 실행 종료 시간
cost_time_sec = time.time() - start_time
cost_time_min = cost_time_sec / 60
cost_time_hour = cost_time_min / 60

print(f">> 소요시간: {cost_time_sec:,.1f}초 = {cost_time_min:,.1f}분 = {cost_time_hour:,.1f}시간")
