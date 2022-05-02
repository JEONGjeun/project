import db # db.py import
import datetime
#db 호출
def getlist(selectDate) :
    print("2") 
    print(selectDate)
    # 선택된 날짜가 있으면 그것을 datetime 형으로 변환
    # 선택된 날짜가 없으면 오늘 날짜를 datetime 형으로 변환
    # 형식은 yyyy-mm-dd 00:00:00
    if selectDate is not None :
        tsSelectDate = datetime.datetime.strptime(selectDate, '%Y-%m-%d')
    else :
        tsSelectDate = datetime.datetime.today().strftime('%Y-%m-%d')
    print(tsSelectDate)
    db_list = db.getList(tsSelectDate) # 메서드 호출에는 ()가 반드시 필요 ex)객체명.메서드명()
    print("7")     
    data_list = list()

    # db에서 추출한 데이터를 화면 표시용으로 가공
    for data in db_list:
        dt = str(data[3]) + ":00" #hh를 표현하는 방법
        obj = board(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        data_list.append(obj)
    print("30") 
    return data_list;


# 화면에 표시되는 정보 1줄의 정보를 담는 클래스
class board :
    def __init__(self, no, arp, congestYn, hh, pcg, pct, sdt, tof) :
        self.no = no
        self.arp = arp
        self.congestYn = congestYn
        self.hh = hh
        self.pcg = pcg
        self.pct = pct
        self.sdt = sdt
        self.tof = tof