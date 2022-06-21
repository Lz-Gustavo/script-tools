#!/bin/bash


isRemoteExecution=true
etcdHostname="10.10.1.2"
measureFile=/tmp/recov-time.out

sleepDurationSec=10
iterations=10

recovPath=/tmp/recov
rootFolder=$(pwd)

logFiles=${rootFolder}/logs.tar.gz
nodeScript=${rootFolder}/run-singlenode.sh
etcdPath=/media/disk1/etcd

main() {
    if [[ $# -lt 1 ]]; then
        echo "using ${recovPath} value for 'recovPath'"
    else
        echo "using $1 as value for 'recovPath'"
        recovPath=$1
    fi

    if [[ $# -ne 2 ]]; then
        echo "using ${rootFolder} value for 'rootFolder'"
    else
        echo "using $2 as value for 'rootFolder'"
        rootFolder=$2
    fi

    echo "running..."
    for (( i = 0; i < ${iterations}; i++ )); do
        if [[ "${isRemoteExecution}" == "true" ]]; then
            doRemoteExecution $i
        else
            doLocalExecution $i
        fi
    done
    echo "finished!"
}

doRemoteExecution() {
    local i=$1

    echo "#${i}: starting remote execution"
    echo "#${i}: purging previous state"
    ssh root@${etcdHostname} "rm ${recovPath}/*; rm -r ${etcdPath}/*"

    echo "#${i}: preparing files"
    ssh root@${etcdHostname} "mkdir -p ${recovPath}; cp ${logFiles} ${recovPath}; tar -xzvf ${recovPath}/logs.tar.gz -C ${recovPath} --strip-components 3; rm ${recovPath}/logs.tar.gz"

    echo "#${i}: launching server on remote"
    ssh root@${etcdHostname} "${nodeScript}" &
    sleep ${sleepDurationSec}s

    echo "#${i}: killing server on remote and copying results"
    ssh root@${etcdHostname} "killall etcd -u root -w; mv -f ${measureFile} ${rootFolder}/${i}-recov-time.out"

    echo "#${i}: finished iteration"; echo ""
}

doLocalExecution() {
    local i=$1

    echo "#${i}: starting local execution"
    echo "#${i}: purging previous state"
    rm ${recovPath}/* && rm -r ${etcdPath}/*

    echo "#${i}: preparing files"
    mkdir -p ${recovPath} && cp ${logFiles} ${recovPath} && tar -xzvf ${recovPath}/logs.tar.gz -C ${recovPath} --strip-components 3 && rm ${recovPath}/logs.tar.gz

    echo "#${i}: launching local server"
    ${nodeScript} &
    sleep ${sleepDurationSec}s

    echo "#${i}: killing server and copying results"
    killall etcd -u root -w && mv -f ${measureFile} ${rootFolder}/${i}-recov-time.out

    echo "#${i}: finished iteration"; echo ""
}

main "$@"; exit
