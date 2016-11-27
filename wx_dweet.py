# Upload code specialized for reporting weather station data to dweet.io using 'dweepy'
#
# Author: David Bryant

import dweepy

def report_dweet(timestamp,outtemp,barometer,intemp,wspeed,wgust,rainfall,raintoday):

        try:
            dweepy.dweet_for('orangemoose-wxotemp',{
                'sensor': "Outdoor Temperature",
                'value': outtemp,
                'unit': "degrees F",
                'time': timestamp,
            });
            dweepy.dweet_for('orangemoose-wxitemp',{
                'sensor': "Indoor Temperature",
                'value': intemp,
                'unit': "degrees F",
                'time': timestamp,
            });
            dweepy.dweet_for('orangemoose-wxbaro',{
                'sensor': "Barometric Pressure",
                'value': barometer,
                'unit': "inches HG",
                'time': timestamp,
            });
            dweepy.dweet_for('orangemoose-wxwspeed',{
                'sensor': "Wind Speed",
                'value': wspeed,
                'unit': "MPH",
                'time': timestamp,
            });
            dweepy.dweet_for('orangemoose-wxwgust',{
                'sensor': "Wind Gust",
                'value': wgust,
                'unit': "MPH",
                'time': timestamp,
            });
            dweepy.dweet_for('orangemoose-wxrain',{
                'sensor': "Rainfall",
                'value': rainfall,
                'unit': "inches",
                'time': timestamp,
            });
            dweepy.dweet_for('orangemoose-wxraintoday',{
                'sensor': "Rainfall Today",
                'value': raintoday,
                'unit': "inches",
                'time': timestamp,
            });
        except Exception, e:
            print e
