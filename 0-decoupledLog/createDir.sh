#!/bin/bash

local=.

folders=("AppLogger" "1-Logger" "2-Logger" "NotLog")

#numClients=(1 3 5 7 9 11)
numClients=(1 8 15 22 29 36 43 50)

dataSizeOptions=(0 1 2) #0: 128B, 1: 1KB, 2: 4KB

echo "creating experiment folders..."
for i in ${folders[*]}
do
	mkdir $local/${i}

	for j in ${dataSizeOptions[*]}
	do
		mkdir $local/${i}/${j}

		for k in ${numClients[*]}
		do
			mkdir $local/${i}/${j}/${k}
		done
	done
done

echo "finished!"