#!/bin/bash

user=user
nodeIP=10.10.1.2
freshStart=true

diskpath=/media/disk1
measurepath=/tmp

stateFolder=${diskpath}/etcd
beelogFolder=${diskpath}/beelog

# 0: disabled WAL
# 1: standard WAL
# 2: standard batch WAL
# 3: beelog
export ETCD_LOG_CONFIG=3
export ETCD_LOG_BATCH_SIZE=1000
export ETCD_SYNC_IO=false

# 0: naive
export ETCD_BEELOG_RECOV_CONFIG=0

export ETCD_RECOVERY_MSR_ENABLED=false
export ETCD_RECOVERY_MSR_FILE=/tmp/recov-time.out

export ETCD_THR_FILE=${measurepath}/throughput.out
export ETCD_LAT_FILE=${measurepath}/latency.out
export ETCD_BATCHWAL_LAT_FILE=${measurepath}/bw-latency.out

export ETCD_BEELOG_CONC_LEVEL=2
export ETCD_BEELOG_LOGS_DIR=${beelogFolder}
export ETCD_BEELOG_LAT_FILE=${measurepath}/bl-latency.out
export ETCD_BEELOG_PARALLEL_IO=false

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
