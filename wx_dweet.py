# Upload code specialized for reporting weather station data to dweet.io using 'dweepy'
#
# Author: David Bryant

import dweepy

def report_dweet(timestamp,outtemp,barometer,intemp,wspeed,wgust,rainfall,raintoday):

        try:

            dweepy.dweet_for('orangemoose-wxstation',{
                'time' : timestamp,
                'sensors' : [
                    {
                        'name' : 'Outdoor Temperature',
                        'value' : outtemp,
                        'units' : 'degrees F',
                    },
                    {
                        'name' : 'Indoor Temperature',
                        'value' : intemp,
                        'units' : 'degrees F',
                    },
                    {
                        'name' : 'Barometric pressure',
                        'value' : barometer,
                        'units' : 'inches Hg',
                    },
                    {
                        'name' : 'Wind Speed',
                        'value' : wspeed,
                        'units' : 'MPH',
                    },
                    {
                        'name' : 'Wind Gust',
                        'value' : wgust,
                        'units' : 'MPH',
                    },
                    {
                        'name' : 'Rainfall',
                        'value' : rainfall,
                        'units' : 'inches',
                    },
                    {
                        'name' : 'Rainfall Today',
                        'value' : raintoday,
                        'units' : 'inches',
                    }
                ]
            })
        except Exception, e:
            print e

