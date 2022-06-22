# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

iterations=10
recov_file_name="-recov-time.out"


def ExtractData(filename):
    fd = open(filename)
    text = fd.readlines()
    fd.close()

    data = []
    for i in range(0, len(text)):
        data.append(int(text[i]))
    return data


def main():
    configs = [
        {
            "name": "PL-300",
            "workload": "rand10",
            "path": "/path/to/files"
        },
        {
            "name": "PL-600",
            "workload": "rand10",
            "path": "/path/to/files"
        }
    ]

    names = []
    workloads = []
    ave_read_times = []
    ave_receive_times = []
    ave_apply_times = []
    stddev_read_times = []
    stddev_receive_times = []
    stddev_apply_times = []

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
        for i in range(0, iterations):
            fn = path + "/" + str(i) + recov_file_name
            data = ExtractData(fn)
            if len(data) != 4:
                print("incomplete data returned")
                return

            read_times_ns.append(data[1] - data[0])
            receive_times_ns.append(data[2] - data[1])
            apply_times_ns.append(data[3] - data[2])

        np_read_times = np.array(read_times_ns)
        np_receive_times = np.array(receive_times_ns)
        np_apply_times = np.array(apply_times_ns)

        ave_read_times.append(np.mean(np_read_times))
        ave_receive_times.append(np.mean(np_receive_times))
        ave_apply_times.append(np.mean(np_apply_times))

        stddev_read_times.append(np.std(np_read_times))
        stddev_receive_times.append(np.std(np_receive_times))
        stddev_apply_times.append(np.std(np_apply_times))

    column_names = ["Name", "Workload", "Read_time(ns)", "Read_std_dev", "Receive_time(ns)", "Receive_std_dev", "Apply_time(ns)", "Apply_std_dev"]
    data = {
        column_names[0]: names,
        column_names[1]: workloads,
        column_names[2]: ave_read_times,
        column_names[3]: stddev_read_times,
        column_names[4]: ave_receive_times,
        column_names[5]: stddev_receive_times,
        column_names[6]: ave_apply_times,
        column_names[7]: stddev_apply_times
    }

    df = pd.DataFrame(data, columns=column_names)
    print(df)

    # TODO: export df to csv file


if __name__ == "__main__":
    main()
