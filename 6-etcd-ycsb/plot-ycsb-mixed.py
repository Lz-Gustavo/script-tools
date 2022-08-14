# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

exp_preffix = "49-"
graphs_folder = "graphs/mixed/"

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


def plot_exp_graph(workload: str, ylimit: float, exps: list):
    ave_config_formats = ["g-o", "b-D", "k-*", "r-^", "y-H"]
    p90_config_formats = ["g--o", "b--D", "k--*", "r--^", "y--H"]

    for exp in exps:
        plt.xlabel('Throughput (k cmds/s)')
        plt.ylabel('Latency (sec)')
        plt.grid(axis="y")

        plots = exp['plots']
        clients = exp['clients']
        i = 0
        for plot in plots:
            thrs, ave_lats, p90_lats = [], [], []
            for j in range(0, len(clients)):
                path = plot['path'] + '/' + workload + '/' + str(clients[j]) + 'clients'

                thr_fname = path + '/throughput.out'
                thr = get_array_from_file(thr_fname)

                lat_fname = path + '/ycsb-latency.out'
                lat = get_array_from_file(lat_fname)

                np_thr = np.array(thr)
                np_lat = np.array(lat)

                ave_thr = np.average(np_thr)
                ave_lat = np.average(np_lat)
                p90_lat = np.percentile(np_lat, 95)

                thrs.append(ave_thr)
                ave_lats.append(ave_lat)
                p90_lats.append(p90_lat)


            #thrs = np.divide(thrs, 1000)
            ave_lats = np.divide(np.array(ave_lats), 1000000000) # ns -> s
            p90_lats = np.divide(np.array(p90_lats), 1000000000) # ns -> s

            plt.ylim([0, ylimit])
            plt.plot(thrs, ave_lats, ave_config_formats[i], label=plot['name'])
            plt.plot(thrs, p90_lats, p90_config_formats[i])
            i += 1


        #plt.title(exp['name'] + '-' + workload)
        #plt.legend(loc='best')

        # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
        # top legend
        plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=5)
        
        # bottom legend 1
        #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
    
        # bottom legend 2
        #plt.legend(bbox_to_anchor=(1,0), loc="lower right", ncol=5)


        if not os.path.exists(graphs_folder):
            os.mkdir(graphs_folder)

        fname = graphs_folder + exp_preffix + exp['name'] + '-' + workload + '.png'
        #print("finished", fname, "...")
        plt.savefig(fname)
        plt.clf()


def main():
    #workloads = ["workloada", "workloadaprime", "workloadalatest", "workloadb", "workloadc", "workloadd"]
    workloads = ["workloada", "workloadaprime", "workloadalatest"]

    #ylimits = [0.6, 0.4, 0.4, 0.3, 0.3, 0.3]
    ylimits = [0.4, 0.3, 0.3]

    configs = [
        {
            "name": "batch300",
            "clients": [300, 450, 600, 750, 900, 1050],
            "plots": [
                {
                    "name": "SL",
                    "path": "exp/normal/sl-300"
                },
                {
                    "name": "PL",
                    "path": "exp/normal/pl-300"
                },
                {
                    "name": "PL-2disks",
                    "path": "exp/2disks/pl-300"

                },
                {
                    "name": "PL-4disks",
                    "path": "exp/4disks/pl-300"
                },
                {
                    "name": "PL-6disks",
                    "path": "exp/6disks/pl-300"
                }
            ]
        },
        {
            "name": "batch600",
            "clients": [600, 750, 900, 1050, 1200],
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
            "clients": [900, 1050, 1200, 1350, 1500],
            "plots": [
                {
                    "name": "SL-900",
                    "path": "exp/normal/sl-900"
                },
                {
                    "name": "PL-900",
                    "path": "exp/normal/pl-900"
                },
                {
                    "name": "PL-2disks",
                    "path": "exp/2disks/pl-900"
                },
                {
                    "name": "PL-4disks",
                    "path": "exp/4disks/pl-900"
                },
                {
                    "name": "PL-6disks",
                    "path": "exp/6disks/pl-900"
                }
            ]
        },
        {
            "name": "batch1200",
            "clients": [1200, 1350, 1500, 1650, 1800],
            "plots": [
                {
                    "name": "SL-1200",
                    "path": "exp/normal/sl-1200"
                },
                {
                    "name": "PL-1200",
                    "path": "exp/normal/pl-1200"
                },
                {
                    "name": "PL-2disks",
                    "path": "exp/2disks/pl-1200"
                },
                {
                    "name": "PL-4disks",
                    "path": "exp/4disks/pl-1200"
                },
                {
                    "name": "PL-6disks",
                    "path": "exp/6disks/pl-1200"
                }
            ]
        }
    ]

    for i in range(0, len(workloads)):
        plot_exp_graph(workloads[i], ylimits[i], configs)


if __name__ == "__main__":
    main()
