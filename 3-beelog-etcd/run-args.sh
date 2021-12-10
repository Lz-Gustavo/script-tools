#!/bin/bash

user=user
nodeIP=10.10.1.2
freshStart=true

diskpath=/media/disk1
measurepath=/tmp

stateFolder=${diskpath}/etcd
beelogFolder=${diskpath}/beelog

if [[ $# -ne 2 ]]; then
	echo "usage: $0 'logConfig' 'batchSize'"
  echo "logConfig: 0 (disabled); 1 (SL); 2 (SL-batch); 3 (beelog, PL)"
	exit 1
fi

export ETCD_LOG_CONFIG=$1
export ETCD_LOG_BATCH_SIZE=$2

export ETCD_THR_FILE=${measurepath}/throughput.out
export ETCD_LAT_FILE=${measurepath}/latency.out

export ETCD_BEELOG_CONC_LEVEL=2
export ETCD_BEELOG_LOGS_DIR=${beelogFolder}
export ETCD_BEELOG_LAT_FILE=${measurepath}/bl-latency.out
export ETCD_BEELOG_PARALLEL_IO=false
export ETCD_BEELOG_SECOND_DISK_LOGS_DIR=/media/disk2/beelog

export ETCD_DATA_DIR=${stateFolder}/data
export ETCD_WAL_DIR=${stateFolder}/wal
export ETCD_SNAPSHOT_COUNT=1000000000000 # infinite?


if [[ ${freshStart} == "true" ]]; then
  rm -rf ${stateFolder}
  rm -rf ${beelogFolder}
  mkdir ${beelogFolder}
fi

/users/${user}/go/src/github.com/Lz-Gustavo/etcd/bin/etcd --name=node0 \
  --log-level=error \
  --listen-peer-urls=http://0.0.0.0:2380 \
  --listen-client-urls=http://0.0.0.0:2379 \
  --advertise-client-urls=http://${nodeIP}:2379 \
  --initial-advertise-peer-urls=http://${nodeIP}:2380 \
  --initial-cluster node0=http://${nodeIP}:2380 \
  --initial-cluster-state=new
