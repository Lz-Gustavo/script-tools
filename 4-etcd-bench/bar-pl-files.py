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


def PlotBar(data, workloads, labels, xaxis, yaxis, filename):
    xlabels = np.arange(len(labels))
    width = 0.2

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

    plt.legend(loc='upper left')
    plt.savefig(filename)


def PlotBoxplot(data, labels, xaxis, yaxis, filename):
    fig, ax = plt.subplots()
    ax.yaxis.grid(linestyle='--')

    ax.boxplot(data)
    ax.set_ylabel(yaxis)
    ax.set_xlabel(xaxis)

    ax.set_xticklabels(labels)
    fig.tight_layout()

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
            "size_fname": "logsize.out",
            "batch_fname": "logbatches.out"
        },
        {
            "name": "PL-10",
            "paths": [
                root_folder + "/" + sub_folder + "/pl-10",
                root_folder + "/" + sub_folder + "/pl-10-10keys"
            ],
            "count_fname": "logcounts.out",
            "size_fname": "logsize.out",
            "batch_fname": "logbatches.out"
        },
        {
            "name": "PL-100",
            "paths": [
                root_folder + "/" + sub_folder + "/pl-100",
                root_folder + "/" + sub_folder + "/pl-100-10keys"
            ],
            "count_fname": "logcounts.out",
            "size_fname": "logsize.out",
            "batch_fname": "logbatches.out"
        },
        {
            "name": "PL-500",
            "paths": [
                root_folder + "/" + sub_folder + "/pl-500",
                root_folder + "/" + sub_folder + "/pl-500-10keys"
            ],
            "count_fname": "logcounts.out",
            "size_fname": "logsize.out",
            "batch_fname": "logbatches.out"
        }
    ]

    labels = []
    workload_counts = []
    workload_sizes = []
    workload_batches = []
    for w in workloads:
        workload_counts.append([])
        workload_sizes.append([])
        workload_batches.append([])

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
            workload_sizes[i].append(diff)

            # batches
            batch_fname = paths[i] + "/" + c["batch_fname"]
            data = ExtractData(batch_fname)
            workload_batches[i].append(data)

    PlotBar(workload_counts, workloads, labels, 'Configurations', 'Command Reduction', 'log-counts.png')
    PlotBar(workload_sizes, workloads, labels, 'Configurations', 'Log Size Reduction', 'log-sizes.png')
    for i in range(0, len(workloads)):
        PlotBoxplot(workload_batches[i], labels, 'Configurations', 'Log Batch Sizes', 'log-batches-' + workloads[i] + '.png')


if __name__ == "__main__":
    main()
