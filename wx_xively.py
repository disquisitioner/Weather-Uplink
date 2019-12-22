
# Upload code specialized for reporting weather station data to dweet.io using 'dweepy'
#
# Author: David Bryant

import traceback
import xively

# Xively key and feed URL.  Put yours here (these won't work)
XIVELY_API_KEY = 'your_xively_key_goes_here'
XIVELY_FEED_ID = 1234567890

# Initialize the connection to Xively, returning the appropriate feed.  If Xively is
# unavailable (which can happen) returns a feed value of 'None'
def initialize_xively():
    feed = None
    # Initialize Xively API and connect to our feed
    try:
        api = xively.XivelyAPIClient(XIVELY_API_KEY)
        # print "Xively api active"
    except Exception, e:
        print e
        # traceback.print_exc()
        return None

    try:
        feed = api.feeds.get(XIVELY_FEED_ID)
        # print "Xively feed retrieved"
    except Exception, e:
        print "ERROR: Unable to retrieve feed from Xively!"
        print e
        # traceback.print_exc()
    return feed

def report_xively(feed,now,outtemp,barometer,intemp,wspeed,wgust,rainfall,raintoday):
        feed.datastreams[0].id = "OutdoorTemp"
        feed.datastreams[0].current_value = outtemp
        feed.datastreams[0].unit.label  = "degrees F"
        feed.datastreams[0].unit.symbol = "F"
        feed.datastreams[0].at = now

        feed.datastreams[1].id = "Barometer"
        feed.datastreams[1].current_value = barometer
        feed.datastreams[1].unit.label  = "inches Hg"
        feed.datastreams[1].unit.symbol = "in Hg"
        feed.datastreams[1].at = now

        feed.datastreams[2].id = "IndoorTemp"
        feed.datastreams[2].current_value = intemp
        feed.datastreams[2].unit.label  = "degrees F"
        feed.datastreams[2].unit.symbol = "F"
        feed.datastreams[2].at = now

        feed.datastreams[3].id = "WindSpeed"
        feed.datastreams[3].current_value = wspeed
        feed.datastreams[3].unit.label  = "Miles per hour"
        feed.datastreams[3].unit.symbol = "MPH"
        feed.datastreams[3].at = now

        feed.datastreams[4].id = "WindGust"
        feed.datastreams[4].current_value = wgust
        feed.datastreams[4].unit.label  = "Miles per hour"
        feed.datastreams[4].unit.symbol = "MPH"
        feed.datastreams[4].at = now

        feed.datastreams[5].id = "Rainfall"
        feed.datastreams[5].current_value = rainfall
        feed.datastreams[5].unit.label  = "inches"
        feed.datastreams[5].unit.symbol = "in"
        feed.datastreams[5].at = now

        feed.datastreams[6].id = "RainfallToday"
        feed.datastreams[6].current_value = raintoday
        feed.datastreams[6].unit.label  = "inches"
        feed.datastreams[6].unit.symbol = "in"
        feed.datastreams[6].at = now

        # feed.datastreams = [
            # Datastream(id='OutdoorTemp',  current_value=outtemp,   at=now),
            # Datastream(id='Barometer',    current_value=barometer, at=now),
            # Datastream(id='IndoorTemp',   current_value=intemp,    at=now),
            # Datastream(id='WindSpeed',    current_value=wspeed,    at=now),
            # Datastream(id='WindGust',     current_value=wgust,     at=now),
            # Datastream(id='Rainfall',     current_value=rainfall,  at=now),
            # Datastream(id='RainfallToday',current_value=raintoday, at=now),
        # ]
        try:
            feed.update()
        except Exception, e:
            print e
            traceback.print_exc()
