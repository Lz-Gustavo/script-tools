#! /usr/bin/python
from typing import NamedTuple
import os
import time


class RunConfig(NamedTuple):
	logConfig: int
	clients: list
	numOps: int
	outDir: str


configs = {
	0: RunConfig(
		logConfig=0,
		batchSize=100,
		clients=[9, 17, 25, 33, 41, 49, 57, 65],
		numOps=240000,
		outDir="/users/user/...",
	),
	# TODO
}

logConfigs = [0, 1, 2, 3]
workloads = ["workloada", "workloadaprime"]

user = "user"
etcdHostname = "teste"
measurepath = "/tmp"
targetThroughput = 9000
numDiffKeys = 1000000


def runSSH(rc: RunConfig, workload: str):
	for cl in rc.clients:
		print("launching server on remote")
		
		os.system(f"""
			ssh root@{etcdHostname} "/users/{user}/experiment/run-args.sh"
			{rc.logConfig}
			{rc.batchSize}
			&
		""")
		time.sleep(5)

		print(f"executing $workload for $t clients")
		os.system(f"""
			$path/bin/go-ycsb run etcd -P $path/workloads/${workload}
				-p threadcount={cl}
				-p recordcount={numDiffKeys}
				-p operationcount={rc.numOps}
				-p target={targetThroughput}
				-p etcd.hostname={etcdHostname}
		""")

		print("killing server on remote and copying results")
		os.system(f"mkdir -p {rc.outDir}/{workload}/{cl}c")
		os.system(f"""
			ssh root@{etcdHostname} "killall etcd -u root -w;
			mv {measurepath}/*.out {rc.outDir}/{workload}/{cl}c/"
		""")

		print(f"finished ${cl} client threads...\n")


def main():
	for lc in logConfigs:
		for w in workloads:
			runSSH(configs[lc], w)


if __name__ == "__main__":
	main()
