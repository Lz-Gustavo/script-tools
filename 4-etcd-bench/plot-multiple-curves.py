# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import os

batch_size = "100"
sub_folder = "1"

exp_identifier = "batch" + batch_size + "-" + sub_folder
title = '[100 300 500 1k 1.5k 2k 5k clients]'


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
	thr_fnames = [
		"./" + sub_folder + "/normal/sl-" + batch_size + "/put-throughput.out",
		"./" + sub_folder + "/normal/pl-" + batch_size + "/put-throughput.out",
		"./" + sub_folder + "/2disks/pl-" + batch_size + "/put-throughput.out",
		"./" + sub_folder + "/4disks/pl-" + batch_size + "/put-throughput.out",
		"./" + sub_folder + "/6disks/pl-" + batch_size + "/put-throughput.out",
	]

	lat_fnames = [
		"./" + sub_folder + "/normal/sl-" + batch_size + "/put-latency.out",
		"./" + sub_folder + "/normal/pl-" + batch_size + "/put-latency.out",
		"./" + sub_folder + "/2disks/pl-" + batch_size + "/put-latency.out",
		"./" + sub_folder + "/4disks/pl-" + batch_size + "/put-latency.out",
		"./" + sub_folder + "/6disks/pl-" + batch_size + "/put-latency.out",
	]

	curve_names = [
		"SL",
		"PL",
		"PL-2disk",
		"PL-4disk",
		"PL-6disk"
	]
	config_formats = ["g-o", "b-D", "k-*", "r-^", "y-H"]

	plt.xlabel('Throughput (k cmds/s)')
	plt.ylabel('Latency (sec)')

	plt.grid(axis="y")

	thrs, lats = [], []
	for i in range(0, len(thr_fnames)):
		thr = GetArrayFromFile(thr_fnames[i])
		lat = GetArrayFromFile(lat_fnames[i])

		#truncate last ones
		thr = thr[:len(thr)-3]
		lat = lat[:len(lat)-3]

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
