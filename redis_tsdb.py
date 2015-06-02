# -*- coding:utf-8 -*-

import redis
import time
import requests
import json
#import struct
#import sys


url = "http://125.7.128.53:4242/api/put"
flag = 0

def BLOCK_70(r, block):

        try :
                state=r.get(block)
		print str(unixTime) + " : "+ block + " : " + str(state)

                packets = state.split(":")
                packet = packets[3].replace(",","")
                value = int((packet[:5]))

                data = {
                        "metric":block,
                        "timestamp":time.time(),
                        "value" : value,
                        "tags":{
                                "host":"mobis"
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
        except:
		print "block_70 error"
                pass

def BLOCK_41(r, block):
        try :
                quality=r.rpop(block)
		#print time.time() + "  " + quality

		if quality == 'None':
			print block + " : None"
			return

		print str(unixTime) + " : "+ block + " : " + str(quality)

                packets = quality.split(":")
                packet = packets[3].split(",")

                short_num = packet[0]
                cycle_time = packet[1]
                make_time = packet[2]

                rot_time = packet[3]
                make_loc = packet[4]
                vp_posi = packet[5]

                vc_posi = packet[6]
                remain = packet[7]
                make_pres = packet[8]

                vp_sw_pres = packet[9]
                back_pres = packet[10]
                mold_in_pres = packet[11]

                event_time = packet[12]
                event_date = packet[13]

                str_year = event_date[0:2]
                str_month = event_date[2:4]
                str_day = event_date[4:6]

                str_hour = event_time[0:2]
                str_min = event_time[2:4]
                str_sec = event_time[4:6]

                s = "%s/%s/%s %s:%s:%s" % ("20"+str_year, str_month, str_day, str_hour, str_min, str_sec)
                insertT = time.mktime(time.strptime(s, "%Y/%m/%d %H:%M:%S"))

                data = {
                        "metric":block+"_Snum",
                        "timestamp" : insertT,
                        "value": short_num,
			"tags":{
				"host":"mobis"
				}
                }

                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Cycle_Time",
                        "timestamp" : insertT,
                        "value": cycle_time,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Make_Time",
                        "timestamp" : insertT,
                        "value": make_time,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Rot_Time",
                        "timestamp" : insertT,
                         "value": rot_time,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_Make_Loc",
                        "timestamp" : insertT,
                        "value": make_loc,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_Vp_Posi",
                        "timestamp" : insertT,
                        "value": vp_posi,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Vc_Posi",
                        "timestamp" : insertT,
                        "value": vc_posi,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Remain",
                        "timestamp" : insertT,
                        "value": remain,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_Make_Pres",
                        "timestamp" : insertT,
                        "value": make_pres,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }       
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Vp_Sw_Pres",
                        "timestamp" : insertT,
                        "value": vp_sw_pres,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_Back_Pres",
                        "timestamp" : insertT,
                        "value": back_pres,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_Mold_In_Pres",
                        "timestamp" : insertT,
                        "value": mold_in_pres,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

	except:
		pass


def BLOCK_50(r, block):
        try :
                quality=r.rpop(block)

		if quality == 'None':
			print block + " : Null"
			return

		print str(unixTime) + " : "+ block + " : " + str(quality)

                packets = quality.split(":")
                packet= packets[3].split(",")

                short_num = packet[0]
                nh_temp = packet[1]
                h1_temp = packet[2]

                h2_temp = packet[3]
                h3_temp = packet[4]
                h4_temp = packet[5]

                mold_temp1 = packet[6]
                mold_temp2 = packet[7]
                gas_temp = packet[8]

                lnh_temp = packet[9]
                hopper_temp = packet[10]
                hv_temp = packet[11]

                reserved_temp1 = packet[12]
                reserved_temp2 = packet[13]

                insertT = time.time()

                data = {
                        "metric":block+"_Snum",
                        "timestamp" : insertT,
                        "value": short_num,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }

                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_NH_Temp",
                        "timestamp" : insertT,
                        "value": nh_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_H1_Temp",
                        "timestamp" : insertT,
                        "value": h1_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_H2_Temp",
                        "timestamp" : insertT,
                         "value": h2_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_H3_Temp",
                        "timestamp" : insertT,
                        "value": h3_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_H4_Temp",
                        "timestamp" : insertT,
                        "value": h4_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Mold_Temp1",
                        "timestamp" : insertT,
                        "value": mold_temp1,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Mold_Temp2",
                        "timestamp" : insertT,
                        "value": mold_temp2,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_Gas_Temp",
                        "timestamp" : insertT,
                        "value": gas_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }       
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_LNH_Temp",
                        "timestamp" : insertT,
                        "value": lnh_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_Hopper_Temp",
                        "timestamp" : insertT,
                        "value": hopper_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))
 
                data = {
                        "metric":block+"_HV_Temp",
                        "timestamp" : insertT,
                        "value": hv_temp,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Reserved_Temp1",
                        "timestamp" : insertT,
                        "value": reserved_temp1,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

                data = {
                        "metric":block+"_Reserved_Temp2",
                        "timestamp" : insertT,
                        "value": reserved_temp2,
                        "tags":{
                                "host":"mobis",
                                "short_num": short_num
                                }
                }
                ret = requests.post(url, data=json.dumps(data))

	except:
		pass

def RedisRead():
	r = redis.Redis(host='182.252.222.202', port=6379, db=0)

	try :
		BLOCK_70(r,'F1_R2_BLOCK_70')
		BLOCK_70(r,'F2_R2_BLOCK_70')
		BLOCK_41(r,'F1_R2_BLOCK_41')
		BLOCK_41(r,'F2_R2_BLOCK_41')
		BLOCK_50(r,'F1_R2_BLOCK_50')
		BLOCK_50(r,'F2_R2_BLOCK_50')
	except:
		print "redis read error"
		pass

while(1) : 
	unixTime = time.time()
	t = time.localtime()
	tsec = t.tm_sec

	if tsec%5 !=0 :
		flag = 0
	else :
		try :
			if flag == 0 :
				flag = 1
				print "start"
				RedisRead()
				print "end"
		except :
			pass

