import pandas as pd
import datetime
import calendar # 월 첫날과 마지막날 구하는 import
import calcunapbu
import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import calcunapbu
import numpy as np
import openpyxl
import os

holidays = [] # 휴일 담을 리스트 생성   
result = pd.DataFrame(np.empty((0, 4)))

def dweekend(ddate, dholidays): # 기준 날짜, 휴일날짜 받고 실행
    ff=[]
    for i in dholidays:
        a = datetime.datetime.strptime(i, "%Y%m%d")
        ff.append(a)


        
    while(True): #주말 여부를 위한 무한 반복문, 위 계산된 ddate가 기준
            if(ddate.weekday() == 5 or ddate.weekday() == 6 or (ddate in ff) == True): # 5 = 토요일, 6 = 일요일, #휴일같이
                ddate = ddate + relativedelta(days=1)                                 
            else: # 주말이 아니면 반복문 탈출 
                break    
    return ddate


def firstdate(detecteddate10, holidays10): # 1차 납부기한 함수 
    firstdate10 = detecteddate10 + relativedelta(days=10) #날짜 10일 더하기
    finalfirstdate10 = dweekend(firstdate10, holidays10) #dweekend 함수 호출 // 기준 날짜, 휴일 정보 반환
    return finalfirstdate10 # 1차납부기한 반환

def seconddate(detecteddate20, holidays20): # 2차 납부기한 함수 
    seconddate20 = detecteddate20 + relativedelta(days=20) #날짜 20일 더하기
    finalseconddate20 = dweekend(seconddate20, holidays20) #dweekend 함수 호출 // 1차납부기한 날짜, 휴일 정보 반환
    return finalseconddate20 # 2차납부기한 반환

def gwadate(detecteddate15, holidays15): # 과태료 함수 
    firstdate15 = detecteddate15 + relativedelta(days=15) #날짜 15일 더하기
    finalgwadate15 = dweekend(firstdate15, holidays15) #dweekend 함수 호출 // 기준 날짜, 휴일 정보 반환
    return finalgwadate15 # 과태료 기한 반환




def getdatesholidays(gdates, gholidays): # 기준 날짜 및 휴일 정보들 받아서 함수 실행
    first = firstdate(gdates, gholidays) # 1차 납부기한 함수 호출, 기준 날짜, 휴일날짜 인계
    second = seconddate(first, gholidays) # 2차 납부기한 함수 호출, 1차 납부날짜, 휴일날짜 인계
    gwa = gwadate(gdates, gholidays) # 과태료 함수 호출, 기준 날짜, 휴일날짜 인계
    #print('기준 날짜 : ', gdates.strftime('%Y-%m-%d'), '\n' + '1차 납부기한', first.strftime('%Y-%m-%d'), '\n' + '2차 납부기한', second.strftime('%Y-%m-%d'), '\n' + '과태료', gwa.strftime('%Y-%m-%d'), '\n' )

    
    tt = pd.DataFrame({'기준날짜' : gdates.strftime('%Y-%m-%d'), '1차납부' : first.strftime('%Y-%m-%d'), '2차납부' : second.strftime('%Y-%m-%d'),  '과태료' : gwa.strftime('%Y-%m-%d')}, index = [1])
    return tt
    
    
    






def calcunapbustart(now):
    starturi = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/' # API 주소
    servicekey = 'getRestDeInfo?serviceKey=BLlX7Aed74ufW62zmZUpoAfjTs1nPJlgjYy30PwpXp2Nuvwx2u56ODNCtaApZVE%2BkWypsUIQn91cyJ3D1F08FQ%3D%3D&' # API 서비스키


    date = [] # API로 호출한 item 태그 담을 리스트 생성

    for i in range(3): # 기준점으로 3개월치 휴일을 담기위한 반복 실행
        ctlmonth = relativedelta(months=0) # ctlmonth 월 더해줄 변수 생성 i로 추가 될예정
        if i>0: # i가 0보다 클때 실행, 3번 실행 i값 0,1,2
            ctlmonth = relativedelta(months=i) # ctlmonth에 더할 만큼의 월 초기화
            ctldate = now + ctlmonth   #기준 시간에 월 더하기
            year = ctldate.strftime("%Y") # year변수에 연도를 2021형식으로 변환하여 문자열 저장 
            month = ctldate.strftime("%m") # month변수에 연도를 2021형식으로 변환하여 문자열 저장    
            uri = starturi + servicekey + 'solYear=' + year + '&'+ 'solMonth=' + month # uri에 API에 호출할 주소 생성
            response = requests.get(uri) # uri로 특일 API 호출하여 response에 저장
            soup = BeautifulSoup(response.content, 'html.parser') # soup변수에 BeautifulSoup를 이용하여 받은 데이터 html화 시켜 저장
            date = date + soup.find_all('item') # date변수에 BeautifulSoup를 이용하여 휴일정보가 있는 item태그를 저장
        else:
            ctldate = now + ctlmonth   #기준 시간에 월 더하기
            year = ctldate.strftime("%Y") # year변수에 연도를 2021형식으로 변환하여 문자열 저장 
            month = ctldate.strftime("%m") # month변수에 연도를 2021형식으로 변환하여 문자열 저장    
            uri = starturi + servicekey + 'solYear=' + year + '&'+ 'solMonth=' + month # uri에 API에 호출할 주소 생성
            response = requests.get(uri) # uri로 특일 API 호출하여 response에 저장
            soup = BeautifulSoup(response.content, 'html.parser') # soup변수에 BeautifulSoup를 이용하여 받은 데이터 html화 시켜 저장
            date = date + soup.find_all('item') # date변수에 BeautifulSoup를 이용하여 휴일정보가 있는 item태그를 저장
            
            

    for item in date: # 리스트에 휴일 담기 위하여 반복
        datename = item.find('datename') # datename변수에 휴일의 이름 저장
        isholiday = item.find('isholiday') # isholiday변수에 휴일 유무 저장
        locdate = item.find('locdate') # locdate 변수에 휴일의 날짜 저장
        holidays.append(locdate.get_text()) # holidays 리스트에 휴일 날짜 텍스트화 시켜서 추가 기존은 HTML
        



print('월(月) 총 납부기간 출력')
standardMonthDate = input('원하는 월(月)를 연도(年)와 입력해주세요 : ')


monthdate = datetime.datetime.strptime(standardMonthDate, "%Y%m") # 입력받은 날짜를 datetime으로 변환

monthFirstDay = 1
monthLastDay = calendar.monthrange(monthdate.year, monthdate.month)[1]

calcunapbustart(monthdate)
2

facto = pd.DataFrame()
for i in range(monthFirstDay, monthLastDay+1):
    if(i == 15):
        facto= facto.append(pd.DataFrame({'기준날짜' : '기준날짜', '1차납부' : '1차납부', '2차납부' : '2차납부',  '과태료' : '과태료'}, index = [1]))
    facto = facto.append(getdatesholidays(datetime.datetime(monthdate.year, monthdate.month, i), holidays))
    
    

facto.to_excel('{0}\{1}년 {2}월 납부기간.xlsx'.format(os.path.join(os.path.expanduser('~'),'Desktop'), monthdate.year, monthdate.month), sheet_name='new_name', index=False)
print('{0}년 {1}월 납부기한 엑셀 파일 출력 완료!'.format(monthdate.year,monthdate.month))


