Weather-Uplink
===============

This repository contains programs used to uplink data from a simple home weather station to various cloud services such as Xively and Dweet. The weather station in question is one I've designed and built around an Arduino and a variety of digital and analog sensors. It's capable of reading data from the sensors, processing that data, displaying it on an OLED display, and then periodically emitting aggregate readings over the Arduino's serial port.  (All the code for that will appear on GitHub soon.)

The code here provides a means for getting the periodic sensor readings from the Arduino weather station to any of a number of Interent services through some network-connected system such as a PC or Raspberry Pi. While I could have added network connectivity to the Arduino itself I wanted a separate, more sophisticated system in the loop to properly handle data logging and backup, restarting everything should there be an interruption in power or network connectivity, routine generation of automatic reports, etc.  There are existing tools to do this and someday I might switch to them.  For now, though, this is a fun and interesting way to learn Python, Raspberry Pi, and Linux.

The programs here represent an ongoing evolution in how the weather station's data is uploaded.  In the beginning (late 2012) I selected Cosm as the uplink service given its free and open APIs and ability to both log and interactively graph the data.  In May 2013 Cosm came out of beta and relaunched as Xively, changing its APIs but not its general features, and so I migrated the uplink software to the new interface. Later in 2013 I added support for some other new cloud services, and that's a pattern that has continued through today. 

## Content
**Uplink Code**

In all cases these routines run continuously as background processes on a Raspberry Pi (or PC) connected to the Arduino weather station's serial port. As data from the weather station is received it is stored in a logfile and also uploaded to a variety of web services and weather data sites.  The logfile can then be accessed as a simple database by other programs, several examples of which are included here.

* `wxstation2web.py` -- This is the current version of the uplink application, with the name reflecting that it delivers the regular weather station data to a variety of web services.  All ongoing development is happening in this application
* `wxstation2xively.py` -- A previous version that just uploads data to Xively.com, which was needed when Cosm relaunched as Xively and the APIs changed. Given no ongoing development is happening, this is simply here for reference purposes.
* `wxstation2cosm.py` -- The first generation uplink utility, designed to work with Cosm.com (which no longer exists)


**Other Utilities**

* `wxinit.sh` -- An init script designed to let you install the uplink program as a system service and configure it to be started at boot time.  This allows the uplink process to restart when the system reboots (such as after a power outage).  Information on installing the script as a system service is provided in comments in the script itself.
* `wxsummary.py` -- Extracts daily high and low temperature information from a weather station logfile and generates an message file which can be sent to anyone (including the weather station administrator) to summarize conditions observed by the weather station.
* `wxchart.py` -- Generates a chart of daily high and low temperature information from a weather station logfile.  The chart uses the Google Visualization API and the program's output is an HTML file that can be viewed in any browser.


## Usage

### wxstation2web.py

Each of the web services supported has its own URL, upload API, authentication method, and data format.  Key configuration settings are all at the beginning of the program, with comments
providing guidance on appropriate values.  In some cases you'll need to sign up for the services and create an account, which often generates an access key or some authentication credentials.

Each service implemented is defined in its own Python module, so for example the 
interface to dweet.io is provided in wx_dweet.py.  Adding or removing services is 
therefore much cleaner as the interface can be developed and tested separately as
a Python module and then, when ready, quickly added to the main uplink program.

The program runs in an infinite loop, reading data from the weather station
over the serial port (generally via USB) and then dispatches the relevant information to each service in turn.  On my Raspberry Pi I have it configured to be run as part of the system boot sequence so I'm sure it is started automatically whenever the Raspberry Pi is rebooted. A simpler arrangement is to just start the program from the command line and have it execute independently:

```
% nohup wxstation2cosm.py > wx.out 2>&1 &
```

### wxsummary.py

By default the program outputs the daily high and low temperature, along with the time of day for each, for every day contained in the specified weather station logfile.  Command line options allow you to tell the program to just display the high and low temperatures for today or yesterday.

The program generates the summary as output, so if you want to save it for other purposes you will need to redirect output into a file.  (I save the output and have a separate program that sends it to me as email.)

```
% wxsummary.py [-h} [-t] [-y] wxlogfile > wxsummary.txt
```

### wxchart.py

This program generates a chart of daily high and low temperatures for the specified weather station logfile. The chart takes the form of an HTML file which is generated as output and should be saved, then opened in a browser.
```
% wxchart.py wxlogfile > wxchart.html
```
The chart file generated makes reference to Google Visualization APIs so to be viewed properly you need to be connected to the internet when you load the file into a browser.
