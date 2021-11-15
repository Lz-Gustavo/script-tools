import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main():
	data = pd.read_csv('data-analysis-full.csv')
	print(data.head())

	workloads = ["YCSB-A", "YCSB-AW", "YCSB-AWL", "YCSB-B", "YCSB-D"]
	work_dfs = []

	work_dfs_sync = []
	work_dfs_sync_thousand = []

	for w in workloads:
		df = data[data['workload'] == w]
		work_dfs.append(df[df['sync'] == False])
		
		sync = df[df['sync'] == True]
		sync_n = sync[sync['interval'] != 1000]
		work_dfs_sync.append(sync_n)

		sync_thousand = sync[sync['interval'] == 1000]
		work_dfs_sync_thousand.append(sync_thousand)


	# plot assync scenarios
	# i = 0
	# for wd in work_dfs:
	# 	box = sns.boxplot(y='thr', x='interval', data=wd, palette="colorblind", hue='config')
	# 	fig = box.get_figure()
	# 	fig.savefig("seaborn-workloads/" + workloads[i] + ".png")
	# 	plt.clf()
	# 	i += 1

	i = 0
	for wd in work_dfs_sync:
		box = sns.boxplot(y='thr', x='interval', data=wd, palette="colorblind", hue='config')
		fig = box.get_figure()
		fig.savefig("seaborn-workloads/" + workloads[i] + "-sync.png")
		plt.clf()
		i += 1

	i = 0
	for wd in work_dfs_sync_thousand:
		box = sns.boxplot(y='thr', x='workload', data=wd, palette="colorblind", hue='config')	
		fig = box.get_figure()
		fig.savefig("seaborn-workloads/" + workloads[i] + "-sync.png")
		plt.clf()
		i += 1


if __name__ == "__main__":
	main()