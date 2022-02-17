# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import os

batch_size = "1"
exp_identifier = "etcdbench" + batch_size + "-SL"
title = '(10 100 300 500 1k 1.5k 2k 5k 10k clients) - 1 conn'


def GetArrayFromFile(filename: str):
	fd = open(filename)
	text = fd.readlines()
	fd.close()

	data = []
	for ln in text:
		n = float(ln)
		if n > 0:
			data.append(n)
	return data


def main():
	thr_fname = [
		"./put-throughput.out",
	]

	lat_fname = [
		"./put-latency.out",
	]

	curve_names = [
		"put",
	]
	config_formats = ["g-o", "b-D", "k-*", "r-^", "y-H"]

	plt.xlabel('Throughput (k cmds/s)')
	plt.ylabel('Latency (sec)')

	thrs, lats = [], []
	for i in range(0, len(thr_fname)):
		thr = GetArrayFromFile(thr_fname[i])
		lat = GetArrayFromFile(lat_fname[i])

		np_thr = np.array(thr)
		np_lat = np.array(lat)

		thr = np.divide(np_thr, 1000)
		#lat = np.divide(np_lat, 1000000) # ns -> ms
		thrs.append(thr)
		lats.append(lat)
		plt.plot(thr, lat, config_formats[i], label=curve_names[i])


	plt.title(title)
	plt.legend(loc='best')

	if not os.path.exists('graphs/'):
		os.mkdir('graphs/')

	fname = 'graphs/' + exp_identifier + '.png'
	print("finished", fname, "...")
	plt.savefig(fname)
	plt.clf()


if __name__ == "__main__":
    main()
