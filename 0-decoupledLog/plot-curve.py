# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import sys

clients = [1, 4, 7, 10, 13, 16, 19]

warmUpOffset = 5
tailOffset = 5

def CalculateP90Latency(rootFolder):
	"""
		Extract latency data from each client execution
	"""
	dataLatency = []
	for i in clients:
		fd = open(str(rootFolder)+str(i)+"/"+str(i)+"c-latency.txt")
		text = fd.readlines()
		fd.close()
		line = []
		for j in text:
			line.append(float(j))
		dataLatency.append(line)

	# Calculate the 90th percentile
	P90Latency = []
	for i in dataLatency:
		arr = np.array(i)
		P90Latency.append(np.percentile(arr, 90))
	
	return P90Latency

def CalculateAveThroughput(svrThroughputFilename):
	"""
		Extract thoughput for each client execution on rep0.txt (leader)
	"""
	fd = open(svrThroughputFilename)
	text = fd.readlines()
	fd.close()

	dataThroughput = []
	sequence = []

	countZeros = 0
	for i in range(len(text)):

		if int(text[i]) == 0:
			countZeros += 1
		
		elif countZeros > 5:
			for j in range(i+warmUpOffset, len(text)):
				if int(text[j]) != 0:
					sequence.append(int(text[j]))
				else:
					break

			dataThroughput.append(sequence[:-tailOffset])
			sequence = []
			i = j
			countZeros = 0
		#if

	# Calculate the average thoughput for each client experiment
	AveThroughput = []
	for i in dataThroughput:
		arr = np.array(i)
		AveThroughput.append(np.mean(arr))

	return AveThroughput


def main():

	P90Latency = CalculateP90Latency("App-NotLog/0/")
	AveThroughput = CalculateAveThroughput("App-NotLog/0/thr-notlog.txt")

	twoLogsP90Lat = CalculateP90Latency("AppLog-Decoup/0/")
	twoLogsAveThr = CalculateAveThroughput("AppLog-Decoup/0/decouplog-thr.txt")

	appLogP90Lat = CalculateP90Latency("AppLog-Coup/0/")
	appLogAveThr = CalculateAveThroughput("AppLog-Coup/0/applog-thr.txt")

	# ======================================
	# ========= Plot Graph =================
	# ======================================

	plt.xlabel('Throughput (cmds/s)')
	plt.ylabel('Latency (ms)')

	#plt.xlabel(u'Vazão (cmds/s)')
	#plt.ylabel(u'Latência (ms)')

	ax = plt.axes()
	ax.yaxis.grid(linestyle='--')

	# Convert ns -> ms
	P90Latency = np.divide(P90Latency, 1000000)
	twoLogsP90Lat = np.divide(twoLogsP90Lat, 1000000)
	appLogP90Lat = np.divide(appLogP90Lat, 1000000)

	# Plot axis
	plt.plot(AveThroughput, P90Latency, "h-b", label="kvstore")
	plt.plot(appLogAveThr, appLogP90Lat, "v:y", label="kvstore-level logging")
	plt.plot(twoLogsAveThr, twoLogsP90Lat, "o--g", label="kvstore with decoupled logging")

	#plt.plot(AveThroughput, P90Latency, "h-b", label="kvstore")
	#plt.plot(appLogAveThr, appLogP90Lat, "v:y", label=u"kvstore com log em nível de aplicação")
	#plt.plot(twoLogsAveThr, twoLogsP90Lat, "o--g", label=u"kvstore com log desacoplado")

	# Layout

	plt.legend(loc='best')

	# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

	plt.savefig('kvstore-128b-dell.png')

if __name__ == "__main__":
    main()