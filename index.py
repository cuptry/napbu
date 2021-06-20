import calcunapbu
import monthnapbu



a= input('월 달력 출력을 원하시면 1번, 오늘날짜만 알고싶으면 2번 입력 : ')

if(a==1):
    calcunapbu.startcalcunapbu()
else:
    monthnapbu.getmonthdate()