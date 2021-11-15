# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import matplotlib.pyplot as plt
import sys

upperRangeLimit = 60
file_id = "logger.out"
kv = False

def GetMetrics(filename, firstIndex, offset):
    """
    	1: net bytes_recv
        2: net bytes_sent
        3: io bytes_read
        4: io bytes_write
    """
    fd = open(filename)
    text = fd.readlines()
    fd.close()

    data = []

    i = firstIndex
    while i < len(text):
        data.append(int(text[i]))
        i += offset

    return data

def main():

    if kv:
        net_bytes_recv = GetMetrics("kv/kv-counters-"+file_id, 1, 5)
        net_bytes_sent = GetMetrics("kv/kv-counters-"+file_id, 2, 5)
        io_bytes_read = GetMetrics("kv/kv-counters-"+file_id, 3, 5)
        io_bytes_write = GetMetrics("kv/kv-counters-"+file_id, 4, 5)
        
    else:
        net_bytes_recv = GetMetrics("disk/disk-counters-"+file_id, 1, 5)
        net_bytes_sent = GetMetrics("disk/disk-counters-"+file_id, 2, 5)
        io_bytes_read = GetMetrics("disk/disk-counters-"+file_id, 3, 5)
        io_bytes_write = GetMetrics("disk/disk-counters-"+file_id, 4, 5)

    pointsInTime = range(0, len(net_bytes_recv))

    plt.xlabel('Time (s)')
    plt.ylabel('Usage (Bytes)')

    ax = plt.axes()
    ax.yaxis.grid(linestyle='--')

    # Plot axis
    #plt.plot(pointsInTime, net_bytes_recv, "y--", label="net bytes recv")
    #plt.plot(pointsInTime, net_bytes_sent, "b-^", label="net bytes sent")
    plt.plot(pointsInTime, io_bytes_read, "r-o", label="io bytes read")
    plt.plot(pointsInTime, io_bytes_write, "g-*", label="io bytes write")


    plt.legend(loc='best')

    if kv:
        plt.savefig(file_id+'-kv.png')
    else:
        plt.savefig(file_id+'-disk.png')

if __name__ == "__main__":
    main()
