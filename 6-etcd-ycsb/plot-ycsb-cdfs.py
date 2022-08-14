# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys

exp_preffix = "49-"
graphs_folder = "graphs/cdf/"

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


# https://stackoverflow.com/questions/9378420/how-to-plot-cdf-in-matplotlib-in-python
# https://seaborn.pydata.org/generated/seaborn.kdeplot.html
def plot_exp_cdf_graph(workload: str, exps: list):
    colors = ['g', 'b', 'k', 'r', 'y']

    for exp in exps:
        plt.xlabel('Latency (sec)')
        plt.ylabel('Cumulative fraction')
        #plt.grid(axis="y")

        plots = exp['plots']
        clients = exp['clients']

        i = 0
        for plot in plots:
            path = plot['path'] + '/' + workload + '/' + str(clients) + 'clients'
            lat_fname = path + '/ycsb-latency.out'
            lat = get_array_from_file(lat_fname)

            np_lat = np.array(lat)
            lat = np.divide(np_lat, 1000000000) # ns -> s

            #plt.hist(lat, density=True, cumulative=True, label=plot['name'], histtype='step', color=colors[i])
            sns.kdeplot(data=lat, cumulative=True, label=plot['name'], color=colors[i])
            i += 1


        plt.title(exp['name'] + '-' + workload + '-' + str(clients) + 'clients')
        plt.legend(loc='best')

        if not os.path.exists(graphs_folder):
            os.mkdir(graphs_folder)

        fname = graphs_folder + exp_preffix + exp['name'] + '-' + workload + '.png'
        #print("finished", fname, "...")
        plt.savefig(fname)
        plt.clf()


def main():
    workloads = ["workloada", "workloadaprime", "workloadalatest"]
    configs = [
        {
            "name": "batch300",
            "clients": 750,
            "plots": [
                {
                    "name": "SL",
                    "path": "exp/normal/sl-600"
                },
                {
                    "name": "PL",
                    "path": "exp/normal/pl-600"
                },
                {
                    "name": "PL-2disks",
                    "path": "exp/2disks/pl-600"
                },
                {
                    "name": "PL-4disks",
                    "path": "exp/4disks/pl-600"
                },
                {
                    "name": "PL-6disks",
                    "path": "exp/6disks/pl-600"
                }
            ]
        },
        {
            "name": "batch600",
            "clients": 1050,
            "plots": [
                {
                    "name": "SL",
                    "path": "exp/normal/sl-600"
                },
                {
                    "name": "PL",
                    "path": "exp/normal/pl-600"
                },
                {
                    "name": "PL-2disks",
                    "path": "exp/2disks/pl-600"
                },
                {
                    "name": "PL-4disks",
                    "path": "exp/4disks/pl-600"
                },
                {
                    "name": "PL-6disks",
                    "path": "exp/6disks/pl-600"
                }
            ]
        },
        {
            "name": "batch900",
            "clients": 1200,
            "plots": [
                {
                    "name": "SL",
                    "path": "exp/normal/sl-600"
                },
                {
                    "name": "PL",
                    "path": "exp/normal/pl-600"
                },
                {
                    "name": "PL-2disks",
                    "path": "exp/2disks/pl-600"
                },
                {
                    "name": "PL-4disks",
                    "path": "exp/4disks/pl-600"
                },
                {
                    "name": "PL-6disks",
                    "path": "exp/6disks/pl-600"
                }
            ]
        },
        {
            "name": "batch1200",
            "clients": 1500,
            "plots": [
                {
                    "name": "SL",
                    "path": "exp/normal/sl-600"
                },
                {
                    "name": "PL",
                    "path": "exp/normal/pl-600"
                },
                {
                    "name": "PL-2disks",
                    "path": "exp/2disks/pl-600"
                },
                {
                    "name": "PL-4disks",
                    "path": "exp/4disks/pl-600"
                },
                {
                    "name": "PL-6disks",
                    "path": "exp/6disks/pl-600"
                }
            ]
        }
    ]

    for w in workloads:
        plot_exp_cdf_graph(w, configs)


if __name__ == "__main__":
    main()
