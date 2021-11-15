# -*- coding: utf-8 -*-
import pandas as pd
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


def ParseLatencyTuples(filename):
	data = pd.read_csv(filename)

	# currently returning total latency, t4 - t1
	return data["t4"] - data["t1"]


def main():
	series = ["SL", "PL-2t"]
	workloads = ["YCSB-A", "YCSB-AW", "YCSB-AWL", "YCSB-B", "YCSB-D"]

	latency = {
		"PL-2t": [
			"/bl-1-latency.out",
			"/bl-10-latency.out",
			"/bl-100-latency.out",
			"/bl-1000-latency.out",
		],
		"SL": [
			"/trad-1-latency.out",
			"/trad-10-latency.out",
			"/trad-100-latency.out",
			"/trad-1000-latency.out",
		]
	}

	# looooool
	translate_series = {
		"SL": "SL",
		"PL-2t": "PL",
	}

	intervals = ["1", "10", "100", "1000"]

	fd = open('data-latency.csv', 'w')
	fieldnames = ["workload", "config", "interval", "p90_lat", "ave_lat", "ave_lat_ms"]
	writer = csv.DictWriter(fd, fieldnames=fieldnames)
	writer.writeheader()

	for w in workloads:
		for s in series:
			i = 0
			for l in latency[s]:
				fname = s + '/' + w + l
				data = []
				if s == "SL":
					# same troughput parse procedure
					data = ParseThroughput(fname)

				else:
					data = ParseLatencyTuples(fname)
				
				lat = np.array(data)
				p90_lat = np.percentile(lat, 90)
				ave_lat = np.mean(lat)
				ave_lat_ms = np.divide(ave_lat, 1000000)


				writer.writerow({
					"workload":   w,
					"config":     translate_series[s],
					"interval":   intervals[i],
					"p90_lat":    p90_lat,
					"ave_lat":    ave_lat,
					"ave_lat_ms": ave_lat_ms,
				})
				i += 1

	fd.close()


if __name__ == "__main__":
	main()
