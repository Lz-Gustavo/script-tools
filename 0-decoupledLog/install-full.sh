#!/bin/bash

path=/home/user/go

apt-get update
yes | apt-get install golang-1.10
ln -s /usr/lib/go-1.10/bin/go /usr/bin/go
export GOPATH=$path
export GOBIN=$GOPATH/bin
go get github.com/BurntSushi/toml
go get github.com/armon/go-metrics
go get github.com/hashicorp/go-hclog
go get github.com/hashicorp/raft
go get github.com/Lz-Gustavo/raft-demo
go get github.com/Lz-Gustavo/journey

echo "finished installing depencies"