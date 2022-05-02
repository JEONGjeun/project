# from django.shortcuts import render
from flask import Flask, render_template, request
import servi

#Flask 객체 인스턴스 생성
app = Flask(__name__)


@app.route('/') # 접속하는 url
def index():
    print("1") 
    # GET 요청으로 들어오는 날짜 획득, 없을 수 있음
    selectDate = request.args.get("selectDate");
    list = servi.getlist(selectDate)
    print(list)

    # 화면에 돌려주는 list를 담고 반환
    # list는 빈칸도 가능하며, 빈 리스트는 html에서 감지하여 에러를 내지않게 함
    return render_template('index.html', dataList=list)

# @app.route('/')
# def dataLoading():
#     date = request.args.get({"selectDate"});
#     print(date) 
    
#     return render_template('index.html')