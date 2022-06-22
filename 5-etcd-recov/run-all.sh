#!/bin/bash

recov=/media/disk1/beelog
#recov=/media/disk1/etcd/wal

cur=$(pwd)
experiments=(
    "1-rand10/pl-300"
    "1-rand10/pl-600"
    "1-rand10/pl-900"
    "1-rand10/pl-1200"
    #"1-rand10/sl-1"

    "2-seq1kk/pl-300"
    "2-seq1kk/pl-600"
    "2-seq1kk/pl-900"
    "2-seq1kk/pl-1200"
    #"2-seq1kk/sl-1"

    "3-rand500/pl-300"
    "3-rand500/pl-600"
    "3-rand500/pl-900"
    "3-rand500/pl-1200"
    #"3-rand500/sl-1"
)

for exp in ${experiments[*]}; do
    echo "running ${exp}..."
    /bin/bash ${cur}/recov-bench.sh ${recov} ${cur}/${exp}/

    sleep 10s
done

echo "finished!"
