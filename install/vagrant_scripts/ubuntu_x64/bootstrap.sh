#!/usr/bin/env bash
echo "Makahiki Environment Setup Script for Ubuntu (x64)"
echo "--------------------------------------------------"
echo "Script started at $(date)"
apt-get install -y git
apt-get install -y gcc
apt-get install -y python-setuptools
easy_install pip
apt-get install -y python-imaging
apt-get install -y python-dev
apt-get install -y libjpeg-dev
# Python Imaging Library shared library symlink setup
echo "Checking locations of Python Imaging Library shared libraries."
if [ ! -f /usr/lib/libjpeg.so ]
	then
	    if [ -f /usr/lib/x86_64-linux-gnu/libjpeg.so ]
			then
				echo "Found: /usr/lib/x86_64-linux-gnu/libjpeg.so"
				echo "Creating symlink: /usr/lib/libjpeg.so --> /usr/lib/x86_64-linux-gnu/libjpeg.so"
				echo "sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so"
				sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/
			else
				echo "Could not find libjpeg.so in /usr/lib or /usr/lib/x86_64-linux-gnu/." 
				echo "Python Imaging Library packages may not have installed properly."
				echo "Script exiting at $(date)."
				exit 1
		fi
	else
		echo "Found: /usr/lib/libjpeg.so"
fi

if [ ! -f /usr/lib/libz.so ]
	then
		if [ -f /usr/lib/x86_64-linux-gnu/libz.so ]
			then
				echo "Found: /usr/lib/x86_64-linux-gnu/libz.so"
				echo "Creating symlink: /usr/lib/libz.so --> /usr/lib/x86_64-linux-gnu/libz.so"
				echo "sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/"
				sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
			else
				echo "Could not find libz.so in /usr/lib or /usr/lib/x86_64-linux-gnu/."
				echo "Python Imaging Library packages may not have installed properly."
				echo "Script exiting at $(date)"
				exit 1
		fi
	else
		echo "Found: /usr/lib/libz.so"
fi
echo "Python Imaging Library shared libraries check is complete."
apt-get install -y postgresql-9.1
apt-get install -y libpq-dev
apt-get install -y memcached
apt-get install -y libmemcached-dev
pip install virtualenvwrapper
echo "Script completed at $(date)"
exit 0