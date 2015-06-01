#!/usr/bin/python

import csv
import urllib2
import time


def load_data(metric, start, end):
	
	def dataParser(s):
		s = s.split("{")
		i = 0
		j = len(s)

		if j > 2:
			s = s[3].replace("}","")
			s = s.replace("]","")
		else:
			return '0:0,0:0'
		return s
	
	#url = 'http://125.7.128.53:4242/api/query?start=2015/05/01-00:00:00&end=2015/06/01-09:46:13&m=sum:F1_R2_BLOCK_41_Cycle_Time'
	url = 'http://125.7.128.53:4242/api/query?start=%s&end=%s&m=sum:%s' % (start, end, metric)

	try:
		u = urllib2.urlopen(url)
	except:
		pass

	data = u.read()
	packets = dataParser(data)
	res = {}
	i = 0
	for l in packets.split(','):
		k, v = l.split(':')
		k = eval(k)
		v = eval(v)
		res[k] = v

	return res



METRICS = {}
#startTime = '2015/06/01-09:55:00' 
#endTime = '2015/06/01-10:55:00' 
#metric_41 = 'F2_R2_BLOCK_41' 

METRIC_41 = 'F1_R2_BLOCK_41_' 

startTime = '185m-ago' # 3h 5m
endTime = '5m-ago' # 5m

#METRICS['etype1'] = load_data('gyu_RC1_thl.temperature', 820, '2015/06/01-09:55:00', '2015/06/01-09:56:00')
#METRICS['etype2'] = load_data('gyu_RC1_thl.temperature', 830, '2015/06/01-09:55:00', '2015/06/01-09:56:00')

METRICS['Snum'] = load_data(METRIC_41 + 'Snum', startTime, endTime)
METRICS['CycleTime'] = load_data(METRIC_41 + 'Cycle_Time', startTime, endTime)
METRICS['MakeTime'] = load_data(METRIC_41 + 'Make_Time', startTime, endTime)
METRICS['RotTime'] = load_data(METRIC_41 + 'Rot_Time', startTime, endTime)
METRICS['MakeLoc'] = load_data(METRIC_41 + 'Make_Loc', startTime, endTime)
METRICS['VpPosi'] = load_data(METRIC_41 + 'Vp_Posi', startTime, endTime)
METRICS['VcPosi'] = load_data(METRIC_41 + 'Vc_Posi', startTime, endTime)
METRICS['Remain'] = load_data(METRIC_41 + 'Remain', startTime, endTime)
METRICS['MakePres'] = load_data(METRIC_41 + 'Make_Pres', startTime, endTime)
METRICS['VpSwPres'] = load_data(METRIC_41 + 'Vp_Sw_pres', startTime, endTime)
METRICS['BackPres'] = load_data(METRIC_41 + 'Back_Pres', startTime, endTime)
METRICS['MoldInPres'] = load_data(METRIC_41 + 'Mold_In_Pres', startTime, endTime)


with open('metric.csv', 'w') as csvfile:
	fieldnames = ['time'] + METRICS.keys()
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	all_times = []
	for metricName in METRICS.keys():
		times = METRICS[metricName].keys()
		#val = METRICS[metricName].values()
		all_times += times
	all_times = sorted(list(set(all_times)))
	
	for t in all_times:
		ctx = {}
		ctx['time'] = t
		
		for metricName in METRICS.keys():
			if t in METRICS[metricName]:
				ctx[metricName] = METRICS[metricName][t]
				#print ctx[metricName]
		writer.writerow(ctx)

