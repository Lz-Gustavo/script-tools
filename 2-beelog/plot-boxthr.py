# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import sys

def ParseThroughput(svrThroughputFilename):
	"""
		Extract thoughput for each client execution on rep0.txt (leader)
	"""
	fd = open(svrThroughputFilename)
	text = fd.readlines()
	fd.close()

	dataThroughput = []
	reachedSeries = False
	for i in range(len(text)):
		# remove first zero values on boxplot
		if not reachedSeries:
			if int(text[i]) == 0:
				continue
			else:
				reachedSeries = True

		dataThroughput.append(int(text[i]))
		reachedSeries = True
	return dataThroughput


def setBoxColors(bp):
	plt.setp(bp['boxes'][0], color='blue')
	plt.setp(bp['caps'][0], color='blue')
	plt.setp(bp['caps'][1], color='blue')
	plt.setp(bp['whiskers'][0], color='blue')
	plt.setp(bp['whiskers'][1], color='blue')
	#plt.setp(bp['fliers'][0], color='blue')
	#plt.setp(bp['fliers'][1], color='blue')
	plt.setp(bp['medians'][0], color='blue')

	plt.setp(bp['boxes'][1], color='red')
	plt.setp(bp['caps'][2], color='red')
	plt.setp(bp['caps'][3], color='red')
	plt.setp(bp['whiskers'][2], color='red')
	plt.setp(bp['whiskers'][3], color='red')
	#plt.setp(bp['fliers'][2], color='red')
	#plt.setp(bp['fliers'][3], color='red')
	plt.setp(bp['medians'][1], color='red')

	plt.setp(bp['boxes'][2], color='yellow')
	plt.setp(bp['caps'][3], color='yellow')
	plt.setp(bp['caps'][4], color='yellow')
	plt.setp(bp['whiskers'][3], color='yellow')
	plt.setp(bp['whiskers'][4], color='yellow')
	#plt.setp(bp['fliers'][3], color='yellow')
	#plt.setp(bp['fliers'][4], color='yellow')
	plt.setp(bp['medians'][2], color='yellow')

def main():
	sync = True
	series = ["SL", "PL-2t", "PL-10t"]
	#series = ["SL", "PL-10t"]
	
	workloads = ["YCSB-A", "YCSB-AW", "YCSB-AWL", "YCSB-B", "YCSB-D"]
	#workloads = ["YCSB-A"]
	ylimits = [450, 250, 325, 3750, 3750]

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
	labels = ["1", "10", "100", "1000"]
	xlabels = np.arange(len(labels))
	#xlabels = [-1.0, 1.5, 4.0, 6.5]

	#jump = 1
	#xlabels += jump
	#print(xlabels)
	factor = 1000
	spread = 0.5

	i = 0
	for w in workloads:
		plt.ylabel('Throughput (k commands)')
		#plt.ylim(top=ylimits[i])
		fig, ax = plt.subplots()
		ax.yaxis.grid(linestyle='--')

		ax.set_xticks(xlabels)
		#ax.set_xticks([-1.0, 1.5, 4.0, 6.5])

		ax.set_xticklabels(labels)
		#plt.xlim(-2,10)
		#fig.tight_layout()

		j = 0
		for s in series:
			ths = []
			for c in configs[s]:
				# divide 10^3 and cut first/last
				fn = ""
				if sync:
					fn += "sync/"
				fn += s + '/' + w + c
				func = ParseThroughput(fn)
				ths.append(np.divide(func, factor)[1:-1])

			stride = float(j) / 3
			print("stride:", stride)
			pos = [
				xlabels[0] - spread + stride,
				xlabels[1] + stride,
				xlabels[2] + spread + stride,
				xlabels[3] + (2*spread) + stride
			]

			# pos = []
			# if j == 0:
			# 	pos = xlabels - spread + stride
			# elif j == 1:
			# 	pos = xlabels + stride
			# else:
			# 	pos = xlabels + spread + stride
			
			print("pos:", pos)
			#print("ths:", ths)
			bp = plt.boxplot(ths, labels=labels, positions=pos, showfliers=False, widths=0.3)
			setBoxColors(bp)			
			j += 1

		#print("-------------------------------------------------------------\n")
		# draw temporary red and blue lines and use them to create a legend
		hB = plt.plot([1,1], 'b-')
		hR = plt.plot([1,1], 'r-')
		hY = plt.plot([1,1], 'y-')
		hK = plt.plot([1,1], 'k-')

		plt.legend((hB[0], hR[0], hY[0], hK[0]), ('PL-2t', 'PL-10t','SL'), loc='best')
		#plt.legend(loc='best')

		hB[0].set_visible(False)
		hR[0].set_visible(False)
		hY[0].set_visible(False)
		hK[0].set_visible(False)

		fn = 'graphs'
		if sync:
			fn += '-sync'
		fn += '/box-' + w
		print("finished running for", fn)
		plt.savefig(fn + '.png')
		plt.clf()
		i += 1


if __name__ == "__main__":
	main()
