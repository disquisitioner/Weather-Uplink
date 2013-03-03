#! /usr/bin/python
#
# Program to generate summary information from Weather Station data log files
# Author: David Bryant (djbryant@gmail.com)
# Version: 1.0
# Date: 3 March 2013
#

import argparse
import time
from datetime import date, timedelta

# Backhand way of using the degree symbol
DEGREE_SYM = unichr(176).encode("latin-1")

# Create the argument parser
parser = argparse.ArgumentParser(description='Summarize daily information from the weather station log file. By default displays all days covered in the log file.')

# Arguments supported
#  logfile        REQUIRED, specifies the file containing the weather log data to be scanned
#  -t,--today     OPTIONAL, just show summary for today
#  -y,--yesterday OPTIONAL, just show summary for yesterday

parser.add_argument("logfile",help="Path to the weather station log file to be summarized")
parser.add_argument("-t","--today",help="Just show summary for today, can be combined with -y", 
	action="store_true")
parser.add_argument("-y","--yesterday",help="Just show summary for yesterday, can be combined with -t", 
	action="store_true")

args = parser.parse_args()

# Echo argument info (just while developing...)
print "Weather station log file is '{}'".format(args.logfile)

today = date.today()
yest  = date.today() - timedelta(days=1)

if args.today:
	print "Look for data only on date {}/{}/{}".format(today.month,today.day,today.year)

if args.yesterday:
	print "Look for data only on date {}/{}/{}".format(yest.month,yest.day,yest.year)

# Open specified weather station logfile
f = open(args.logfile,'r')

# Initialize variables
t_mo  = 0
t_day = 0
day_low  =  10000
day_high = -10000

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
#		if ( ((not args.today)     or (today.month == t_mo and today.day == t_day)) and
#             ((not args.yesterday) or (yest.month == t_mo and yest.day == t_day)) ):
	if t_day != day:
		if ( (args.today and today.month == t_mo and today.day == t_day) or
             (args.yesterday and yest.month == t_mo and yest.day == t_day) or
             (not args.today and not args.yesterday) ):
			print "On {:02d}/{:02d} - High of {}{}F at {}, Low of {}{}F at {}".format(t_mo,t_day,day_high,DEGREE_SYM,time_high,day_low,DEGREE_SYM,time_low)
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
if ( (args.today and today.month == t_mo and today.day == t_day) or
	 (args.yesterday and yest.month == t_mo and yest.day == t_day) or
     (not args.today and not args.yesterday) ):
	print "On {:02d}/{:02d} - High of {}{}F at {}, Low of {}{}F at {}".format(t_mo,t_day,day_high,DEGREE_SYM,time_high,day_low,DEGREE_SYM,time_low)
