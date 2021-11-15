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

	fd = open('data-analysis-full.csv', 'w')
	fieldnames = ["workload", "config", "interval", "sync", "thr"]
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

					for d in data:
						writer.writerow({
							"workload": w,
							"config":   s,
							"interval": intervals[i],
							"sync":     f == sync_fname,
							"thr":      d
						})
				i += 1
	fd.close()


if __name__ == "__main__":
	main()
