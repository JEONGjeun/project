from select import select
import pymysql
import sys

def getList(selectDate):
    print("3") 
    
    # 데이터베이스 연결
    try :
        conn = pymysql.connect(
            user = "root",
            password = "1004",
            host = "localhost",
            database ="airp",
            port = 3306,
            charset = "utf8"
        )
    except pymysql.Error as e :
        print(f"error connecting to mariadb platform {e}")
        sys.exit(1)
    # 데이터베이스 커서 획득
    cur = conn.cursor()

    
    print("4") 
    print(selectDate) 
    # SQL 실행 (특정 날짜를 선택하여 획득)
    cur.execute("SELECT * FROM airp_uv where sdt = %s", (selectDate, )) 
    # 실행 결과의 전체 리스트 담기
    data_list = cur.fetchall()
    print(data_list) 
    
    #cur.execute("SELECT * FROM airp_uv") 
    #print("5")          
    #data_list = cur.fetchall()
    #print("6") 
    #print(data_list) 

    return data_list