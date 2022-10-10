# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys


exp_preffix = "59-"
graphs_folder = "graphs/lat-boxplot/"

workload_name_conversion = {
    "workloada": "A",
    "workloadaprime": "AW",
    "workloadalatest": "AWL",
    "workloadb": "B",
    "workloadc": "C",
    "workloadd": "D"
}

def get_array_from_file(filename: str):
    try:
        fd = open(filename)
        text = fd.readlines()
        fd.close()

        data = []
        for ln in text:
            if ln == '\n':
                continue
            n = float(ln)
            if n > 0:
                data.append(n)
        return data

    except:
        print('could not read file:', filename)
        sys.exit()


def plot_boxplot(df, title, xaxis, yaxis, filename):
    fig, ax = plt.subplots()
    ax.yaxis.grid(linestyle='--')

    box = sns.boxplot(y='latency', x='workloads', data=df, palette="colorblind", hue='batch', showfliers=False)		
    box.tick_params(labelsize=11)

    fig = box.get_figure()
    plt.ylabel(yaxis, {'size':'13'})
    plt.xlabel(xaxis, {'size':'13'})
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=6, fancybox=True, prop={'size':12})

    fig.savefig(filename)
    plt.clf()


def plot_exp_graph(config: dict, workloads: list, batch_sizes: list):
    data_col = []
    workload_col = []
    batch_col = []

    for i in range(0, len(workloads)):
        for j in range(0, len(batch_sizes)):
            path = config['path'] + '/' + config['prefix'] + batch_sizes[j] + '/' + workloads[i] + '/' + config['saturation'][j] + 'clients'
            lat_fname = path + '/ycsb-latency.out'
            lat = get_array_from_file(lat_fname)
            np_lat = np.array(lat)
            np_lat = np.divide(np_lat, 1000000)

            for k in np_lat:
                workload_col.append(workload_name_conversion[workloads[i]])
                batch_col.append(int(batch_sizes[j]))
                data_col.append(k)

    data_dict = {
        "workloads": workload_col,
        "batch": batch_col,
        "latency": data_col,
    }

    df = pd.DataFrame(data_dict)
    plot_boxplot(df, '', 'YCSB workloads', 'Latency (ms)', graphs_folder + config['name'] + '.png')


def main():
    workloads = ["workloada", "workloadalatest", "workloadaprime", "workloadb", "workloadc", "workloadd"]
    batch_sizes = ["300", "600", "900", "1200"]
    configs = [
        {
            "name": "SL",
            "path": "exp/normal",
            "prefix": "sl-",
            "saturation": ["750", "1050", "1200", "1500"]
        },
        {
            "name": "PL",
            "path": "exp/normal",
            "prefix": "pl-",
            "saturation": ["750", "1050", "1200", "1500"]
        },
        {
            "name": "PL-2disks",
            "path": "exp/2disks",
            "prefix": "pl-",
            "saturation": ["750", "1050", "1200", "1500"]
        },
        {
            "name": "PL-4disks",
            "path": "exp/4disks",
            "prefix": "pl-",
            "saturation": ["750", "1050", "1200", "1500"]
        },
        {
            "name": "PL-6disks",
            "path": "exp/6disks",
            "prefix": "pl-",
            "saturation": ["750", "1050", "1200", "1500"]
        }
    ]

    for cfg in configs:
        plot_exp_graph(cfg, workloads, batch_sizes)


if __name__ == "__main__":
    main()
