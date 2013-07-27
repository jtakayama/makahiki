#!/usr/bin/env bash
MD5SUM_PGHBA_EXPECTED=$(md5sum "/vagrant/pg_hba.conf.ubuntu.default")
MD5SUM_PGHBA_ACTUAL=$(md5sum "/etc/postgresql/9.1/main/pg_hba.conf")
MD5SUM_PGHBA_MAKAHIKI=$(md5sum "/vagrant/pg_hba.conf.ubuntu.makahiki")

# Split string <checksum><2 spaces><filename> on spaces (awk default)
MD5_PGHBA_EXPECTED=$(echo "$MD5SUM_PGHBA_EXPECTED" | awk '{ print $1 }')
MD5_PGHBA_ACTUAL=$(echo "$MD5SUM_PGHBA_ACTUAL" | awk '{ print $1 }')
MD5_PGHBA_MAKAHIKI=$(echo "$MD5SUM_PGHBA_MAKAHIKI" | awk '{ print $1 }')

echo "Expected md5 checksum of default PostgreSQL 9.1 pg_hba.conf: $MD5_PGHBA_EXPECTED"
echo "Actual md5 checksum of default PostgreSQL 9.1 pg_hba.conf: $MD5_PGHBA_ACTUAL"

if [ $MD5_PGHBA_EXPECTED = $MD5_PGHBA_ACTUAL ]
    then
        echo "Checksums match. pg_hba.conf will be overwritten with Makahiki settings."
        echo "sudo cp /vagrant/pg_hba.conf.ubuntu.makahiki /etc/postgresql/9.1/main/pg_hba.conf"
        sudo cp /vagrant/pg_hba.conf.ubuntu.makahiki /etc/postgresql/9.1/main/pg_hba.conf
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
