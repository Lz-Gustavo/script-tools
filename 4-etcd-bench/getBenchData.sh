#!/bin/bash

defaultFolder=/users/${user}/experiment
rootFolder=""

if [[ $# -ne 1 ]]; then
	echo "using defualt value for 'rootFolder'"
	rootFolder=defaultFolder

else
    echo "using $1 as value for 'rootFolder'"
    rootFolder=$1
fi

clients=(100 300 500 1000 1500 2000 5000 10000 15000 20000)
operations=("put" "range")

echo "running..."
for op in ${operations[*]}; do
    latFn=${rootFolder}/${op}-latency.out
    thrFn=${rootFolder}/${op}-throughput.out

    > ${latFn} && > ${thrFn}

    for (( i = 0; i < ${#clients[*]}; i++ )); do
        cl=${clients[$i]}
        fn=${rootFolder}/${op}/${cl}c/bench.out

        cat ${fn} | grep Average: | sed 's/Average://g; s/secs.//g; s/[[:space:]]//g' >> ${rootFolder}/${op}-latency.out
        cat ${fn} | grep Requests/sec: | sed 's/Requests\/sec://g; s/[[:space:]]//g' >> ${rootFolder}/${op}-throughput.out
    done
done
echo "finished!"
