#!/bin/bash

user=user
etcdHostname="10.10.1.2"
path=/users/${user}/go/src/go-ycsb
measurepath=/tmp

numDiffKeys=1000000 # 1kk
numOps=240000
threads=25

workloads=("workloadaprime")
targetThrs=(2000 3000 4000)

if [[ $# -ne 1 ]]; then
	echo "usage: $0 'rootFolder'"
	exit 1
fi

echo "running..."
for workload in ${workloads[*]}; do
	for t in ${targetThrs[*]}; do
		echo "launching server on remote"
		ssh root@${etcdHostname} "/users/${user}/experiment/run-singlenode.sh" &
		sleep 5s

		echo "executing $workload for $t target throughput"
		$path/bin/go-ycsb run etcd -P $path/workloads/${workload} -p target=${t} -p threadcount=${threads} -p recordcount=${numDiffKeys} -p operationcount=${numOps} -p etcd.hostname=${etcdHostname} -p etcd.thinktime=0

		echo "killing server on remote and copying results"
		mkdir -p $1/${workload}/${t}thr
		ssh root@${etcdHostname} "killall etcd -u root -w; mv ${measurepath}/*.out $1/${workload}/${t}thr/"

		echo "finished ${t} target throughput..."; echo ""
	done
done

echo "finished!"
