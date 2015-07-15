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



while 1 :
        t = time.localtime()
        tsec = t.tm_sec
	if tsec%10!=0 :
                pass
		
	else :
		endTimeUnix = time.time()
		startTimeUnix = endTimeUnix - 60 

		startTime = datetime.fromtimestamp(startTimeUnix).strftime('%Y/%m/%d-%H:%M:%S')
		endTime = datetime.fromtimestamp(endTimeUnix).strftime('%Y/%m/%d-%H:%M:%S')

		#print startTime
		#print endTime

		meterList = [1011,1012,1021,1022,1031,1041,1051]

		for i in meterList :
			url = 'http://125.7.128.52:4242/api/query?start='+startTime+'&end='+endTime+'&m=sum:gyu_RC1_etype.t_current{nodeid='+str(i)+'}'

			try:
				u = urllib2.urlopen(url)
			except:
				pass

			data = u.read()
			packets = dataParser(data)
			packet = packets.split(',')

			j=len(packet)

			v_s = packet[0].split(":")
			v_e = packet[j-1].split(":")

			try :
				meterExpect = float(v_e[1])-float(v_s[1])
			except :
				meterExpect = 1

        		if i==1011:
				meterExpect = meterExpect*40*4/1000
		        elif i==1012:
				meterExpect = meterExpect*40*4/1000
        		elif i==1021:
				meterExpect = meterExpect*80*4/1000
        		elif i==1022:
				meterExpect = meterExpect*60*4/1000
        		elif i==1031:
				meterExpect = meterExpect*40*4/1000
        		elif i==1041:
				meterExpect = meterExpect*40*4/1000
        		elif i==1051:
				meterExpect = meterExpect*80*4/1000
			if meterExpect > 1000 : 
				pass
			else :
				print "gyu_RC1_etype.15m_expect %d %f nodeid=%d" % ( endTimeUnix, meterExpect*15, i )

		time.sleep(1)
