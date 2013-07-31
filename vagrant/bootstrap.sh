#!/usr/bin/env bash
echo "Makahiki Environment Setup Script for Ubuntu (x86)"
echo "--------------------------------------------------"
echo "Script started at $(date)"
echo "Appending locale settings (UTF-8) to /etc/bash.bashrc: started at $(date)"
echo "# UTF-8 locale settings for Makahiki" >> /etc/bash.bashrc
echo "export LANGUAGE=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LANG=en_US.UTF-8" >> /etc/bash.bashrc
echo "export LC_ALL=en_US.UTF-8" >> /etc/bash.bashrc
echo "Appending locale settings (UTF-8): finished at $(date)"
echo "Configuring UTF-8 locale settings: started at $(date)"
locale-gen en_US.UTF-8
dpkg-reconfigure locales
echo "Configuring UTF-8 locale settings: finished at $(date)"
echo "Updating package list: started at $(date)"
echo "apt-get update"
apt-get update
echo "Updating package list: finished at $(date)"
echo "Installing git: started at $(date)"
echo "apt-get install -y git"
apt-get install -y git
echo "Installing git: finished at $(date)"
echo "Installing gcc: started at $(date)"
echo "apt-get install -y gcc"
apt-get install -y gcc
echo "Installing gcc: finished at $(date)"
echo "Installing python-setuptools: started at $(date)"
echo "apt-get install -y python-setuptools"
apt-get install -y python-setuptools
echo "Installing python-setuptools: finished at $(date)"
echo "Installing pip: started at $(date)"
echo "easy_install pip"
easy_install pip
echo "Installing pip: finished at $(date)"
echo "Installing python-imaging: started at $(date)"
echo "apt-get install -y python-imaging"
apt-get install -y python-imaging
echo "Installing python-imaging: finished at $(date)"
echo "Installing python-dev: started at $(date)"
echo "apt-get install -y python-dev"
apt-get install -y python-dev
echo "Installing python-dev: finished at $(date)"
echo "Installing libjpeg-dev: started at $(date)"
echo "apt-get install -y libjpeg-dev"
apt-get install -y libjpeg-dev
echo "Installing libjpeg-dev: finished at $(date)"
# Python Imaging Library shared library symlink setup
echo "Configuring Python Imaging Library shared libraries: started at $(date)"
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
echo "Configuring Python Imaging Library shared libraries: finished at $(date)"
echo "Installing postgresql-9.1: started at $(date)"
echo "apt-get install -y postgresql-9.1"
apt-get install -y postgresql-9.1
echo "Installing postgresql-9.1: finished at $(date)"
echo "Installing libpq-dev: started at $(date)"
echo "apt-get install -y libpq-dev"
apt-get install -y libpq-dev
echo "Installing libpq-dev: finished at $(date)"
echo "Configuring PostgreSQL cluster \"main\" with locale en_US.UTF8: started at $(date)"
echo "pg_dropcluster 9.1 main --stop"
pg_dropcluster 9.1 main --stop
echo "pg_createcluster --locale en_US.UTF8 9.1 main"
pg_createcluster --locale en_US.UTF8 9.1 main
echo "Configuring PostgreSQL cluster \"main\" with locale en_US.UTF8: finished at $(date)"
echo "Copying PostgreSQL 9.1 pg_hba.conf: started at $(date)"
# Begin pg_hba.conf copying code:
MD5SUM_PGHBA_EXPECTED=$(md5sum "/vagrant/config_examples/pg_hba.conf.ubuntu.default")
MD5SUM_PGHBA_ACTUAL=$(md5sum "/etc/postgresql/9.1/main/pg_hba.conf")
MD5SUM_PGHBA_MAKAHIKI=$(md5sum "/vagrant/config_examples/pg_hba.conf.ubuntu.makahiki")

# Split string <checksum><2 spaces><filename> on spaces (awk default)
MD5_PGHBA_EXPECTED=$(echo "$MD5SUM_PGHBA_EXPECTED" | awk '{ print $1 }')
MD5_PGHBA_ACTUAL=$(echo "$MD5SUM_PGHBA_ACTUAL" | awk '{ print $1 }')
MD5_PGHBA_MAKAHIKI=$(echo "$MD5SUM_PGHBA_MAKAHIKI" | awk '{ print $1 }')

echo "Expected md5 checksum of default PostgreSQL 9.1 pg_hba.conf: $MD5_PGHBA_EXPECTED"
echo "Actual md5 checksum of default PostgreSQL 9.1 pg_hba.conf: $MD5_PGHBA_ACTUAL"

if [ $MD5_PGHBA_EXPECTED = $MD5_PGHBA_ACTUAL ]
    then
        echo "Checksums match. pg_hba.conf will be overwritten with Makahiki settings."
        echo "sudo cp /vagrant/config_examples/pg_hba.conf.ubuntu.makahiki /etc/postgresql/9.1/main/pg_hba.conf"
        sudo cp /vagrant/config_examples/pg_hba.conf.ubuntu.makahiki /etc/postgresql/9.1/main/pg_hba.conf
        echo "pg_hba.conf copy succeeded. [ OK ]"
    else
        if [ $MD5_PGHBA_MAKAHIKI = $MD5_PGHBA_ACTUAL ]
            then
                echo "pg_hba.conf file already overwritten with makahiki settings. [ OK ]"
            else
                echo "WARNING! pg_hba.conf default file is different from expected file."
                echo "File could not be safely overwritten with Makahiki defaults."
                echo "You will need to edit it manually."
        fi
fi
# End pg_hba.conf copying code.
echo "/etc/init.d/postgresql-9.1 restart"
/etc/init.d/postgresql-9.1 restart
echo "Copying PostgreSQL 9.1 pg_hba.conf: finished at $(date)"
echo "Installing memcached: started at $(date)"
echo "apt-get install -y memcached"
apt-get install -y memcached
echo "Installing memcached: finished at $(date)"
echo "Installing libmemcached-dev: started at $(date)"
echo "apt-get install -y libmemcached-dev"
apt-get install -y libmemcached-dev
echo "Installing libmemcached-dev: finished at $(date)"
echo "Installing virtualenvwrapper: started at $(date)"
echo "pip install virtualenvwrapper"
pip install virtualenvwrapper
echo "Installing virtualenvwrapper: finished at $(date)"
echo "Creating /home/vagrant/makahiki_env.sh: started at $(date)"
echo "touch /home/vagrant/makahiki_env.sh"
touch /home/vagrant/makahiki_env.sh
echo "chown vagrant:vagrant /home/vagrant/makahiki_env.sh"
chown vagrant:vagrant /home/vagrant/makahiki_env.sh
echo "Appending Makahiki environment variables..."
echo "# Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>" >> /home/vagrant/makahiki_env.sh
echo "export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki" >> /home/vagrant/makahiki_env.sh
echo "# Syntax: <admin_name>:<admin_password>" >> /home/vagrant/makahiki_env.sh
echo "export MAKAHIKI_ADMIN_INFO=admin:admin" >> /home/vagrant/makahiki_env.sh
echo "Creating /home/vagrant/makahiki_env.sh: finished at $(date)"
echo "Appending Makahiki settings to /home/vagrant/.bashrc: started at $(date)"
echo "source /home/vagrant/makahiki_env.sh" >> /home/vagrant/.bashrc
echo "Appending Makahiki settings to /home/vagrant/.bashrc: finished at $(date)"
echo "Downloading source code from Github: started at $(date)"
echo "cd /home/vagrant"
cd /home/vagrant
# This line needs to be changed before merging with the main repository
echo "git clone http://github.com/jtakayama/makahiki"
git clone http://github.com/jtakayama/makahiki.git
echo "chown -R vagrant:vagrant /home/vagrant/makahiki"
chown -R vagrant:vagrant /home/vagrant/makahiki
echo "Downloading source code from Github: finished at $(date)"
echo "pip install: started at $(date)"
echo "cd /home/vagrant/makahiki"
cd /home/vagrant/makahiki
echo "pip install -r requirements.txt"
pip install -r requirements.txt
echo "pip install: finished at $(date)"
echo "Script completed at $(date)"
exit 0