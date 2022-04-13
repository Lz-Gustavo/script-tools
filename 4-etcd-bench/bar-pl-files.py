# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

sl_command_count = 100000
sl_byte_size = 64000000

root_folder = "."
sub_folder = "1"


def ExtractData(filename):
    fd = open(filename)
    text = fd.readlines()
    fd.close()

    data = []
    for i in range(0, len(text)):
        data.append(int(text[i]))
    return data


def Plot(data, workloads, labels, xaxis, yaxis, filename):
    xlabels = np.arange(len(labels))
    width = 0.1

    fig, ax = plt.subplots()
    ax.yaxis.grid(linestyle='--')

    # TODO: iterate over labels and plot bars with right width
    ax.bar(xlabels - (width/2), data[0], width, label=workloads[0])
    ax.bar(xlabels + (width/2), data[1], width, label=workloads[1])

    ax.set_ylabel(yaxis)
    ax.set_xlabel(xaxis)

    ax.set_xticks(xlabels)
    ax.set_xticklabels(labels)
    fig.tight_layout()

    plt.legend(loc='best')
    plt.savefig(filename)


def main():
    workloads = ["Seq1kk", "Rand10"]
    configs = [
        {
            "name": "PL-1",
            "paths": [
                root_folder + "/" + sub_folder + "/pl-1",
                root_folder + "/" + sub_folder + "/pl-1-10keys"
            ],
            "count_fname": "logcounts.out",
            "size_fname": "logsize.out"
        },
        {
            "name": "PL-10",
            "paths": [
                root_folder + "/" + sub_folder + "/pl-10",
                root_folder + "/" + sub_folder + "/pl-10-10keys"
            ],
            "count_fname": "logcounts.out",
            "size_fname": "logsize.out"
        },
        {
            "name": "PL-100",
            "paths": [
                root_folder + "/" + sub_folder + "/pl-100",
                root_folder + "/" + sub_folder + "/pl-100-10keys"
            ],
            "count_fname": "logcounts.out",
            "size_fname": "logsize.out"
        },
        {
            "name": "PL-500",
            "paths": [
                root_folder + "/" + sub_folder + "/pl-500",
                root_folder + "/" + sub_folder + "/pl-500-10keys"
            ],
            "count_fname": "logcounts.out",
            "size_fname": "logsize.out"
        }
    ]

    labels = []
    workload_counts = []
    workload_sizes = []
    for w in workloads:
        workload_counts.append([])
        workload_sizes.append([])

    for c in configs:
        paths = c["paths"]
        if len(paths) != len(workloads):
            print("paths should have same len as workloads")
            return

        labels.append(c["name"])
        for i in range(0, len(paths)):
            # command counts
            count_fname = paths[i] + "/" + c["count_fname"]
            data = ExtractData(count_fname)

            arr = np.array(data)
            diff =  1 - (np.sum(arr) / sl_command_count)
            workload_counts[i].append(diff)


            # logsize
            size_fname = paths[i] + "/" + c["size_fname"]
            data = ExtractData(size_fname)[0]

            diff = 1 - float(data / sl_byte_size)
            #print(diff)
            workload_sizes[i].append(diff)

    Plot(workload_counts, workloads, labels, 'Configurations', 'Command Reduction', 'test-counts.png')
    Plot(workload_sizes, workloads, labels, 'Configurations', 'Log Size Reduction', 'test-sizes.png')


if __name__ == "__main__":
    main()
