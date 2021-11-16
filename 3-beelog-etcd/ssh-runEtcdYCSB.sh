#!/bin/bash

user=user
etcdHostname="10.10.1.2"
path=/users/${user}/go/src/go-ycsb


workloads=("workloada")
threadCounts=(9 17 25 33 41 49 57 65)

numDiffKeys=1000000 # 1kk
targetThr=9000
numOps=480000


if [[ $# -ne 1 ]]; then
	echo "usage: $0 'rootFolder'"
	exit 1
fi

echo "running..."
for workload in ${workloads[*]}; do
	for t in ${threadCounts[*]}; do
		echo "launching server on remote"
		ssh root@${etcdHostname} "/users/${user}/experiment/run-singlenode.sh" &
		sleep 5s

		echo "executing $workload for $t clients"
		$path/bin/go-ycsb run etcd -P $path/workloads/${workload} -p threadcount=${t} -p recordcount=${numDiffKeys} -p operationcount=${numOps} -p target=${targetThr} -p etcd.hostname=${etcdHostname}

		echo "killing server on remote and copying results"
		mkdir -p $1/${workload}/${t}c
		ssh root@${etcdHostname} "killall etcd -u root -w; mv /tmp/*.out $1/${workload}/${t}c/"

		echo "finished ${t} client threads..."; echo ""
	done
done

echo "finished!"
