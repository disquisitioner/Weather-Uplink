# Utility for sending weather station info to ThingSpeak, with all sensors
# being fields in a single channel

# the API key used here must map to the right ThingSpeak channel
TS_API_KEY = 'your_key_goes_here'

import requests

def report_thingspeak(timestamp,outtemp,barometer,intemp,wspeed,wgust,rainfall,raintoday):

    try:
        # Not using https (yet) on Raspberry Pi
        r = requests.post('http://api.thingspeak.com/update',
            json={
                'api_key': TS_API_KEY,
                'field1': timestamp,
                'field2': outtemp,
                'field3': barometer,
                'field4': intemp,
                'field5': wspeed,
                'field6': wgust,
                'field7': rainfall,
                'field8': raintoday
            })

        # Uncomment these for testing purposes
        # print(r.url)
        # print(r.text)

    except Exception, e:
        print e
