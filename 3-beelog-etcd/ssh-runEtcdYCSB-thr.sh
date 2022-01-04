#!/bin/bash

user=user
etcdHostname="10.10.1.2"
path=/users/${user}/go/src/go-ycsb
measurepath=/tmp

numDiffKeys=1000000 # 1kk
threads=100

workloads=("workloadaprime")

# unique size arrays
numOps=(100000 200000 300000 500000 500000)
targetThrs=(1000 2000 4000 8000 16000)

if [[ $# -ne 1 ]]; then
	echo "usage: $0 'rootFolder'"
	exit 1
fi

echo "running..."
for workload in ${workloads[*]}; do
	for (( i = 0; i < ${#targetThrs[*]}; i++ )); do
		t=${targetThrs[$i]}
		n=${numOps[$i]}

		echo "launching server on remote"
		ssh root@${etcdHostname} "/users/${user}/experiment/run-singlenode.sh" &
		sleep 5s

		echo "executing $workload for $t target throughput"
		$path/bin/go-ycsb run etcd -P $path/workloads/${workload} -p target=${t} -p threadcount=${threads} -p recordcount=${numDiffKeys} -p operationcount=${n} -p etcd.hostname=${etcdHostname} -p etcd.thinktime=0

		echo "killing server on remote and copying results"
		mkdir -p $1/${workload}/${t}thr
		ssh root@${etcdHostname} "killall etcd -u root -w; mv ${measurepath}/*.out $1/${workload}/${t}thr/"

		echo "finished ${t} target throughput..."; echo ""
	done
done

echo "finished!"
