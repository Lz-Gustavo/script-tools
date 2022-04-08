#!/bin/bash

user=user

rootFolder=$(pwd)
nodeScript=${rootFolder}/run-singlenode.sh

etcdHostname="10.10.1.2"
measurepath=/tmp

keySize=8
valueSize=128

numDiffKeys=1000000 # 1kk
conns=1

numOps=(8000 20000 25000 50000 50000 50000 50000 50000 50000 50000)
clients=(100 300 500 1000 1500 2000 5000 10000 15000 20000)
operations=("put" "range")

echo "running..."
for op in ${operations[*]}; do
    for (( i = 0; i < ${#clients[*]}; i++ )); do
        cl=${clients[$i]}
        n=${numOps[$i]}

        echo "launching server on remote"
        ssh root@${etcdHostname} "${nodeScript}" &
        sleep 5s

        echo "executing for $cl concurrent clients"
        if [[ ${op} -eq "put" ]]; then
            /users/${user}/go/bin/benchmark --endpoints=${etcdHostname}:2379 --target-leader --conns=${conns} --clients=${cl} \
                put --key-space-size=${numDiffKeys} --key-size=${keySize} --precise --sequential-keys --total=${n} --val-size=${valueSize} \
                > ${measurepath}/bench.out

        else
            /users/${user}/go/bin/benchmark --endpoints=${etcdHostname}:2379 --target-leader --conns=${conns} --clients=${cl} \
                range TODO --precise --consistency=l --total=${n} \
                > ${measurepath}/bench.out
        fi

        echo "killing server on remote and copying results"
        mkdir -p ${rootFolder}/${op}/${cl}c
        ssh root@${etcdHostname} "killall etcd -u root -w; mv ${measurepath}/*.out ${rootFolder}/${op}/${cl}c/"

        echo "finished ${cl} clients..."; echo ""
    done
done

echo "finished!"

