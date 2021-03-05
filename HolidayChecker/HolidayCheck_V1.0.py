# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
from lunardate import LunarDate


class KR():

    SOLAR_HOLIDAYS = (
    	(1, 1, "신정", False),
        (3, 1, "삼일절", False),
        (5, 1, "노동절", False),
        (5, 5, "어린이날", True), #대체 공휴일 적용
        (6, 6, "현충일", False),
        (8, 15, "광복절", False),
        (10, 3, "개천절", False),
        (10, 9, "한글날", False),
        (12, 25, "크리스마스", False)
    )

    LUNAR_HOLIDAYS = (
        (1, 1, "구정", True), #대체 공휴일 적용 : 설날
        (4, 8, "석가탄신일", False),
        (8, 15, "추석", True) #대체 공휴일 적용 : 추석
    )

def ListHOLIDAYS (From_Year, To_Year):
	HOLIDAYS = []

	CurrentDateTime = datetime.date(From_Year, 1, 1)

	for Year in range(From_Year, To_Year):
		for LHDays in range (0, len(KR.LUNAR_HOLIDAYS)):
			CurrentDateTime = LunarDate(Year, KR.LUNAR_HOLIDAYS[LHDays][0], KR.LUNAR_HOLIDAYS[LHDays][1]).toSolarDate()
			NameOfDateTime = KR.LUNAR_HOLIDAYS[LHDays][2]
			ReplacedHoliday = KR.LUNAR_HOLIDAYS[LHDays][3]

			HOLIDAYS.append ([CurrentDateTime, NameOfDateTime, ReplacedHoliday])

			if LHDays in (0,2):
				CurrentDateTime = LunarDate(Year, KR.LUNAR_HOLIDAYS[LHDays][0], KR.LUNAR_HOLIDAYS[LHDays][1]).toSolarDate() - datetime.timedelta(days = 1)
				HOLIDAYS.append ([CurrentDateTime, NameOfDateTime, ReplacedHoliday])
				CurrentDateTime = LunarDate(Year, KR.LUNAR_HOLIDAYS[LHDays][0], KR.LUNAR_HOLIDAYS[LHDays][1]).toSolarDate() - datetime.timedelta(days = -1)
				HOLIDAYS.append ([CurrentDateTime, NameOfDateTime, ReplacedHoliday])	


		for SHDays in range (0, len(KR.SOLAR_HOLIDAYS)):
			CurrentDateTime = datetime.date(Year, KR.SOLAR_HOLIDAYS[SHDays][0], KR.SOLAR_HOLIDAYS[SHDays][1])
			NameOfDateTime = KR.SOLAR_HOLIDAYS[SHDays][2]

			HOLIDAYS.append ([CurrentDateTime, NameOfDateTime, ReplacedHoliday])


	HOLIDAYS.sort()
	print (HOLIDAYS)

	for CheckHolidays in range(0, len(HOLIDAYS)):
		if HOLIDAYS[CheckHolidays][0].weekday() == 6 and HOLIDAYS[CheckHolidays][2] == True:
			DeltaCount = 1
			HOLIDAYS[CheckHolidays][0] = HOLIDAYS[CheckHolidays][0] + datetime.timedelta(days = 1)

			while str(HOLIDAYS[CheckHolidays][0]) == str(HOLIDAYS[CheckHolidays + DeltaCount][0]):
				HOLIDAYS[CheckHolidays][0] = HOLIDAYS[CheckHolidays][0] + datetime.timedelta(days = 1)
				DeltaCount = DeltaCount + 1
			else:
				HOLIDAYS[CheckHolidays][1] = HOLIDAYS[CheckHolidays][1] + "_대체공휴일"

	HOLIDAYS.sort()
	return HOLIDAYS


def isHOLIDAY (HOLIDAYS, TestDate):
	Holidays_TF = False
	NameOfDay = ""
	Weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	# print ( str(TestDate) + " is a " + Weekdays[TestDate.weekday()])

	DayOfTheWeek = Weekdays[TestDate.weekday()]

	if TestDate.weekday() in (5, 6):
		Holidays_TF = True

	for CheckHolidays in range(0, len(HOLIDAYS)):
		if str(TestDate) == str(HOLIDAYS[CheckHolidays][0]):
			Holidays_TF = True
			NameOfDay = HOLIDAYS[CheckHolidays][1]

	return DayOfTheWeek, Holidays_TF, NameOfDay

###########################################################################################################

if __name__ == "__main__":
	From_Year = 2015
	To_Year = 2016
	Holidays_TF = False

	HOLIDAYS = ListHOLIDAYS (From_Year, To_Year)

	# print (HOLIDAYS)
	# print ("-----------------------------------------------------------------------------------")

	TestDate = datetime.date(2015, 5, 1)
	DayOfTheWeek, Holidays_TF, NameOfDay = isHOLIDAY (HOLIDAYS, TestDate)
	
	print (DayOfTheWeek)
	print (Holidays_TF)

	if Holidays_TF == False :
		print ("This day is not an Holiday.")
	else:
		print ("This day is a Holiday!!!")
		print ("이 날은 공휴일 입니다.")
		print (NameOfDay)





