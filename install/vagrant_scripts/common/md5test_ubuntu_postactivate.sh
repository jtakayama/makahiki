#!/usr/bin/env bash
MD5SUM_POSTACTIVATE_EXPECTED=$(md5sum "/vagrant/postactivate.default")
MD5SUM_POSTACTIVATE_ACTUAL=$(md5sum "$WORKON_HOME/makahiki/bin/postactivate")
MD5SUM_POSTACIVATE_MAKAHIKI=$(md5sum "/vagrant/postactivate.makahiki")

# Split string <checksum><2 spaces><filename> on spaces (awk default)
MD5_POSTACTIVATE_EXPECTED=$(echo "$MD5SUM_POSTACTIVATE_EXPECTED" | awk '{ print $1 }')
MD5_POSTACTIVATE_ACTUAL=$(echo "$MD5SUM_POSTACTIVATE_ACTUAL" | awk '{ print $1 }')
MD5_POSTACTIVATE_MAKAHIKI=$(echo "$MD5SUM_POSTACTIVATE_MAKAHIKI" | awk '{ print $1 }')

echo "Expected md5 checksum of default makahiki postactivate: $MD5_POSTACTIVATE_EXPECTED"
echo "Actual md5 checksum of default makahiki postactivate: $MD5_POSTACTIVATE_ACTUAL"

if [ $MD5_POSTACTIVATE_EXPECTED = $MD5_POSTACTIVATE_ACTUAL ]
    then
        echo "Checksums match. postactivate will be overwritten with Makahiki settings."
        echo "sudo cp /vagrant/postactivate.makahiki $WORKON_HOME/makahiki/bin/postactivate"
        sudo cp /vagrant/postactivate.makahiki $WORKON_HOME/makahiki/bin/postactivate
        echo "postactivate copy succeeded. [ OK ]"
    else
        if [ $MD5_POSTACTIVATE_MAKAHIKI = $MD5_POSTACTIVATE_ACTUAL ]
            then
                echo "postactivate file already overwritten with makahiki settings. [ OK ]"
            else
                echo "WARNING! postactivate default file is different from expected file."
                echo "File could not be safely overwritten with Makahiki defaults."
                echo "You will need to edit it manually."
        fi
fi
