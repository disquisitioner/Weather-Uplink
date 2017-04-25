# Upload code specialized for reporting weather station data to Weather Underground
#
# Author: David Bryant

from urllib import urlencode
import urllib2

# Need to define the station ID and API key to use for accessing Weather Underground
#
# These are only used here, so they don't need to be any more widely exposed than
# necessary.
wu_station_id = "KCALOSGA222"
wu_static_key = "9abgy802"

# URL to use for uploading raw data
WU_URL = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

# Configuration and convenience variables
WEATHER_UPLOAD = True


# Primary entry point, used to upload data to Weather Underground
def report_wu(dateutc,temp_f,indoortemp_f,pressure,w_mph,w_gust,rainhour,raintoday):
        weather_data = {
                "action": "updateraw",
                "ID": wu_station_id,
                "PASSWORD": wu_static_key,
                "dateutc": str(dateutc),
                "tempf": str(temp_f),
                "indoortempf": str(indoortemp_f),
                "baromin": str(pressure),
                "windspeedmph": str(w_mph),
                "windgustmph": str(w_gust),
                "dailyrainin": str(raintoday),   # rain today in inches
                "rainin": str(rainhour),         # rain inches the past hour
                "softwaretype": "Orangemoose WX",
        }
        # print(weather_data)

        upload_url = WU_URL + "?" + urlencode(weather_data)
        # print(upload_url)
        if WEATHER_UPLOAD:
            try:
                response = urllib2.urlopen(upload_url)
                html = response.read()
                # print "Weather Underground response: '{}'".format(html)
                response.close()  # best practice to close the file
            except Exception, e:
                print e
        else:
            print "Skipping Weather Underground upload"

