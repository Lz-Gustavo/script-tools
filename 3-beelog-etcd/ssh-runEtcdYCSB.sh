#!/bin/bash

user=user
etcdHostname="10.10.1.3"
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
		ssh ${user}@${etcdHostname} "/users/${user}/experiments/run-singlenode.sh"

		echo "executing $workload for $t clients"
		$path/bin/go-ycsb run etcd -P $path/workloads/${workload} -p threadcount=${t} -p recordcount=${numDiffKeys} -p operationcount=${numOps} -p target=${targetThr} -p etcd.hostname=${etcdHostname}

		echo "killing server on remote and copying results"
		ssh ${user}@${etcdHostname} "killall -9 etcd -u ${user}; mv /tmp/etcd/*.out $1/${workload}/"

		echo "finished ${t} client threads..."; echo ""		
	done
done

echo "finished!"
