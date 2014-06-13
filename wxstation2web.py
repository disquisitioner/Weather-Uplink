#! /usr/bin/python
#
# Program to read weather station data and send it to web cloud services.
# This version supports publishing to Xively and Voices
#
# Author: David Bryant
# Version: 1.6
# Date: 11 June, 2014
#
# Expects to receive weather station data over serial port as a line
# of text in the following format:
#
# 	Sample#,Temp1F,Pressure,Temp2F
#
# Logs data received, with a timestamp, to a file for further local procesing
#
# Requires a valid feed ID and API key from Xively, and IDs (names) of the feed's
# channels
#
# Based on previous version built for Cosm (which became Xively), plus liberal
# borrowing from Xively python SDK examples.
#
# Version History
#   1.6   Added support for dweet.io via the dweepy module
#   1.5   Added reporting of data both to Nokia Voices and Xively

import os
import sys
import traceback
import time
import datetime
import serial
import xively
import urllib2
import json
import dweepy

# ------ Program parameters -----
# Xively key and feed URL
XIVELY_API_KEY = 'tS82GBe5Y-xWxg5PzMAN1JyN_JuSAKxRbSs2UWtzQ01XOD0g'
XIVELY_FEED_ID = 1248145598

# Voices metadata
USERID = "dabryant"
UUID = "d9974fad-8888-4d97-b8e8-34b64be46cd6"
LONGITUDE  = "-121.9850"
LATITUDE = "37.1455"
### prep url
voices_url = 'http://voices.stg.nokiaconnect.net:19090/api/v1.0/users/{}/devices/{}/voices/events'.format(USERID,UUID)



# File we're logging data into
#LOG_FILE = './wx_debug_log.txt'
LOG_FILE = '/home/wx/bin/wxlogfile.txt'

# Serial port to open. This may change based on device ports and what's plugged in.
PORT = '/dev/ttyACM0'


# Generator to get us the data reported through the serial port
def read_data(stream):
    for datapacket in stream:
        if datapacket.find('#') == 0:
            print 'Message: ',datapacket
            continue
        print 'Data: ',datapacket.strip()

        # Split line of text into comma-separated fields (data)
        readings = datapacket.strip().split(",")

        # Make sure we received valid data (four fields)
        if len(readings) != 4:
            print "Skipping malformed data: ",readings
            continue
        yield readings


# main routine
def main(device=PORT):
    # Open the file for logging data & seek to the end
    f = open(LOG_FILE,'a+')
    f.seek(2)

    # Initialize Xively API and connect to our feed
    api = xively.XivelyAPIClient(XIVELY_API_KEY)
    feed = api.feeds.get(XIVELY_FEED_ID)

    print voices_url

    # Infinite loop reading data from the input device
    # for samplenum, outtemp, barometer, intemp in read_data(open(device)):
    for samplenum, outtemp, barometer, intemp in read_data(serial.Serial(device)):
        # Post data to Xively
        now = datetime.datetime.utcnow()
        feed.datastreams[0].id = "OutdoorTemp"
        feed.datastreams[0].current_value = outtemp
        feed.datastreams[0].at = now

        feed.datastreams[1].id = "Barometer"
        feed.datastreams[1].current_value = barometer
        feed.datastreams[1].at = now

        feed.datastreams[2].id = "IndoorTemp"
        feed.datastreams[2].current_value = intemp
        feed.datastreams[2].at = now

        # feed.datastreams = [
            # Datastream(id='OutdoorTemp', current_value=outtemp,   at=now),
            # Datastream(id='Barometer',   current_value=barometer, at=now),
            # Datastream(id='IndoorTemp',  current_value=intemp,    at=now),
        # ]
        try:
            feed.update()
        except Exception, e:
            print e
            traceback.print_exc()


        # Now publish data to Voices

        # Need local time to extract values and build ISO 8601 timestamp
        lognow = time.gmtime(time.time())
        timestamp = ( '{0}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}Z'.
              format(lognow.tm_year,lognow.tm_mon,lognow.tm_mday,
              lognow.tm_hour,lognow.tm_min,lognow.tm_sec) )

        # Event structure emulates what Voices Quarks send
        voices_events = [
            {
                "status": "notify", "uuid": UUID, "source": UUID,
                "user": USERID, "longitude": LONGITUDE,
                "latitude": LATITUDE,
                "type": "peripheral.temperature", "id": samplenum,
                "event_time": timestamp,
                "meta": {
                    "units": "degrees F",
                    "service_id": "172901",
                    "peripheral_id": "OutdoorTemp",
                    "value": outtemp,
                },
            },
            {
                "status": "notify", "uuid": UUID, "source": UUID,
                "user": USERID, "longitude": LONGITUDE,
                "latitude": LATITUDE,
                "type": "peripheral.temperature", "id": samplenum,
                "event_time": timestamp,
                "meta": {
                    "units": "degrees F",
                    "service_id": "172901",
                    "peripheral_id": "IndoorTemp",
                    "value": intemp,
                },
            },
            {
                "status": "notify", "uuid": UUID, "source": UUID,
                "user": USERID, "longitude": LONGITUDE,
                "latitude": LATITUDE,
                "type": "peripheral.barometer", "id": samplenum,
                "event_time": timestamp,
                "meta": {
                    "units": "inches Hg",
                    "service_id": "172902",
                    "peripheral_id": "Barometer",
                    "value": barometer,
                },
            },
        ]

        voices_data = json.dumps(voices_events)

        try:
                req = urllib2.Request(voices_url, voices_data)
                req.add_header('Content-Type', 'application/json')
                req.add_header('Content-Length', len(voices_data))

                post = urllib2.urlopen(req)
                print post.read()
                post.close()
        except Exception, e:
                print e


        # Report current sensor info to dweet.io via dweepy
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


        # Write timestamp and data to output file
        f.write(timestamp + ',' + samplenum + ',' + outtemp + ',' + barometer + ',' + intemp + '\n');

        # Flush output buffer and sync to disk
        f.flush()
        os.fsync(f.fileno())

        # If testing, fake a delay between data packets received from the weather station
        time.sleep(60)



if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        print 'Options = ',args
        print 'Device = ',PORT,', Logfile = ',LOG_FILE
        main(*args)
    except KeyboardInterrupt:
        pass

