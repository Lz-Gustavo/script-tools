# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np


targets = [2000, 4000, 8000, 16000]

latWarmUpOffset = 0 # always even
latTailOffset = 2

thrWarmUpOffset = 0
thrTailOffset = 0


def CalculateAveLatency(rootFolder: str, beelog: bool):
	"""
		Extract server-side latency data from each client execution
		on rootFolder/
	"""
	dataLatency = []
	if not beelog:
		for i in targets:
			fd = open(rootFolder + "/" + str(i) + "thr/latency.out")
			text = fd.readlines()
			fd.close()

			ln = len(text) - latTailOffset
			if ln % 2 != 0:
				ln -= 1

			msr = []
			for j in range(latWarmUpOffset, ln, 2):
				start = int(text[j])
				end = int(text[j+1])
				msr.append(end - start)
			dataLatency.append(msr)

	else:
		for i in targets:
			fd = open(rootFolder + "/" + str(i) + "thr/latency.out")
			text = fd.readlines()
			fd.close()

			msr_etcd = []
			for j in text:
				msr_etcd.append(int(j))

			fd = open(rootFolder + "/" + str(i) + "thr/bl-latency.out")
			text = fd.readlines()
			fd.close()

			msr_bl = []
			for j in text:
				msr_bl.append(int(j))

			msr = []
			bl_cursor = 0
			# msr_etcd will always be > msr_bl, not considering warmupOffset on bl
			for j in range(0, len(msr_etcd) - latTailOffset):
				if msr_etcd[j] == 0:
					bl_cursor += 1
					if bl_cursor >= len(msr_bl):
						break
					continue

				start = int(msr_etcd[j])
				end = int(msr_bl[bl_cursor])
				msr.append(end - start)
			dataLatency.append(msr)

	avelat = []
	for i in dataLatency:
		arr = np.array(i)
		avelat.append(float(np.mean(arr)))
		#avelat.append(float(np.percentile(arr, 90)))
	return avelat


def CalculateAveThroughput(rootFolder: str):
	"""
		Extract thoughput data from each client execution on rootFolder/
	"""
	dataThroughput = []
	for i in targets:
		fd = open(rootFolder + "/" + str(i) + "thr/throughput.out")
		text = fd.readlines()
		fd.close()

		msr = []
		for j in range(thrWarmUpOffset, len(text) - thrTailOffset):
			n = int(text[j])
			#if n > 0:
			msr.append(n)
		dataThroughput.append(msr)

	avethr = []
	for i in dataThroughput:
		arr = np.array(i)
		avethr.append(float(np.mean(arr)))
	return avethr


def SaveIntoFile(arr: list, fn: str):
	fd = open(fn, 'w')
	for fn in arr:
		for f in fn:
			fd.write(str(f) + ",")
		fd.write("\n")	
	fd.close()


def main():
	exp_identifier = "d430-avelat-3"
	thr_fname = [
		"./sl/workloada",
		"./pl-1/workloada",
		"./pl-10/workloada",
		"./pl-100/workloada",
		"./pl-1k/workloada",
	]

	lat_fname = [
		"./sl/workloada",
		"./pl-1/workloada",
		"./pl-10/workloada",
		"./pl-100/workloada",
		"./pl-1k/workloada",
	]

	bl_lat_fname = [
		"",
		"./pl-1/workloada",
		"./pl-10/workloada",
		"./pl-100/workloada",
		"./pl-1k/workloada",
	]

	curve_names = [
		"SL",
		"PL-1",
		"PL-10",
		"PL-100",
		"PL-1k",
	]
	config_formats = ["g-o", "b-D", "k-*", "r-^", "y-H"]

	plt.xlabel('Throughput (k cmds/s)')
	plt.ylabel('Latency (ms)')

	thrs, lats = [], []
	for i in range(0, len(thr_fname)):
		thr = CalculateAveThroughput(thr_fname[i])
		lat = CalculateAveLatency(lat_fname[i], bool(bl_lat_fname[i] != ""))

		np_thr = np.array(thr)
		np_lat = np.array(lat)

		thr = np.divide(np_thr, 1000)
		lat = np.divide(np_lat, 1000000) # ns -> ms
		thrs.append(thr)
		lats.append(lat)
		plt.plot(thr, lat, config_formats[i], label=curve_names[i])

	SaveIntoFile(thrs, "csv/" + exp_identifier + "-throughput.csv")
	SaveIntoFile(lats, "csv/" + exp_identifier + "-latency.csv")

	plt.legend(loc='best')
	fname = 'graphs/workA-' + exp_identifier + '.png'
	print("finished", fname, "...")
	plt.savefig(fname)
	plt.clf()


if __name__ == "__main__":
    main()