# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np

#clients = [5, 9, 13, 17, 21, 25, 29]
#clients = [7, 13, 19, 25, 31, 37, 43]
clients = [9, 17, 25, 33, 41, 49, 57, 65]

warmUpOffset = 5
tailOffset = 5


def CalculateP90Latency(rootFolder):
	"""
		Extract latency data from each client execution
	"""
	dataLatency = []
	for i in clients:
		fd = open(str(rootFolder)+"/"+str(i)+"c-lat.out")
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
		P90Latency.append(float(np.percentile(arr, 90)))
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
		
		elif countZeros > 1 and int(text[i]) != 0:
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
		AveThroughput.append(float(np.mean(arr)))
	return AveThroughput


def ParseSeriesWithLimit(filename, limit):
	"""
		Extracts series on a specific file, at maximum of 'limit' points
		if limit > 0; else everything is parsed.
	"""
	fd = open(filename)
	text = fd.readlines()
	fd.close()

	dataThroughput = []
	reachedSeries = False
	c = 0
	for i in range(len(text)):
		# remove first zero values
		if not reachedSeries:
			if int(text[i]) == 0:
				continue
			else:
				reachedSeries = True
	
		dataThroughput.append(int(text[i]))
		reachedSeries = True
		c += 1
		if limit > 0 and c >= limit:
			break
	return dataThroughput


def main():
	img_identifier = "singlenode"
	thr_fname = [
		#"./defaultlog-run3/workloada/throughput.out",
		"./beelog-100/workloada/throughput.out",
		"./beelog-1k/workloada/throughput.out",
	]

	lat_fname = [
		#"./defaultlog-run3/workloada",
		"./beelog-100/workloada",
		"./beelog-1k/workloada",
	]

	curve_names = [
		#"SL",
		"PL-100",
		"PL-1k",
	]
	config_formats = ["g-o", "b-D", "k-*", "r-^", "y-H"]

	plt.xlabel('Throughput (k cmds/s)')
	plt.ylabel('Latency (ms)')

	#ax = plt.axes()
	#ax.yaxis.grid(linestyle='--')

	for i in range(0, len(thr_fname)):
		thr = CalculateAveThroughput(thr_fname[i])
		lat = CalculateP90Latency(lat_fname[i])

		np_thr = np.array(thr)
		np_lat = np.array(lat)

		thr = np.divide(np_thr, 1000)
		lat = np.divide(np_lat, 1000000) # ns -> ms
		print(len(thr))
		print(len(lat))
		plt.plot(thr, lat, config_formats[i], label=curve_names[i])

	plt.legend(loc='best')
	fname = 'graphs/workA-' + img_identifier + '.png'
	print("finished", fname, "...")
	plt.savefig(fname)
	plt.clf()


if __name__ == "__main__":
    main()