#!/usr/bin/env bash
echo "Makahiki Environment Setup Script for Ubuntu (x86)"
echo "--------------------------------------------------"
echo "Script started at $(date)"
echo "Updating package list."
apt-get update
echo "Done updating package list."
echo "Installing git."
apt-get install -y git
echo "Done installing git."
echo "Installing gcc."
apt-get install -y gcc
echo "Done installing gcc."
echo "Installing python-setuptools."
apt-get install -y python-setuptools
echo "Done installing python-setuptools."
echo "Installing pip."
easy_install pip
echo "Done installing pip."
echo "Installing python-imaging."
apt-get install -y python-imaging
echo "Done installing python-imaging."
echo "Installing python-dev."
apt-get install -y python-dev
echo "Done installing python-dev."
apt-get install -y libjpeg-dev
# Python Imaging Library shared library symlink setup
echo "Checking locations of Python Imaging Library shared libraries."
if [ ! -f /usr/lib/libjpeg.so ]
	then
	    if [ -f /usr/lib/i386-linux-gnu/libjpeg.so ]
			then
				echo "Found: /usr/lib/i386-linux-gnu/libjpeg.so"
				echo "Creating symlink: /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so"
				echo "sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/libjpeg.so"
				sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/
			else
				echo "Could not find libjpeg.so in /usr/lib or /usr/lib/i386-linux-gnu/." 
				echo "Python Imaging Library packages may not have installed properly."
				echo "Script exiting at $(date)."
				exit 1
		fi
	else
		echo "Found: /usr/lib/libjpeg.so"
fi

if [ ! -f /usr/lib/libz.so ]
	then
		if [ -f /usr/lib/i386-linux-gnu/libz.so ]
			then
				echo "Found: /usr/lib/i386-linux-gnu/libz.so"
				echo "Creating symlink: /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so"
				echo "sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/"
				sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/
			else
				echo "Could not find libz.so in /usr/lib or /usr/lib/i386-linux-gnu/."
				echo "Python Imaging Library packages may not have installed properly."
				echo "Script exiting at $(date)"
				exit 1
		fi
	else
		echo "Found: /usr/lib/libz.so"
fi
echo "Python Imaging Library shared libraries check is complete."
echo "Installing postgresql-9.1."
apt-get install -y postgresql-9.1
echo "Done installing postgresql-9.1."
echo "Installing libpq-dev."
apt-get install -y libpq-dev
echo "Done installing libpq-dev."
echo "Installing memcached."
apt-get install -y memcached
echo "Finished installing memcached."
echo "Installing libmemcached-dev."
apt-get install -y libmemcached-dev
echo "Done installing libmemcached-dev."
echo "Installing virtualenvwrapper."
pip install virtualenvwrapper
echo "Done installing virtualenvwrapper."
echo "Script completed at $(date)"
exit 0