#!/bin/bash

etcdHostname="10.10.1.2"
measureFile=/tmp/recov-time.out

sleepDurationSec=10
iterations=10

recovPath=/tmp/recov
if [[ $# -lt 1 ]]; then
	echo "using ${recovPath} value for 'recovPath'"

else
    echo "using $1 as value for 'recovPath'"
    recovPath=$1
fi

rootFolder=$(pwd)
if [[ $# -ne 2 ]]; then
	echo "using ${rootFolder} value for 'rootFolder'"

else
    echo "using $2 as value for 'rootFolder'"
    rootFolder=$2
fi

logFiles=${rootFolder}/logs.tar.gz
nodeScript=${rootFolder}/run-singlenode.sh
etcdPath=/media/disk1/etcd

echo "running..."
for (( i = 0; i < ${iterations}; i++ )); do
    echo "#${i}: preparing files"
    ssh root@${etcdHostname} "mkdir -p ${recovPath}; cp ${logFiles} ${recovPath}; tar -xzvf ${recovPath}/logs.tar.gz -C ${recovPath} --strip-components 3; rm ${recovPath}/logs.tar.gz"

    echo "#${i}: launching server on remote"
    ssh root@${etcdHostname} "${nodeScript}" &
    sleep ${sleepDurationSec}s

    echo "#${i}: killing server on remote and copying results"
    ssh root@${etcdHostname} "killall etcd -u root -w; mv ${measureFile} ${rootFolder}/${i}-recov-time.out; rm ${recovPath}/*; rm -r ${etcdPath}/*"

    echo "#${i}: finished iteration"; echo ""
done

echo "finished!"
