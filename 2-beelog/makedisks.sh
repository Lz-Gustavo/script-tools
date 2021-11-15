#!/bin/bash

yes | mkfs.ext4 /dev/sdb
mkdir /media/disk1
mount /dev/sdb /media/disk1

yes | mkfs.ext4 /dev/sdc
mkdir /media/disk2
mount /dev/sdc /media/disk2
