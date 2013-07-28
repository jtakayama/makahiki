#!/usr/bin/env bash
echo "Makahiki Environment Setup Script for Ubuntu (x64)"
echo "--------------------------------------------------"
echo "Script started at $(date)"
echo "Appending locale settings (UTF-8) to /etc/bash.bashrc"
echo "# UTF-8 locale settings for Makahiki" >> /etc/bash.bashrc
echo "export LANGUAGE=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LANG=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LC_ALL=en_US.UTF-8" >> /etc/bash.bashrc
locale-gen en_US.UTF-8
dpkg-reconfigure locales
echo "Done configuring locale settings."
echo "Updating package list."
echo "apt-get update"
apt-get update
echo "Done updating package list."
echo "Installing git."
echo "apt-get install -y git"
apt-get install -y git
echo "Done installing git."
echo "Installing gcc."
echo "apt-get install -y gcc"
apt-get install -y gcc
echo "Done installing gcc."
echo "Installing python-setuptools."
echo "apt-get install -y python-setuptools" 
apt-get install -y python-setuptools
echo "Done installing python-setuptools."
echo "Installing pip."
echo "easy_install pip"
easy_install pip
echo "Done installing pip."
echo "Installing python-imaging."
echo "apt-get install -y python-imaging"
apt-get install -y python-imaging
echo "Done installing python-imaging."
echo "Installing python-dev."
echo "apt-get install -y python-dev"
apt-get install -y python-dev
echo "Done installing python-dev."
echo "apt-get install -y libjpeg-dev"
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
echo "Installing postgresql-9.1."
echo "apt-get install -y postgresql-9.1"
apt-get install -y postgresql-9.1
echo "Done installing postgresql-9.1."
echo "Installing libpq-dev."
echo "apt-get install -y libpq-dev"
apt-get install -y libpq-dev
echo "Done installing libpq-dev."
echo "Configuring PostgreSQL cluster \"main\" with locale en_US.UTF8"
echo "pg_dropcluster 9.1 main --stop"
pg_dropcluster 9.1 main --stop
echo "pg_createcluster --locale en_US.UTF8 9.1 main"
pg_createcluster --locale en_US.UTF8 9.1 main
echo "Done configuring cluster \"main\"."
echo "Installing memcached."
echo "apt-get install -y memcached"
apt-get install -y memcached
echo "Finished installing memcached."
echo "Installing libmemcached-dev."
echo "apt-get install -y libmemcached-dev"
apt-get install -y libmemcached-dev
echo "Done installing libmemcached-dev."
echo "Installing virtualenvwrapper."
echo "pip install virtualenvwrapper"
pip install virtualenvwrapper
echo "Done installing virtualenvwrapper."
echo "Appending virtualenvwrapper settings to /home/vagrant/.bashrc."
echo "# Virtualenvwrapper settings for makahiki" >> /home/vagrant/.bashrc
echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
echo "export PROJECT_HOME=/home/vagrant/makahiki" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
echo "Done appending settings to /home/vagrant/.bashrc."
echo "Downloading source code from Github."
echo "cd /home/vagrant"
cd /home/vagrant
# This line needs to be changed before merging with the main repository
echo "git clone http://github.com/jtakayama/makahiki"
git clone http://github.com/jtakayama/makahiki.git
echo "chown -R vagrant:vagrant /home/vagrant/makahiki"
chown -R vagrant:vagrant /home/vagrant/makahiki
echo "Done downloading source code."
echo "Script completed at $(date)"
exit 0