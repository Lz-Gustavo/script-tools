#!/bin/bash

yes | add-apt-repository ppa:longsleep/golang-backports
apt update
yes | apt install golang-1.15

