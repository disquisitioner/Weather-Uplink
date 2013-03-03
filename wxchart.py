#! /usr/bin/python
#
# Program to generate data plot from Weather Station data log files
# using Google Chart's 'candlestick' chart type
# Author: David Bryant (djbryant@gmail.com)
# Version: 1.0
# Date: 3 March, 2013
#

import argparse
import time
from datetime import date, timedelta

def print_htmlfront():
    print "<html xmlns=\"http://www.w3.org/1999/xhtml\">"
    print "  <head>"
    print "    <meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\"/>"
    print "    <title>"
    print "      Google Visualization API Sample"
    print "    </title>"
    print "    <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>"
    print "    <script type=\"text/javascript\">"
    print "      google.load('visualization', '1', {packages: ['corechart']});"
    print "    </script>"
    print "    <script type=\"text/javascript\">"
    print "      function drawVisualization() {"
    print "        var data = google.visualization.arrayToDataTable(["

def print_htmlback():
    print "          // Treat first row as data as well."
    print "        ], true);"
    print " "
    print "        var options = {"
    print "          legend:'none',"
    print "          title: 'Daily Temperature At Home',"
    print "          vAxis: {title:'Temperature (F)'},"
    print "          hAxis: {title:'Date'}"
    print "        };"
    print " "
    print "        var chart = new google.visualization.CandlestickChart(document.getElementById('chart_div'));"
    print "        chart.draw(data, options);"
    print "      }"
    print " "
    print "      google.setOnLoadCallback(drawVisualization);"
    print "    </script>"
    print "  </head>"
    print "  <body>"
    print "    <div id=\"chart_div\" style=\"width: 900px; height: 500px;\"></div>"
    print "  </body>"
    print "</html>"


# Backhand way of using the degree symbol
DEGREE_SYM = unichr(176).encode("latin-1")

# Create the argument parser
parser = argparse.ArgumentParser(description='Summarize daily information from the weather station log file. By default displays all days covered in the log file.')

# Arguments supported
#  logfile        REQUIRED, specifies the file containing the weather log data to be scanned

parser.add_argument("logfile",help="Path to the weather station log file to be summarized")

args = parser.parse_args()

# Echo argument info (just while developing...)
print "Weather station log file is '{}'".format(args.logfile)

today = date.today()
yest  = date.today() - timedelta(days=1)

# Open specified weather station logfile
f = open(args.logfile,'r')

# Initialize variables
t_mo  = 0
t_day = 0
day_low  =  10000
day_high = -10000

# print HTML front part
print_htmlfront()

# Go through every line in the logfile...
for line in f:
	data =  line.strip().split(',')

 	# 2012-12-24T21:49:31
	# Process timestamp
	yr  = int( data[0][0:4] )
	mo  = int( data[0][5:7] )
	day = int(data[0][8:10] )
	hr  = int( data[0][11:13] )
	min = int( data[0][14:16] )
	sec = int( data[0][17:] )

	# If this is the first data record we've processed initialize everything
	if t_day == 0:
		t_day = day
		t_mo = mo
		day_low = data[2]
		day_high = data[2]
		time_low  = "{:02d}:{:02d}".format(hr,min)
		time_high = "{:02d}:{:02d}".format(hr,min)
		# Skip to next data record
		continue

	# Not first record, so process it

	# If this record has a new date then we've read all of the prior day's data
	# so generate the daily summary
	if t_day != day:
                print "['{:02d}/{:02d}',{}, {}, {}, {}],".format(
                    t_mo,t_day,day_low,day_low,day_high,day_high)
		t_day = day;
		t_mo = mo;
		day_low = data[2]
		day_high = data[2]
		time_low  = "{:02d}:{:02d}".format(hr,min)
		time_high = "{:02d}:{:02d}".format(hr,min)
	else:
		if data[2] < day_low:
			day_low = data[2]
			time_low  = "{:02d}:{:02d}".format(hr,min)
		if data[2] > day_high:
			day_high = data[2]
			time_high = "{:02d}:{:02d}".format(hr,min)
		continue


# Print last day
print "['{:02d}/{:02d}',{}, {}, {}, {}]".format(
    t_mo,t_day,day_low,day_low,day_high,day_high)

print_htmlback()
