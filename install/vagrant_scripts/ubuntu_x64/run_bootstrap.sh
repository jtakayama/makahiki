#!/usr/bin/env bash
# Sync virtual machine time with real time before creating file timestamp
sudo ntpdate pool.ntp.org
FNAME="ubuntu_x64_"
TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
FNAME2="$FNAME$TIMESTAMP.log"
# Run installation script
sudo sh /vagrant/bootstrap.sh | tee "/vagrant/logs/$FNAME2"

