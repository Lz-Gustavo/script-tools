#!/bin/bash

# Controls wheter commands must be executed through ssh to
# 'etcdHostname' or not.
isRemoteExecution=true

# The benchmark run over two different configurations...
isIncreasingByTargetThroughput=true

user=user
ycsbPath=/users/${user}/go/src/go-ycsb/

etcdHostname="10.10.1.2"
sleepDurationSec=10

rootFolder=$(pwd)
serverMeasurePath=/tmp
latFilename=/tmp/ycsb-latency.out
nodeScript=run-singlenode.sh

workloads=("workloadaprime")
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

    numClients=100

    # unique size arrays
    numOps=(20000 30000 40000 50000 60000 70000 80000)
    targetThrs=(1000 4000 7000 10000 13000 16000 19000)

    for workload in ${workloads[*]}; do
        for (( j = 0; j < ${#targetThrs[*]}; j++ )); do
            t=${targetThrs[$j]}
            n=${numOps[$j]}

            if [[ "${isRemoteExecution}" == "true" ]]; then
                echo "#${i}-${workload}/${j}: launching server on remote"
                ssh root@${etcdHostname} "${rootFolder}/${nodeScript}" &
                sleep ${sleepDurationSec}s

                echo "#${i}-${workload}/${j}: executing $t target throughput"
                ${ycsbPath}/bin/go-ycsb run etcd -P ${ycsbPath}/workloads/${workload} -p target=${t} -p threadcount=${numClients} -p recordcount=${numDiffKeys} -p operationcount=${n} -p etcd.hostname=${etcdHostname} -p etcd.latfilename=${latFilename}

                echo "#${i}-${workload}/${j}: killing server on remote and copying results"
                mkdir -p ${rootFolder}/${t}thr/
                mv -f ${latFilename} ${rootFolder}/${t}thr/
                ssh root@${etcdHostname} "killall etcd -u root -w; mv -f ${serverMeasurePath}/*.out ${rootFolder}/${t}thr/"

            else
                echo "#${i}-${workload}/${j}: launching local server"
                ${rootFolder}/${nodeScript} &
                sleep ${sleepDurationSec}s

                echo "#${i}-${workload}/${j}: executing $t target throughput"
                ${ycsbPath}/bin/go-ycsb run etcd -P ${ycsbPath}/workloads/${workload} -p target=${t} -p threadcount=${numClients} -p recordcount=${numDiffKeys} -p operationcount=${n} -p etcd.hostname=${etcdHostname} -p etcd.latfilename=${latFilename}

                echo "#${i}-${workload}/${j}: killing local server and copying results"
                mkdir -p ${rootFolder}/${t}thr/
                mv -f ${latFilename} ${rootFolder}/${t}thr/
                killall etcd -u root -w; mv -f ${serverMeasurePath}/*.out ${rootFolder}/${t}thr/
            fi
        done
    done
    echo "#${i}: finished target thr iteration"; echo ""
}

increaseByClientCount() {
    local i=$1
    echo "#${i}: started clients iteration"

    targetThroughput=20000

    # unique size arrays
    numOps=(20000 30000 40000 50000 60000 70000 80000)
    clients=(400 600 800 1000 1200 1400 1600)

    for workload in ${workloads[*]}; do
        for (( j = 0; j < ${#clients[*]}; j++ )); do
            cl=${clients[$j]}
            n=${numOps[$j]}

            if [[ "${isRemoteExecution}" == "true" ]]; then
                echo "#${i}-${workload}/${j}: launching server on remote"
                ssh root@${etcdHostname} "${rootFolder}/${nodeScript}" &
                sleep ${sleepDurationSec}s

                echo "#${i}-${workload}/${j}: executing for $cl clients"
                ${ycsbPath}/bin/go-ycsb run etcd -P ${ycsbPath}/workloads/${workload} -p target=${targetThroughput} -p threadcount=${cl} -p recordcount=${numDiffKeys} -p operationcount=${n} -p etcd.hostname=${etcdHostname} -p etcd.latfilename=${latFilename}

                echo "#${i}-${workload}/${j}: killing server on remote and copying results"
                mkdir -p ${rootFolder}/${t}thr/
                mv -f ${latFilename} ${rootFolder}/${t}thr/
                ssh root@${etcdHostname} "killall etcd -u root -w; mv -f ${serverMeasurePath}/*.out ${rootFolder}/${t}thr/"

            else
                echo "#${i}-${workload}/${j}: launching local server"
                ${rootFolder}/${nodeScript} &
                sleep ${sleepDurationSec}s

                echo "#${i}-${workload}/${j}: executing for $cl clients"
                ${ycsbPath}/bin/go-ycsb run etcd -P ${ycsbPath}/workloads/${workload} -p target=${targetThroughput} -p threadcount=${cl} -p recordcount=${numDiffKeys} -p operationcount=${n} -p etcd.hostname=${etcdHostname} -p etcd.latfilename=${latFilename}

                echo "#${i}-${workload}/${j}: killing local server and copying results"
                mkdir -p ${rootFolder}/${t}thr/
                mv -f ${latFilename} ${rootFolder}/${t}thr/
                killall etcd -u root -w; mv -f ${serverMeasurePath}/*.out ${rootFolder}/${t}thr/
            fi
        done
    done
    echo "#${i}: finished clients iteration"; echo ""
}

main "$@"; exit
