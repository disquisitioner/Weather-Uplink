#! /usr/bin/python
#
# Program to read weather station data and send it to Cosm as a feed
# Author: David Bryant
# Version: 1.2
# Date: 2 January, 2013
#
# Expects to receive weather station data over serial port as a line
# of text in the following format:
#
# 	Sample#,Temp1F,Pressure,Temp2F
#
# Logs data received, with a timestamp, to a file for further local procesing
#
# Requires a valid user's API key from Cosm, and the identifying URL of the feed

import os
import time
import eeml
import datetime
import serial

# ------ Program parameters -----
# Cosm key and feed URL
API_KEY = 'ENTER_YOUR_API_KEY_HERE'
API_URL = 'ENTER_YOUR_FEED_URL_HERE'
TEST_API_URL = 'ENTER_TEST_FEED_URL_HERE_(IF_ANY)'

# File we're logging data into
LOG_FILE = '/home/wx/bin/wxlogfile.txt'

# Serial port to open. This may change based on device ports and what's plugged in.
PORT = '/dev/ttyACM0'
#--------------------------------

# ----- Define special units class to use for pressure -----
class InchesHg(eeml.Unit):
    """
    Degree Inches of Mercury (Barometric Pressure)  unit class.
    """

    def __init__(self):
        """
        Initialize the `Unit` parameters with Inches of Mercury.
        """
        eeml.Unit.__init__(self, 'Inches Hg', 'derivedSI', 'inHg')
# ---------------------------

# ----- Initialization -----
# Open the file for logging data
f = open(LOG_FILE,'a+')

# Seek to the end of the file
f.seek(2)

# Open the serial port
ser = serial.Serial(PORT)
print 'Opening: ',ser.portstr

# Initialize connection to Cosm
pac = eeml.Pachube(API_URL, API_KEY)
# --------------------------

# ----- Main loop -----
print 'Entering main loop'
while True:
    # Retrieve line of text sent by sensor platform via serial connection
    datapacket = ser.readline().strip()

    # Check to see if we received data or a message, and ignore messages
    if datapacket.find('#') == 0:
        print 'Message: ',datapacket
        continue
    else:
        print 'Data: ',datapacket

    # Split line of text into comma-separated fields (data)
    readings = datapacket.split(",")

    # Make sure we received valid data (four fields)
    if len(readings) != 4:
	print "Skipping malformed data: ",readings
        continue

    # Need local time to use for timestamp
    now = time.localtime(time.time())

    # Construct ISO 8601 format date/time string
    timestamp = ( '{0}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}'.
      format(now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec) )

    # Send data to Cosm
    pac.update([
    	eeml.Data(0, readings[1], unit=eeml.Fahrenheit()),
        eeml.Data(1, readings[2], unit=InchesHg()),
    	eeml.Data(2, readings[3], unit=eeml.Fahrenheit()),
        ])
    try:
        pac.put()
    except Exception as e:
	print "Failure sending @ {0}, exception: {1}".format(timestamp,e)

    # Write timestamp and data packet to output file
    f.write(timestamp + ',' + datapacket + '\n');

    # Flush output buffer and sync to disk
    f.flush()
    os.fsync(f.fileno())
# ----- End of main loop -----

# Close the file & serial port, though main program loops may never get here...
f.close()
ser.close()
