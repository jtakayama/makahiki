#!/usr/bin/env bash
FNAME="ubuntu_x86_"
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
FNAME2="$FNAME$TIMESTAMP.log"
sudo sh bootstrap.sh | tee "logs/$FNAME2"

