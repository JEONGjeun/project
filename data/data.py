# 모듈 import
from lib2to3.pgen2.pgen import DFAState
import requests
import pprint
from os import name
import xml.etree.ElementTree as et
import pandas as pd
from pandas import Series, DataFrame
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote

#인증키 입력
encoding = 'TKEzopLWWMJ0hEFGtXooFm%2BezPURFhz9cPKbTCq%2Bzty%2Fr6RJzsJM5Wc%2B9aLgUBPHuaOJaPowbWFZ46pBeLghdQ%3D%3D'
decoding = 'TKEzopLWWMJ0hEFGtXooFm+ezPURFhz9cPKbTCq+zty/r6RJzsJM5Wc+9aLgUBPHuaOJaPowbWFZ46pBeLghdQ=='

#url 입력
url = 'http://openapi.airport.co.kr/service/rest/dailyExpectPassenger/dailyExpectPassenger'
# params ={'serviceKey' : decoding , 'pageNo' : '1', 'numOfRows' : '4999', 'startCreateDt' : '2010', 'endCreateDt' : '2022' }
params ={'serviceKey' : decoding , 'pageNo' : '1', 'numOfRows' : '5000', 'startCreateDt' : '2010',
 'endCreateDt' : '2022', 'schAirport' : 'PUS' }
response = requests.get(url, params=params)

# xml 내용
content = response.text

# 깔끔한 출력 위한 코드
pp = pprint.PrettyPrinter(indent=4)
#print(pp.pprint(content))


#bs4 사용하여 item 태그 분리

xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
rows = xml_obj.findAll('item')
print(rows)
"""
# 컬럼 값 조회용
columns = rows[0].find_all()
print(columns)
"""

# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]

#xml값 DataFrame으로 만들기
airpu_df = pd.DataFrame(row_list, columns=name_list)
df = pd.DataFrame(airpu_df)
#aod 목록 삭제(어떤 내용인지 몰라 알수 없으므로 결측데이터로 파악하고 삭제.)
airpu_df = df.drop('aod',axis=1)
print(airpu_df.head(19)) 


# #DataFrame CSV 파일로 저장
airpu_df.to_csv('airp_user.csv', encoding='UTF-8')