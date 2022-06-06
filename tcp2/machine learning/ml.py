import pandas as pd
from sklearn import linear_model as lm
import sklearn.model_selection
from matplotlib import pyplot as plt
import numpy as np
import pymysql

# 아니면 DB에서 직접 뽑아오는 방법도 존재함. 아래의 SQL을 사용
conn = pymysql.connect(
    user = 'taka',
    password = '1004',
    host = '127.0.0.1',
    database ='vist',
    charset = 'utf8'
)

sql = "SELECT str_to_date(concat(date_format(`vistp`.`check_date`,'%Y-%m'),'-01'),'%Y-%m-%d')AS `check_date`,sum(`vistp`.`booking`)AS `sum`, sum(`vistp`.`nb_visit`)AS `sum_2`, sum(`vistp`.`nb_visit`)AS `sum_3`,  sum(`vistp`.`totvisit`) AS sum_4 FROM vistp GROUP BY str_to_date(concat(date_format(`vistp`.`check_date`,'%Y-%m'),'-01'),'%Y-%m-%d')ORDER BY str_to_date(concat(date_format(`vistp`.`check_date`,'%Y-%m'),'-01'),'%Y-%m-%d')ASC"

with conn:
    with conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
        for data in result:
            print(data)
        
        df = pd.DataFrame.from_records(result)

# 인덱스 지정 check_date 를 유니크 값으로 간주 가능
# 결측치는 존재하지 않으므로 처리 할 필요가 없음.
# 일일 데이터의 휴관일 등으로 인한 관람객 0명은 월 합계에서 무시되는 값이기 때문.

# 필요한 데이터만 정제해봄

df = df.drop(df.columns[[1,2,3]], axis=1)

# 총 입장객 수를 가지고, 2018년 1월의 입장객 예측 데이터를 뽑아보려고 함
# 총 입장객 수의 칼럼명 변경

df.columns = ['check_date', 'tot']
print(df.head())

year_months = list(df['check_date'].unique())
pred_data = pd.DataFrame()

# 2017년 7월부터 뽑아야하므로 인덱스번호 6부터
for i in range(6, len(year_months)):
    # 해당 월 하나씩 뽑아서 임시 데이터 프레임에 저장
    tmp = df.copy()
    tmp = tmp.loc[df['check_date'] == year_months[i]]
    # tmp의 tot를 tot_pred로 변경 (예측하고자 하는 정답 데이터)
    tmp.rename(columns={'tot': 'tot_pred'}, inplace=True)
    # 데이터 병합을 위해, 현재 데이터 수집 중인 연월을 저장
    nowDate = year_months[i]

    # 그리고 tmp 하나의 달에 대응하는 이전 6개월 분의 데이터를 만듦
    for j in range(1,7):
        tmp_before = df.copy()
        tmp_before = tmp_before.loc[df['check_date'] == year_months[i-j]]

        # 과거 6개월의 데이터를 채우기 때문에 tot0부터 6까지의 열이 만들어짐
        tmp_before.rename(columns={'tot': 'tot_{}'.format(j-1)}, inplace=True)
        tmp_before.loc[i-j, 'check_date'] = nowDate

        # 그리고 tmp와 tmp_before를 결합
        tmp = pd.merge(tmp, tmp_before, on='check_date', how='left')

    # 결합 후, 비어있는 pred_data에 tmp를 하나하나 결합시킴
    pred_data = pd.concat([pred_data, tmp], ignore_index=True)

print(pred_data)


model = lm.LinearRegression()

# 학습 할 독립 변수
X = pred_data[['tot_0', 'tot_1', 'tot_2', 'tot_3', 'tot_4', 'tot_5']]
# 학습 할 종속 변수
y = pred_data['tot_pred']

# 학습 시키기
# 먼저 train과 test set을 나눔
# 디폴트로는 train:test를 75:25로 분할
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y)
model.fit(X_train, y_train)

# 검증?
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 그래프 그리기

x = np.arange('2017-07', '2018-01', dtype='datetime64[M]')
yy = y.values.tolist()

plt.plot(x, yy)
plt.show()