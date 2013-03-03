Weather-Station
===============

This repository contains programs used with a home weather station I've designed and built around an Arduino and a variety of digital and analog sensors. At the moment the Arduino is reading a digital temperature sensor mounted outside my house and a combined temperature and barometric pressure sensor inside the house.  Data from each sensor is collected every five seconds, averaged over a five minute period, and then output from the Arduino on its USB port.

The program 'wxstation2cosm.py' contained here runs continuously on a Raspberry Pi connected to the Arduino USB port.  As data from the weather station is received it is stored in a logfile and also uploaded to a multi-stream feed on Cosm.com.  The logfile can then be accessed as a simple database by other programs, several examples of which are included here. Data uploaded to Cosm.com can be viewed on any web browser.

Currently included:
* wxstation2cosm.py - Reads weather station data from a USB port, uploads it to Cosm.com, and stores it in a logfile for use by other programs.
* wxsummary.py - Extracts daily high and low temperature information from a weather station logfile and generates an message file which can be sent to anyone (including the weather station administrator) to summarize conditions observed by the weather station.
* wxchart.py - Generates a chart of daily high and low temperature information from a weather station logfile.  The chart uses the Google Visualization API and the program's output is an HTML file that can be viewed in any browser.

## Usage

### wxstation2cosm.py

The program needs the Cosm.com API Key to be used in uploading data, and the URL for the feed to be used.  You'll need to register for a Cosm.com account if you don't already have one. It also needs the path to the weather station log file.  Edit the program to provide this information.

The program also needs you to specify the USB port to which the Arduino sensor platform is connected.  Edit the program to provide this information as well.

The program runs in an infinite loop.  On my Raspberry Pi I have it configured to be run as part of the system boot sequence so I'm sure it is started automatically whenever the Raspberry Pi is rebooted.

### wxsummary.py

By default the program outputs the daily high and low temperature, along with the time of day for each, for every day contained in the specified weather station logfile.  Command line options allow you to tell the program to just display the high and low temperatures for today or yesterday.

```
wxsummary.py [-h} [-t] [-y] logfile
```

### wxchart.py

Generates a chart of daily high and low temperatures for the specified weather station logfile:
```
wxchart.py logfile
```

