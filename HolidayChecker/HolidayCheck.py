# -*- coding: utf-8 -*-
import datetime
from datetime import date
from datetime import timedelta
from lunardate import LunarDate

# print (LunarDate.fromSolarDate(1976, 10, 1))
# print (LunarDate(2000, 1, 1).toSolarDate())
# print (LunarDate(2015, 1, 1).toSolarDate())
# print (LunarDate(1976, 8, 8).year)
# print (LunarDate(1976, 8, 8).month)
# print (LunarDate(1976, 8, 8).day)


class KR():
    # 대체휴일 로직 적용

    SOLAR_HOLIDAYS = (
    	(1, 1, "S_0101"),
        (3, 1, "S_0301"), #삼일절
        (5, 1, "S_0505"), #어린이 날
        (5, 5, "DS_0505"), #대체 공휴일 적용 : 어린이 날
        (6, 6, "S_0606"),
        (8, 15, "S_0815"),
        (10, 3, "S_1003"),
        (10, 9, "S_1009"),
        (12, 25, "S_1225")
    )

    LUNAR_HOLIDAYS = (
        (1, 1, "DL_0101"), #대체 공휴일 적용 : 설날
        (4, 8, "L_0408"),
        (8, 15, "DL_0815") #대체 공휴일 적용 : 추석
    )


if __name__ == "__main__":
	From_Year = 2015
	To_Year = 2016
	HOLIDAYS = []

	CurrentDateTime = datetime.date(From_Year, 1, 1)

	for Year in range(From_Year, To_Year):
		for LHDays in range (0, len(KR.LUNAR_HOLIDAYS)):
			# print (LunarDate(Year, KR.LUNAR_HOLIDAYS[LHDays][0], KR.LUNAR_HOLIDAYS[LHDays][1]).toSolarDate())
			CurrentDateTime = LunarDate(Year, KR.LUNAR_HOLIDAYS[LHDays][0], KR.LUNAR_HOLIDAYS[LHDays][1]).toSolarDate()
			NameOfDateTime = KR.LUNAR_HOLIDAYS[LHDays][2]
			# print (KR.LUNAR_HOLIDAYS[LHDays][2])

			HOLIDAYS.append ([CurrentDateTime, NameOfDateTime])

			if LHDays in (0,2):
				CurrentDateTime = LunarDate(Year, KR.LUNAR_HOLIDAYS[LHDays][0], KR.LUNAR_HOLIDAYS[LHDays][1]).toSolarDate() - datetime.timedelta(days = 1)
				HOLIDAYS.append ([CurrentDateTime, NameOfDateTime])
				CurrentDateTime = LunarDate(Year, KR.LUNAR_HOLIDAYS[LHDays][0], KR.LUNAR_HOLIDAYS[LHDays][1]).toSolarDate() - datetime.timedelta(days = -1)
				HOLIDAYS.append ([CurrentDateTime, NameOfDateTime])	

		# print (len(KR.SOLAR_HOLIDAYS)
		for SHDays in range (0, len(KR.SOLAR_HOLIDAYS)):
			CurrentDateTime = datetime.date(Year, KR.SOLAR_HOLIDAYS[SHDays][0], KR.SOLAR_HOLIDAYS[SHDays][1])
			NameOfDateTime = KR.SOLAR_HOLIDAYS[SHDays][2]

			HOLIDAYS.append ([CurrentDateTime, NameOfDateTime])

	# print (HOLIDAYS)
	HOLIDAYS.sort()
	# print ("-----------------------------------")
	# print (HOLIDAYS)
	# print (len(HOLIDAYS))
	# Check where the holidays are overlapped with Sunday

	for CheckHolidays in range(0, len(HOLIDAYS)):
		# print (HOLIDAYS[CheckHolidays][0].weekday())
		if HOLIDAYS[CheckHolidays][0].weekday() == 6 and HOLIDAYS[CheckHolidays][1][0] == "D":
			# print (str(HOLIDAYS[CheckHolidays][0]) + " Sunday!!")
			# print (str(HOLIDAYS[CheckHolidays + 1][0]) + " Sunday!!'s Next Day")
			
			DeltaCount = 1
			HOLIDAYS[CheckHolidays][0] = HOLIDAYS[CheckHolidays][0] + datetime.timedelta(days = 1)

			while str(HOLIDAYS[CheckHolidays][0]) == str(HOLIDAYS[CheckHolidays + DeltaCount][0]):

				# print (str(HOLIDAYS[CheckHolidays][0]))
				# print (str(HOLIDAYS[CheckHolidays + DeltaCount][0]))
				HOLIDAYS[CheckHolidays][0] = HOLIDAYS[CheckHolidays][0] + datetime.timedelta(days = 1)
				DeltaCount = DeltaCount + 1
				# print (str(HOLIDAYS[CheckHolidays][0]) + " is also a Holiday")
			else:
				# HOLIDAYS[CheckHolidays][0] = HOLIDAYS[CheckHolidays][0] + datetime.timedelta(days = 1)
				HOLIDAYS[CheckHolidays][1] = HOLIDAYS[CheckHolidays][1] + "_ReplacedDay"
				# print (str(HOLIDAYS[CheckHolidays][0]) + " is also a NEW Holiday")

	HOLIDAYS.sort()
	print (HOLIDAYS)
	print (len(HOLIDAYS))


	TestDate = datetime.date(2015, 8, 17)
	Holidays_TF = False

	Weekdays = ["Monday", "Tuesday", "Wednesday","Thursday","Friday", "Saturday", "Sunday"]
	print ( "This day is a " + Weekdays[TestDate.weekday()])

	if TestDate.weekday() in (5, 6):
		Holidays_TF = True

	for CheckHolidays in range(0, len(HOLIDAYS)):
		if str(TestDate) == str(HOLIDAYS[CheckHolidays][0]):
			Holidays_TF = True
	

	if Holidays_TF == False :
		print ("This day is not an Holiday.")
	else:
		print ("This day is a Holiday!!!")





