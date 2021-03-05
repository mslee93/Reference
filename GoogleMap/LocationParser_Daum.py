import urllib
import urllib.parse
import urllib.request
import simplejson
import json

import codecs

import xlrd
import xlsxwriter

apikey = '6f87e62f15effb599f33dd9b507f49fa'
# DaumUrl = 'https://apis.daum.net/local/geo/addr2coord?'

def decode_address_to_coordinates(address):
        params = ({
                'apikey' : apikey,
                'q' : address,
                'output' : 'json'
        })

        url = 'https://apis.daum.net/local/geo/addr2coord?' + urllib.parse.urlencode(params)
        print("URL : " + url)

        response = urllib.request.urlopen(url)


        print("Response : " + str(response))

        reader = codecs.getreader("utf-8")

        result = json.load(reader(response))

        try:
                lat = str(result['channel']['item'][0]['point_x'])
                lng = str(result['channel']['item'][0]['point_y'])
                Title = str(result['channel']['item'][0]['title'])
                City = str(result['channel']['item'][0]['localName_1'])
                Gu = str(result['channel']['item'][0]['localName_2'])    
                Dong = str(result['channel']['item'][0]['localName_3'])

                # print (lat + ", " + lng +", " + City +" " +Gu +" " + Dong)
                print (lat + ", " + lng)
                return (lat, lng, Title, City, Gu, Dong)


        except:
                print ('Address Decode Except')
                return exception

if __name__ == "__main__":
    file_location = "C:\\temp\\CreditCardDataSample_temp.xls"
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)

    workbook = xlsxwriter.Workbook('C:\\temp\\GPSLoc.xlsx')
    worksheet = workbook.add_worksheet()

    for i in range(1,1000):
        address = sheet.cell_value(i,0)

        print ('Current Count : ' + str(i))

        try:
            lat, lng, Title, City, Gu, Dong = decode_address_to_coordinates (address)
            worksheet.write_string(i, 0, lat)
            worksheet.write_string(i, 1, lng)
            worksheet.write_string(i, 2, Title)
            worksheet.write_string(i, 3, City)
            worksheet.write_string(i, 4, Gu)
            worksheet.write_string(i, 5, Dong)

        except:
            worksheet.write_string(i, 0, 'LocationError')
            print ("Main Func Excpetion")


    workbook.close()


