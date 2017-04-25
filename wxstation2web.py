#! /usr/bin/python
#
# Program to read weather station data and send it to web cloud services.
# This version supports publishing to Xively and Dweet.io
#
# Author: David Bryant
# Version: 2.0
# Date: 20 November 2016
#
# Expects to receive weather station data over serial port as a line
# of text in the following format:
#
# 	Sample#,Temp1F,Pressure,Temp2F,WindSpeed,WindGust,Rainfall
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
#   2.0   Added support for Weather Underground, initial modular implementation
#   1.7   Removed Voices support (alas)
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

from collections import deque

from wx_wunderground import report_wu
from wx_dweet import report_dweet
from wx_xively import initialize_xively, report_xively

# ------ Program parameters -----
# Weather Station location
LONGITUDE  = "-121.9850"
LATITUDE = "37.1455"

# File we're logging data into
#LOG_FILE = './wx_debug_log.txt'
LOG_FILE = '/home/wx/bin/wxlogfile.txt'

# Serial port to open. This may change based on device ports and what's plugged in.
PORT = '/dev/ttyACM0'


# Function to calculate timezone offset
def local_time_offset(t=None):
    if t is None:
        t = time.time()

    if time.localtime(t).tm_isdst and time.daylight:
        return -time.altzone
    else:
        return -time.timezone

# Generator to get us the data reported through the serial port
def read_data(stream):
    for datapacket in stream:
        if datapacket.find('#') == 0:
            print 'Message: ',datapacket
            continue
        print 'Data: ',datapacket.strip()

        # Split line of text into comma-separated fields (data)
        readings = datapacket.strip().split(",")

        # Make sure we received valid data (seven fields)
        if len(readings) != 7:
            print "Skipping malformed data: ",readings
            continue
        yield readings


# main routine
def main(device=PORT):
    # Open the file for logging data & seek to the end
    f = open(LOG_FILE,'a+')
    f.seek(2)

    # Initialize Xively API and connect to our feed
    # api = xively.XivelyAPIClient(XIVELY_API_KEY)
    xively_feed = initialize_xively()

    # Initialize variables used to compute rainfall since local midnight and
    # over the last hour (12 reports at a 5 minute interval)
    prev_hr = 0
    raintoday = 0
    rainhr = deque(maxlen=12)

    # Infinite loop reading data from the input device
    # for samplenum, outtemp, barometer, intemp in read_data(open(device)):
    for samplenum, outtemp, barometer, intemp, wspeed, wgust, rainfall in read_data(serial.Serial(device)):

        # Calculate rainfall since local midnight
        localnow = time.localtime();
        if prev_hr == 23 and localnow.tm_hour == 0:
            # This is first sample after local midnight
            prev_hr = 0
            print "Rainfall today ",raintoday
            raintoday = float(rainfall)
        else:
            prev_hr = localnow.tm_hour
            raintoday += float(rainfall)

        # Build ISO 8601 timestamp with local time but show current TZ offset
        # First figure out our timezone offset
        tzoffset = local_time_offset()
        if tzoffset < 0:
            tz_dir = '-'
            tz_delta = -1 * tzoffset
        else:
            tz_dir = '+'
            tz_delta = tzoffset

        tz_hoff = tz_delta / 3600
        tz_moff = (tz_delta % 3600) / 60

        # Then get local time and UTC time
        lognow = time.localtime(time.time())
        now = datetime.datetime.utcnow()

        # Create ISO 8601 timestamp (which some services require)
        timestamp = ( '{0}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}{6:}{7:02d}{8:02d}'.
              format(lognow.tm_year,lognow.tm_mon,lognow.tm_mday,
              lognow.tm_hour,lognow.tm_min,lognow.tm_sec,
              tz_dir,tz_hoff,tz_moff) )

        # Old way: Use GMT to build ISO 8601 timestamp
        # lognow = time.gmtime(time.time())
        # timestamp = ( '{0}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}Z'.
        #       format(lognow.tm_year,lognow.tm_mon,lognow.tm_mday,
        #       lognow.tm_hour,lognow.tm_min,lognow.tm_sec) )


        #######################################################################
        #
        # Post current sensor info to Xively
        #
        if xively_feed != None:
            report_xively(xively_feed,now,outtemp,barometer,intemp,wspeed,wgust,rainfall,raintoday)


        #######################################################################
        #
        # Post current sensor info to dweet.io via dweepy
        #
        report_dweet(timestamp,outtemp,barometer,intemp,wspeed,wgust,rainfall,raintoday)


        #######################################################################
        #
        # Post data to Weather Underground
        #

        # Add current rainfall amount to the hour-long circular buffer.  (Weather
        # underground wants rainfall over the last hour, not the last five minutes,
        # so we need to keep track of the most recent 12 samples and report their sum.)
        rainhr.append(float(rainfall))

        # Report data to Weather Underground
        r = str(sum(rainhr))
        report_wu(now,outtemp,barometer,wspeed,wgust,r,raintoday)



        # Write timestamp and data to output file
        f.write(timestamp + ',' + samplenum + ',' + outtemp + ',' + 
            barometer + ',' + intemp + ',' + wspeed + ',' + wgust + 
            ',' + rainfall +  ',' + "{:0.2f}".format(raintoday) + '\n');

        # Flush output buffer and sync to disk
        f.flush()
        os.fsync(f.fileno())

        # If testing, fake a delay between data packets received from the weather station
        # time.sleep(60)



if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        print 'Options = ',args
        print 'Device = ',PORT,', Logfile = ',LOG_FILE
        main(*args)
    except KeyboardInterrupt:
        pass

