#!/bin/bash

cur=$(pwd)
experiments=(
    "1/pl-1"
    "1/sl-1"
    "1/pl-10"
    "1/sl-10"
    "1/pl-100"
    "1/sl-100"
)

for exp in ${experiments[*]}; do
    echo "running ${exp}..."
    cd ${cur}/${exp}/
    /bin/bash ssh-runEtcdBenchmark.sh

    /bin/bash getBenchData.sh .
    sleep 5s
done

echo "finished!"
