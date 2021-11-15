# -*- coding: utf-8 -*-
import numpy as np
import csv
import sys


def ParseThroughput(filename):
	"""
		Extracts thoughput on specific filename.
	"""
	fd = open(filename)
	text = fd.readlines()
	fd.close()

	dataThroughput = []
	reachedSeries = False
	for i in range(len(text)):
		# remove first zero values
		if not reachedSeries:
			if int(text[i]) == 0:
				continue
			else:
				reachedSeries = True
	
		dataThroughput.append(int(text[i]))
		reachedSeries = True
	return dataThroughput


def main():
	series = ["SL", "PL-2t", "PL-10t"]
	workloads = ["YCSB-A", "YCSB-AW", "YCSB-AWL", "YCSB-B", "YCSB-D"]

	configs = {
		"PL-2t": [
			"/beelog/thr-int-1.out",
			"/beelog/thr-int-10.out",
			"/beelog/thr-int-100.out",
			"/beelog/thr-int-1000.out",
		],
		"PL-10t": [
			"/beelog/thr-int-1.out",
			"/beelog/thr-int-10.out",
			"/beelog/thr-int-100.out",
			"/beelog/thr-int-1000.out",
		],
		"SL": [
			"/trad/thr-int-1000.out",
			"/tradbatch/thr-int-10.out",
			"/tradbatch/thr-int-100.out",
			"/tradbatch/thr-int-1000.out",
		]
	}
	intervals = ["1", "10", "100", "1000"]

	fd = open('data-analysis.csv', 'w')
	fieldnames = ["workload", "config", "interval", "sync", "makespan", "trimmed", "average", "percentile90", "std-dev", "median"]
	writer = csv.DictWriter(fd, fieldnames=fieldnames)
	writer.writeheader()

	for w in workloads:
		for s in series:
			i = 0
			for c in configs[s]:
				fname = s + '/' + w + c
				sync_fname = 'sync/' + s + '/' + w + c

				for f in [fname, sync_fname]:
					data = ParseThroughput(f)

					# one each sec
					makespan = len(data)
					trim = False

					# trim first/last if enough points
					if makespan >= 5:
						data = data[1:-1]
						trim = True

					arr = np.array(data)
					ave = np.mean(arr)
					p90 = np.percentile(arr, 90)
					stddev = np.std(arr)
					med = np.median(arr)

					writer.writerow({
						"workload":     w,
						"config":       s,
						"interval":     intervals[i],
						"sync":         f == sync_fname,
						"makespan":     makespan,
						"trimmed":      trim,
						"average":      ave,
						"percentile90": p90,
						"std-dev":      stddev,
						"median":       med,
					})
				i += 1
	fd.close()


if __name__ == "__main__":
	main()
