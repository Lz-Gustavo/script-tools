# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

exp_preffix = "48-"

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


def plot_exp_graph(workload: str, exps: list):
    config_formats = ["g-o", "b-D", "k-*", "r-^", "y-H"]

    for exp in exps:
        plt.xlabel('Throughput (k cmds/s)')
        plt.ylabel('Latency (sec)')
        plt.grid(axis="y")

        plots = exp['plots']
        i = 0
        for plot in plots:

            clients = plot['clients']
            thrs, lats = [], []
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
                thrs.append(ave_thr)
                lats.append(ave_lat)


            #thrs = np.divide(thrs, 1000)
            lats = np.divide(np.array(lats), 1000000000) # ns -> s
            plt.plot(thrs, lats, config_formats[i], label=plot['name'])
            i += 1


        plt.title(exp['name'] + '-' + workload)
        plt.legend(loc='best')

        if not os.path.exists('graphs/'):
            os.mkdir('graphs/')

        fname = 'graphs/' + exp_preffix + exp['name'] + '-' + workload + '.png'
        #print("finished", fname, "...")
        plt.savefig(fname)
        plt.clf()


def main():
    workloads = ["workloada", "workloadaprime", "workloadalatest", "workloadb", "workloadc", "workloadd"]
    configs = [
        {
            "name": "batch300",
            "plots": [
                {
                    "name": "SL-300",
                    "path": "exp/normal/sl-300",
                    "clients": [400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]	
                },
                {
                    "name": "PL-300",
                    "path": "exp/normal/pl-300",
                    "clients": [400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
                }
            ]
        },
        {
            "name": "batch600",
            "plots": [
                {
                    "name": "SL-600",
                    "path": "exp/normal/sl-600",
                    "clients": [600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200]
                },
                {
                    "name": "PL-600",
                    "path": "exp/normal/pl-600",
                    "clients": [600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200]
                }
            ]
        },
        {
            "name": "batch900",
            "plots": [
                {
                    "name": "SL-900",
                    "path": "exp/normal/sl-900",
                    "clients": [1000, 1200, 1400, 1600, 1800, 2000, 2200]	
                },
                {
                    "name": "PL-900",
                    "path": "exp/normal/pl-900",
                    "clients": [1000, 1200, 1400, 1600, 1800, 2000, 2200]	
                }
            ]
        },
        {
            "name": "batch1200",
            "plots": [
                {
                    "name": "SL-1200",
                    "path": "exp/normal/sl-1200",
                    "clients": [1200, 1400, 1600, 1800, 2000, 2200, 2400]	
                },
                {
                    "name": "PL-1200",
                    "path": "exp/normal/pl-1200",
                    "clients": [1200, 1400, 1600, 1800, 2000, 2200, 2400]
                }
            ]
        }
    ]

    for w in workloads:
        plot_exp_graph(w, configs)


if __name__ == "__main__":
    main()
