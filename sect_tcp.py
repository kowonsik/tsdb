#!/usr/bin/python

import socket
import time
import os
import sys
import struct
import thread

from SocketServer import ThreadingTCPServer, StreamRequestHandler
PORT = 3333 

ETYPE_VALUE_MAX = 8000

state = 0
packet =''

def bigEndian(s):
	res = 0
	while len(s):
		s2 = s[0:2]
		s = s[2:]

		res <<=8
		res += eval('0x' + s2)
	return res

def littleEndian(s):
	res = 0
	while len(s):
		s2 = s[-2:]
		s = s[:-2]

		res <<= 8
		res += eval('0x' + s2)
	return res

def swapBytes(s):
	assert len(s) == 8, s
	res = s[2:4] + s[0:2] + s[6:8] + s[4:6]
	assert len(res) == 8, s + "->" + res
	return res

def toFloat(s):
	assert len(s) == 8,s
	hex = '"' + '\\x' + s[0:2] + '\\x' +s[2:4] + '\\x' + s[4:6] + '\\x'+s[6:8]+'"'
	hex = eval(hex)
	res = struct.unpack('f', hex)[0]
	return res
	

def sese(s):
	head = s[:20]
	type = s[20:24]
	
	serialID = s[24:36]
	nodeID = s[36:40]
	seq = s[40:44]
	
	if type == "0064" : # TH
		temperature = bigEndian( s[48:52] )
		humidity = bigEndian( s[52:56] )
		light = bigEndian( s[56:60] )
		
		v1 = -39.6 + 0.01 * temperature
		tmp = -4 + 0.0405 * humidity + (-0.0000028) * humidity * humidity
		v2 = (v1 - 25) * (0.01 + 0.00008 * humidity) + tmp
		tmp = (light * 100) / 75
		v3 = tmp * 10
		
		t = int(time.time())
		if -50 < v1 < 80 :
				sys.stdout.write( "gyu_RC1_thl.temperature %d %f nodeid=%d\n" % ( t, v1, bigEndian( nodeID ) ))
		if v2 > 0 :
			if v1 < 100 :
				sys.stdout.write( "gyu_RC1_thl.humidity %d %f nodeid=%d\n" % ( t, v2, bigEndian( nodeID ) ))
		if v3 > 0 :
			if v3 < 10000 :
				sys.stdout.write( "gyu_RC1_thl.light %d %f nodeid=%d\n" % ( t, v3, bigEndian( nodeID ) ))
		
	elif type == "0070" : # TH
		temperature = bigEndian( s[48:52] )
		humidity = bigEndian( s[52:56] )
		light = bigEndian( s[56:60] )

		v1 = -46.85 + 0.01 * temperature
		tmp = -6 + 125 * humidity / 4095
		v2 = tmp
		tmp = (light * 1.017)
		v3 = tmp

		t = int(time.time())

		if -50 < v1 < 80 :
				sys.stdout.write( "gyu_RC1_thl.temperature %d %f nodeid=%d\n" % ( t, v1, bigEndian( nodeID ) ))
		if v2 > 0 :
			if v1 < 100 :
				sys.stdout.write( "gyu_RC1_thl.humidity %d %f nodeid=%d\n" % ( t, v2, bigEndian( nodeID ) ))
		if v3 > 0 :
			if v3 < 10000 :
				sys.stdout.write( "gyu_RC1_thl.light %d %f nodeid=%d\n" % ( t, v3, bigEndian( nodeID ) ))

	elif type == "0065":
		t = int(time.time())
		pir = bigEndian(s[48:52])
		sys.stdout.write( "gyu_RC1_pir %d %f nodeid=%d\n" % ( t, pir, bigEndian( nodeID ) ))
		pass
	elif type == "0066":
		ppm = s[48:52]

		t = int(time.time())
		tmp = float(bigEndian(ppm))
		value = float(1.5*(tmp/4086)*2*1000)
		if value > 0 :
			if value < 2500 : 
				sys.stdout.write( "gyu_RC1_co2.ppm %d %f nodeid=%d\n" % (t, value, bigEndian(nodeID)))

	elif type == "006D" or type == "006d":  #Splug

		rawData = s[54:60]
		tmp = bigEndian(rawData)
		if tmp > 15728640:
			tmp = 0
		else:
			tmp = float(tmp/4.127/10)

		watt = tmp
		t = int(time.time())
		if watt >= 0:
			if watt < 3000 :
				sys.stdout.write( "gyu_RC1_splug.watt %d %f nodeid=%d\n" % (t, watt, bigEndian(nodeID)))

	elif type == "0072": #Splug2
		rawData = s[48:56]
		tmp = bigEndian(rawData)
		if tmp > 15728640:
			tmp=0
		else:
			tmp = float(tmp/100)
			watt = tmp

			t_watt_rawData = s[56:64]
			t_watt_tmp = bigEndian( t_watt_rawData)
			t_watt_tmp = float( t_watt_tmp / 10000000.0 )
			t_watt = t_watt_tmp

			t = int(time.time())
			if watt >= 0:
				if watt < 3000 :
					sys.stdout.write( "gyu_RC1_splug.watt %d %f nodeid=%di\n" % (t, watt, bigEndian(nodeID)))
			sys.stdout.write( "gyu_RC1_splug.t_watt %d %f nodeid=%d" %(t, t_watt, bigEndian(nodeID)))

	elif type == "00D3" or type == "00d3":       #etype
		if len(s) < 72:
			sys.stderr.write("ignore too short data for etype:" + s)
		else :	
			t_current = s[48:56]
			current = s[64:72]
			current = toFloat(swapBytes(current))
			t_current = littleEndian(swapBytes(t_current))
			nodeID = bigEndian(nodeID)

			if current > ETYPE_VALUE_MAX:
				sys.stderr.write( "overflow etype.current: %f, nodeID=%d\n" %(current, nodeID))
			elif current <= 0:
				sys.stderr.write( "underflow etype.current: %f, nodeID=%d\n" %(current, nodeID))
			else:
				t = int(time.time())
				sys.stdout.write( "gyu_RC1_etype.t_current %d %d nodeid=%d\n" % (t, t_current, nodeID))
				sys.stdout.write( "gyu_RC1_etype.current %d %f nodeid=%d\n" % (t, current, nodeID))
			
	elif type == "0071":
		ppm = s[48:52]

		t = int(time.time())
		tmp = int(bigEndian(ppm))
		value = tmp
		sys.stdout.write( "gyu_RC1_co2.ppm %d %f nodeid=%d\n" % (t, value, bigEndian(nodeID)))

	elif type == "0063":   # base
		recv = bigEndian(s[48:52])
		send = bigEndian(s[52:56])
		t = int(time.time())
		sys.stdout.write( "gyu_RC1_base.recv %d %f nodeid=%d\n" % (t, recv, bigEndian(nodeID)))
		sys.stdout.write( "gyu_RC1_base.send %d %f nodeid=%d\n" % (t, send, bigEndian(nodeID)))

	else:
		sys.stderr.write( "Invalid type : " + type)
		pass


def handler(clientsock, addr):
	print "connect : " + str(addr) 

	while 1:
		data = clientsock.recv(1024)
		data_in = data.encode('hex')
		#print data_in
		start = data_in[0:2]
		if( start == '7e'):
			p_end = 0
			packet = ""
			p_flag = 0
			p_len = 0
			recv_len = len(data_in)
			#print p_len, ",", recv_len
			while p_len < recv_len:
				byte = str(data_in[p_len:p_len+2])
				if(byte == '7e'):
					if(p_end == 0): # packet start
						packet = "7e"
						p_end = 1
					elif(p_end == 1):# packet end
						packet = packet + '7e'
						#print packet
						sese(packet)
						p_end = 0
					p_len += 2
					continue

				if(byte == '7d'):
					p_flag = 1
					pass
				elif (p_flag == 1):
					if(byte == '5e'):
						byte = '7e'
						packet ='%s%s' % (packet, byte)
					elif(byte == '5d'):
						byte = '7d'
						packet ='%s%s' % (packet, byte)
					else:
						break
				else:
					packet ='%s%s' % (packet, byte)
				p_len += 2
			#:sese(packet)
		sys.stdout.flush()

if __name__ == '__main__':

	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	

	tcpsock.bind(('',PORT))
	tcpsock.listen(5)

	while True:
		clientsock, addr = tcpsock.accept()
		thread.start_new_thread(handler, (clientsock,addr))
