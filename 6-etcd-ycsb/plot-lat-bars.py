# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sys


exp_preffix = "59-"
graphs_folder = "graphs/lat-bars/"

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


def plot_comparison_bars(data, workloads, labels, xaxis, yaxis, filename):
    xlabels = np.arange(len(labels))
    width = 0.1

    fig, ax = plt.subplots()
    ax.yaxis.grid(linestyle='--')
    ax.set_ylim([0, 400])

    # TODO: iterate over labels and plot bars with right width
    ax.bar(xlabels - 3*width, data[0], width, label=workload_name_conversion[workloads[0]])
    ax.bar(xlabels - 2*width, data[1], width, label=workload_name_conversion[workloads[1]])
    ax.bar(xlabels - width, data[2], width, label=workload_name_conversion[workloads[2]])

    ax.bar(xlabels, data[3], width, label=workload_name_conversion[workloads[3]])
    ax.bar(xlabels + width, data[4], width, label=workload_name_conversion[workloads[4]])
    ax.bar(xlabels + 2*width, data[5], width, label=workload_name_conversion[workloads[5]])

    ax.set_ylabel(yaxis)
    ax.set_xlabel(xaxis)

    ax.set_xticks(xlabels)
    ax.set_xticklabels(labels)

    #plt.legend(loc='upper left')
    #plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=6)

    fig.tight_layout()
    plt.savefig(filename)


def plot_exp_graph(config: dict, workloads: list, batch_sizes: list):
    workload_data = []
    for i in range(0, len(workloads)):
        batch_data = []
        for j in range(0, len(batch_sizes)):
            path = config['path'] + '/' + config['prefix'] + batch_sizes[j] + '/' + workloads[i] + '/' + config['saturation'][j] + 'clients'

            lat_fname = path + '/ycsb-latency.out'
            lat = get_array_from_file(lat_fname)
            np_lat = np.array(lat)

            #lat_data = np.average(np_lat)
            lat_data = np.percentile(np_lat, 90)

            lat_data = lat_data / 1000000 # ns -> ms
            batch_data.append(lat_data)

        workload_data.append(batch_data)

    labels = ["300", "600", "900", "1200"]
    plot_comparison_bars(workload_data, workloads, labels, 'Batch Sizes', 'Average Latency (ms)', graphs_folder + config['name'] + '.png')


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
