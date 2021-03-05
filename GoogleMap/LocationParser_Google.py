import urllib
import urllib.parse
import urllib.request
import simplejson
import json

import codecs

import xlrd
import xlsxwriter


googleGeocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?'

def decode_address_to_coordinates(address):
        params = {
                'key' : 'AIzaSyDGLfvSZTZPgNn4hMFLqHBoVUpGi0W7o64',
                'address' : address,
                'sensor' : 'false',
        }  
        url = 'https://maps.google.com/maps/api/geocode/json?' + urllib.parse.urlencode(params)
        response = urllib.request.urlopen(url)
        print("URL : " + url)

        print("Response : " + str(response))

        reader = codecs.getreader("utf-8")

        result = json.load(reader(response))

        try:
                lat = str(result['results'][0]['geometry']['location']['lat'])
                lng = str(result['results'][0]['geometry']['location']['lng'])

                print (lat + ", " + lng)
                return (lat, lng)

        except:
                print ('except')
                return exception

if __name__ == "__main__":
    file_location = "C:\\temp\\CreditCardDataSample_temp.xls"
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)

    workbook = xlsxwriter.Workbook('C:\\temp\\GPSLoc.xlsx')
    worksheet = workbook.add_worksheet()

    for i in range(1,10):
        address = sheet.cell_value(i,0)

        print ('Current Count : ' + str(i))

        try:
            lat, lng = decode_address_to_coordinates (address)
            worksheet.write_string(i, 0, lat)
            worksheet.write_string(i, 1, lng)

        except:
            worksheet.write_string(i, 0, 'LocationError')


    workbook.close()


