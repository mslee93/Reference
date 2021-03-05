# -*- coding:utf-8 -*-

import urllib
import urllib.parse
import urllib.request
import simplejson
import json

import codecs

import xlrd
import xlsxwriter

daum_apikey = '6f87e62f15effb599f33dd9b507f49fa'
google_apikey = 'AIzaSyDGLfvSZTZPgNn4hMFLqHBoVUpGi0W7o64'
# DaumUrl = 'https://apis.daum.net/local/geo/addr2coord?'

def d_decode_address_to_coordinates(address):
        params = ({
                'apikey' : daum_apikey,
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
                lat = str(result['channel']['item'][0]['point_y'])
                lng = str(result['channel']['item'][0]['point_x'])
                Title = str(result['channel']['item'][0]['title'])
                City = str(result['channel']['item'][0]['localName_1'])
                Gu = str(result['channel']['item'][0]['localName_2'])    
                Dong = str(result['channel']['item'][0]['localName_3'])

                # print (lat + ", " + lng +", " + City +" " +Gu +" " + Dong)
                print (lat + ", " + lng)
                return (lat, lng, Title, City, Gu, Dong)


        except:
                print ('Daum Address Decode Except')
                return exception

def g_decode_address_to_coordinates(address):
        params = {
                'key' : google_apikey,
                'address' : address,
                'sensor' : 'false',
        }  
        url = 'https://maps.google.co.kr/maps/api/geocode/json?' + urllib.parse.urlencode(params)
        response = urllib.request.urlopen(url)
        print("URL : " + url)

        print("Response : " + str(response))

        reader = codecs.getreader("utf-8")

        result = json.load(reader(response))

        try:
                lat = str(result['results'][0]['geometry']['location']['lat'])
                lng = str(result['results'][0]['geometry']['location']['lng'])

                Title = str(result['results'][0]['formatted_address'])
                # City = str(result['results'][0]['address_components'][2][shortname])
                # Gu = str(result['results'][0]['address_components'][3][shortname])    
                # Dong = str(result['results'][0]['address_componentsy'][4][shortname])
                print (lat + ", " + lng)
                # return (lat, lng, Title, City, Gu, Dong)
                return (lat, lng, Title)
        except:
                print ('Google Address Decode Except')
                return exception

def d_decode_coordinates_to_address(cod_x, cod_y):
        params = ({
                'apikey' : daum_apikey,
                'latitude' : cod_x,
                'longitude' : cod_y,
                'output' : 'json'
        })

        url = 'https://apis.daum.net/local/geo/coord2addr?' + urllib.parse.urlencode(params)
        print("URL : " + url)

        response = urllib.request.urlopen(url)


        print("Response : " + str(response))
        reader = codecs.getreader("utf-8")
        result = json.load(reader(response))

        try:
            City = str(result['name1'])
            Gu = str(result['name2'])    
            Dong = str(result['name3'])


            print (City + Gu + Dong)
            return (City, Gu, Dong)

        except:
            print ('Daum Cordination Decode Except')
            return exception


if __name__ == "__main__":
    file_location = "C:\\temp\\CreditCardDataSample.xls"
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)

    workbook = xlsxwriter.Workbook('C:\\temp\\GPSLoc.xlsx')
    worksheet = workbook.add_worksheet()

    for i in range(1,100):
        # Address Field Confirm #################################################################
        address = sheet.cell_value(i,23)

        print ('Current Count : ' + str(i))

        try:
            lat, lng, Title, City, Gu, Dong = d_decode_address_to_coordinates (address)
            worksheet.write_string(i, 0, lat)
            worksheet.write_string(i, 1, lng)
            worksheet.write_string(i, 2, Title)
            worksheet.write_string(i, 3, City)
            worksheet.write_string(i, 4, Gu)
            worksheet.write_string(i, 5, Dong)
            worksheet.write_string(i, 6, "DAUM")
        except:
            try:
                print ("Exception Error Try with GOOGLE !!!!!!!!!!!!!!!!!!!!!!!!!")
                # lat, lng, Title, City, Gu, Dong = g_decode_address_to_coordinates (address)
                lat, lng, Title = g_decode_address_to_coordinates (address)
                worksheet.write_string(i, 0, lat)
                worksheet.write_string(i, 1, lng)
                Title = Title.replace("대한민국 ", "")
                Title = Title.replace("특별시", "")
                Title = Title.replace("광역시", "")          

                worksheet.write_string(i, 2, Title)

                City, Gu, Dong = d_decode_coordinates_to_address (lat, lng)

                City = City.replace("특별시", "")
                City = City.replace("광역시", "")          
                City = City.replace("도", "")

                worksheet.write_string(i, 3, City)
                worksheet.write_string(i, 4, Gu)
                worksheet.write_string(i, 5, Dong)
                worksheet.write_string(i, 6, "GOOGLE")

            except:
                worksheet.write_string(i, 0, 'LocationError')
                print ("Main Func Excpetion")


    workbook.close()


