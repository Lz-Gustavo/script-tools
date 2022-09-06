#!/bin/bash

# The benchmark run over two different configurations...
isIncreasingByTargetThroughput=false

user=gustavo
ycsbPath=/users/${user}/go/src/go-ycsb/

etcdHostname="localhost"
sleepDurationSec=10

rootFolder=$(pwd)
nodeScript=run-singlenode.sh

logsDiskPath=/media/disk1

#walsLocation=${logsDiskPath}/etcd/wal
walsLocation=${logsDiskPath}/beelog

outputTarName=logs.tar.gz

workloads=("workloada" "workloadaprime" "workloadalatest" "workloadb" "workloadc" "workloadd")
numDiffKeys=1000000 # 1kk
iterations=1

main() {
    if [[ $# -lt 1 ]]; then
        echo "using ${rootFolder} value for 'rootFolder'"
    else
        echo "using $1 as value for 'rootFolder'"
        rootFolder=$1
    fi

    echo "running..."
    for (( i = 0; i < ${iterations}; i++ )); do
        if [[ "${isIncreasingByTargetThroughput}" == "true" ]]; then
            increaseByTargetThroughput $i
        else
            increaseByClientCount $i
        fi
    done
    echo "finished!"
}

increaseByTargetThroughput() {
    local i=$1
    echo "#${i}: started target thr iteration"

    # must be at least >= BATCH_SIZE
    numClients=1500

    # unique size arrays
    numOps=(100000)
    targetThrs=(9000)

    for workload in ${workloads[*]}; do
        for (( j = 0; j < ${#targetThrs[*]}; j++ )); do
            t=${targetThrs[$j]}
            n=${numOps[$j]}

            echo "#${i}-${workload}/${j}: launching local server"
            ${rootFolder}/${nodeScript} &
            sleep ${sleepDurationSec}s

            echo "#${i}-${workload}/${j}: executing $t target throughput"
            ${ycsbPath}/bin/go-ycsb run etcd -P ${ycsbPath}/workloads/${workload} -p target=${t} -p threadcount=${numClients} -p recordcount=${numDiffKeys} -p operationcount=${n} -p etcd.hostname=${etcdHostname} -p etcd.thinktime=0

            echo "#${i}-${workload}/${j}: killing local server and copying results"
            mkdir -p ${rootFolder}/${workload}/${t}thr/

            killall etcd -u root -w
            tar -czvf ${logsDiskPath}/${outputTarName} ${walsLocation}; mv ${logsDiskPath}/${outputTarName} ${rootFolder}/${workload}/${t}thr/
        done
    done
    echo "#${i}: finished target thr iteration"; echo ""
}

increaseByClientCount() {
    local i=$1
    echo "#${i}: started clients iteration"

    targetThroughput=20000

    numOps=(100000)
    clients=(750)

    for workload in ${workloads[*]}; do
        for (( j = 0; j < ${#clients[*]}; j++ )); do
            cl=${clients[$j]}
            n=${numOps[$j]}

            echo "#${i}-${workload}/${j}: launching local server"
            ${rootFolder}/${nodeScript} &
            sleep ${sleepDurationSec}s

            echo "#${i}-${workload}/${j}: executing for $cl clients"
            ${ycsbPath}/bin/go-ycsb run etcd -P ${ycsbPath}/workloads/${workload} -p target=${targetThroughput} -p threadcount=${cl} -p recordcount=${numDiffKeys} -p operationcount=${n} -p etcd.hostname=${etcdHostname} -p etcd.thinktime=0

            echo "#${i}-${workload}/${j}: killing local server and copying results"
            mkdir -p ${rootFolder}/${workload}/${cl}clients/

            killall etcd -u root -w
            tar -czvf ${logsDiskPath}/${outputTarName} ${walsLocation}; mv ${logsDiskPath}/${outputTarName} ${rootFolder}/${workload}/${cl}clients/
        done
    done
    echo "#${i}: finished clients iteration"; echo ""
}

main "$@"; exit
