import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def set_plot_style():
	plt.ylabel('Throughput')
	plt.xlabel('')
	#plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, fancybox=True)


def main():
	sns.set_style("whitegrid")
	data = pd.read_csv('data-analysis-full.csv')
	#print(data.head())

	intervals = [1, 10, 100, 1000]
	work_dfs_sync = []

	for it in intervals:
		df = data[data['interval'] == it]
		work_dfs_sync.append(df[df['sync'] == True])

	i = 0
	for wd in work_dfs_sync:
		box = sns.boxplot(y='thr', x='workload', data=wd, palette="colorblind", hue='config', showfliers=False)
		#box = sns.boxplot(y='thr', x='workload', data=wd, palette="colorblind", hue='config')
		
		fig = box.get_figure()
		set_plot_style()
		fig.savefig("seaborn/" + str(intervals[i]) + "-sync.png")
		plt.clf()
		i += 1


if __name__ == "__main__":
	main()