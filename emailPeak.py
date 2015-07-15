#!/usr/bin/python
# Read_url.py

import sys
import urllib2
import json
import struct
import time
from datetime import datetime, timedelta
#import datetime
import requests
'''
def send_simple_message(nowData, peakData):
        return requests.post(
                "https://api.mailgun.net/v2/sandbox85c2a18d34bd471b86e71ced73417cae.mailgun.org/messages",
                auth=("api", "key-3d350a2e15fbb253820bad0a132b3501"),
                data={"from": "kows17710@gmail.com",
                        "to": "kows17710@gmail.com, gadin.kang@gmail.com, kmcjyk@hanmail.net",
                        "subject": "consumption : " + str(nowData) + "  peak : " + str(peakData),
                        "text": "This is the Peak Alarm Email Test.\n Now 90% Consumption compare to Peak.\nhttp://222.237.78.76:8080/peakHana.jsp"})
'''

def send_simple_message(nowData, peakData):
        return requests.post(
                "https://api.mailgun.net/v2/sandbox85c2a18d34bd471b86e71ced73417cae.mailgun.org/messages",
                auth=("api", "key-3d350a2e15fbb253820bad0a132b3501"),
                data={"from": "kows17710@gmail.com",
                        "to": "kows17710@gmail.com",
                        "subject": "consumption : " + str(nowData) + "  peak : " + str(peakData),
                        "text": "This is the Peak Alarm Email Test.\n Now 90% Consumption compare to Peak.\nhttp://222.237.78.76:8080/peakHana.jsp"})

def dataParser(s):
	s = s.split("{")
	#print data
	i = 0
	j = len(s)
	if j > 2:
		s = s[3].replace("}","")
		s = s.replace("]","")
	else:
		return '0:0,0:0'
	return s

mailFlag = 1 

while 1 :

	t = time.localtime()
	tm = t.tm_hour + t.tm_min
	ts = t.tm_sec

	if ts%2==0:
		pType = 'gyu_9293_senion.t_current'
		urlPeak = 'http://125.7.128.52:4242/api/query?start=1y-ago&m=sum:1y-max:gyu_9293_senion.t_current'

		try:
			u = urllib2.urlopen(urlPeak)
		except:
			pass

		data = u.read()
		packets = dataParser(data)
		packet = packets.split(',')
		peaktmp = packet[0].split(':')
		peak = float(peaktmp[1])
		peakPercent = peak*0.5
		urlNow = 'http://125.7.128.52:4242/api/query?start=5m-ago&m=sum:gyu_9293_senion.t_current' 

		try:
			uNow = urllib2.urlopen(urlNow)
		except:
			pass

		dataNow = uNow.read()
		packetsNow = dataParser(dataNow)
		packetNow = packetsNow.split(',')
		meterDate = 0
		meterData = 0

		for i in range(0, len(packetNow)):
			Nowtmp = packetNow[i].split(':')
			try:
		        	tmp = Nowtmp[1].split(',')
		        	tmpDate = Nowtmp[0].split(',')
       				tmpValue = tmp[0].translate(None, '"')
        			tmpMeterDate = tmpDate[0].translate(None, '"')
			
				if float(meterDate) < float(tmpMeterDate) :
					meterDate = tmpMeterDate
					meterData = tmpValue 
			except:
				print "error"
				pass

		if meterData < 20:
			mailFlag = 0 
		#print "mterData : " + str(meterData) + " peakPercent : " + str(peakPercent)
		if meterData >  peakPercent :
			if mailFlag == 0:
				send_simple_message(meterData, peak)
				print "send : " + t.tm_year+ "/"+t.tm_month+"/"+t.tm_day+"-"+t.tm_hour+":"+t.tm_min+":"+t.tm_sec
				mailFlag = 1  
		else :
			pass


	else :
		pass

