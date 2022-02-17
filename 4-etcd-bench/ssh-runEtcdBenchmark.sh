#!/bin/bash

user=user

rootFolder=/users/${user}/experiment
nodeScript=${rootFolder}/run-singlenode.sh

etcdHostname="10.10.1.2"
measurepath=/tmp

keySize=128
valueSize=512
numDiffKeys=1000000 # 1kk
conns=20

numOps=(3000 30000 200000 500000 500000)
clients=(10 100 300 500 1000)
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
        mv ${measurepath}/*.out ${rootFolder}/${op}/${cl}c/

        echo "finished ${cl} clients..."; echo ""
    done
done

echo "finished!"
