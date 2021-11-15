#!/bin/bash

path=/users/user/go/src/go-ycsb

etcdHostname="155.98.36.32"

workload="workloada"
threadCounts=(9 17 25 33 41 49 57 65)

numDiffKeys=1000000 # 1kk
targetThr=9000

#numOps=10000000 # 10kk
numOps=480000

if [[ $# -ne 1 ]]; then
	echo "usage: $0 'rootFolder'"
	exit 1
fi

#echo "compiling go-ycsb..."
#make -C $path

echo "running..."
for t in ${threadCounts[*]}; do
	$path/bin/go-ycsb run etcd -P $path/workloads/${workload} -p threadcount=${t} -p recordcount=${numDiffKeys} -p operationcount=${numOps} -p target=${targetThr} -p etcd.hostname=${etcdHostname} -p etcd.latfilename="${1}/${workload}/${t}c-lat.out"
	#$path/bin/go-ycsb run etcd -P $path/workloads/${workload} -p threadcount=${t} -p recordcount=${numDiffKeys} -p operationcount=${numOps} -p etcd.hostname=${etcdHostname} -p etcd.latfilename="${1}/${workload}/${t}c-lat.out"
	echo "finished ${t} client threads..."; echo ""
	sleep 5s
done

echo "finished!"
