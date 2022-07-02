# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

iterations=30
recov_fname="-recov-time.out"

output_config_results = True
output_dir="csv/"
output_csv_fname="RECOV-RESULTS.csv"

def ExtractData(filename):
    fd = open(filename)
    text = fd.readlines()
    fd.close()

    data = []
    for i in range(0, len(text)):
        data.append(int(text[i]))
    return data


def GenerateResultsCSV(names, workloads, ave_read_times, ave_receive_times, ave_apply_times, ave_total_times, stddev_read_times, stddev_receive_times, stddev_apply_times, stddev_total_times):
    column_names = ["Name", "Workload", "Read_time(ns)", "Read_std_dev", "Receive_time(ns)", "Receive_std_dev", "Apply_time(ns)", "Apply_std_dev", "Total_time(ns)", "Total_std_dev"]
    data = {
        column_names[0]: names,
        column_names[1]: workloads,
        column_names[2]: ave_read_times,
        column_names[3]: stddev_read_times,
        column_names[4]: ave_receive_times,
        column_names[5]: stddev_receive_times,
        column_names[6]: ave_apply_times,
        column_names[7]: stddev_apply_times,
        column_names[8]: ave_total_times,
        column_names[9]: stddev_total_times
    }
    df = pd.DataFrame(data, columns=column_names)
    print(df)
    df.to_csv(output_dir + output_csv_fname)


def GenerateConfigCSV(filename, np_read_times, np_receive_times, np_apply_times, np_total_times):
    # NOTE: ensure exact same size arrays for SL
    diff = len(np_receive_times) - len(np_read_times)
    np_read_times = np.append(np_read_times, np.zeros(diff))
    np_total_times = np.append(np_total_times, np.zeros(diff))

    column_names = ["Read_time(ns)", "Receive_time(ns)", "Apply_time(ns)", "Total_time(ns)"]
    data = {
        column_names[0]: np_read_times,
        column_names[1]: np_receive_times,
        column_names[2]: np_apply_times,
        column_names[3]: np_total_times
    }
    df = pd.DataFrame(data, columns=column_names)
    df.to_csv(output_dir + filename)


def main():
    configs = [
        {
            "name": "SL",
            "workload": "rand10",
            "path": "1-rand10/sl-1/"
        },
        {
            "name": "PL-300",
            "workload": "rand10",
            "path": "1-rand10/pl-300/"
        },
        {
            "name": "PL-600",
            "workload": "rand10",
            "path": "1-rand10/pl-600/"
        },
        {
            "name": "PL-900",
            "workload": "rand10",
            "path": "1-rand10/pl-900/"
        },
        {
            "name": "PL-1200",
            "workload": "rand10",
            "path": "1-rand10/pl-1200/"
        },
        {
            "name": "SL",
            "workload": "seq1M",
            "path": "2-seq1kk/sl-1/"
        },
        {
            "name": "PL-300",
            "workload": "seq1M",
            "path": "2-seq1kk/pl-300/"
        },
        {
            "name": "PL-600",
            "workload": "seq1M",
            "path": "2-seq1kk/pl-600/"
        },
        {
            "name": "PL-900",
            "workload": "seq1M",
            "path": "2-seq1kk/pl-900/"
        },
        {
            "name": "PL-1200",
            "workload": "seq1M",
            "path": "2-seq1kk/pl-1200/"
        },
        {
            "name": "SL",
            "workload": "rand500",
            "path": "3-rand500/sl-1/"
        },
        {
            "name": "PL-300",
            "workload": "rand500",
            "path": "3-rand500/pl-300/"
        },
        {
            "name": "PL-600",
            "workload": "rand500",
            "path": "3-rand500/pl-600/"
        },
        {
            "name": "PL-900",
            "workload": "rand500",
            "path": "3-rand500/pl-900/"
        },
        {
            "name": "PL-1200",
            "workload": "rand500",
            "path": "3-rand500/pl-1200/"
        }
    ]

    names = []
    workloads = []
    ave_read_times = []
    ave_receive_times = []
    ave_apply_times = []
    ave_total_times = []
    stddev_read_times = []
    stddev_receive_times = []
    stddev_apply_times = []
    stddev_total_times = []

    for c in configs:
        names.append(c["name"])
        workloads.append(c["workload"])

        path = c["path"]
        if path == "":
            print("path not informed")
            return

        read_times_ns = []
        receive_times_ns = []
        apply_times_ns = []
        total_times_ns = []
        for i in range(0, iterations):
            fn = path + "/" + str(i) + recov_fname
            data = ExtractData(fn)
            if len(data) < 4:
                print("incomplete data returned")
                return

            read_times_ns.append(data[1] - data[0])
            total_times_ns.append(data[len(data)-1] - data[0])

            if c["name"] == "SL":
                for j in range(1, len(data)-2, 2):
                    receive_times_ns.append(data[j+1] - data[j])
                    apply_times_ns.append(data[j+2] - data[j+1])

            else:
                receive_times_ns.append(data[2] - data[1])
                apply_times_ns.append(data[3] - data[2])

        np_read_times = np.array(read_times_ns)
        np_receive_times = np.array(receive_times_ns)
        np_apply_times = np.array(apply_times_ns)
        np_total_times = np.array(total_times_ns)

        ave_read_times.append(np.mean(np_read_times))
        ave_receive_times.append(np.mean(np_receive_times))
        ave_apply_times.append(np.mean(np_apply_times))
        ave_total_times.append(np.mean(np_total_times))

        stddev_read_times.append(np.std(np_read_times))
        stddev_receive_times.append(np.std(np_receive_times))
        stddev_apply_times.append(np.std(np_apply_times))
        stddev_total_times.append(np.std(np_total_times))

        if output_config_results:
            fn = c["name"] + "-" + c["workload"] + ".csv"
            GenerateConfigCSV(fn, np_read_times, np_receive_times, np_apply_times, np_total_times)

    GenerateResultsCSV(names, workloads,
        ave_read_times,
        ave_receive_times,
        ave_apply_times,
        ave_total_times,
        stddev_read_times,
        stddev_receive_times,
        stddev_apply_times,
        stddev_total_times
    )

if __name__ == "__main__":
    main()
