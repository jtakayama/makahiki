.. _section-configuration-system-administration-memcached:


Configure Memcached
========================

About Memcached
---------------

`Memcached <http://memcached.org>`_ is a memory object caching daemon that stores objects in memory to 
reduce the load on the database. This section explains how to configure Makahiki to use memcached as 
the backend cache for its web server.

.. note:: Memcached is optional. However, it is recommended that Memcached be configured on production servers.

These instructions assume that you are using a Bourne-type shell (such as 
bash), which is the default on Mac OS X and Linux.

Replace the Default libmemcached Installation
---------------------------------------------

If you have followed the instructions in ref::install-makahiki-unix, you installed a default 
version of memcached and its dependency libmemcached for your operating system. Check your 
libmemcached version.

On Ubuntu, libmemcached cannot be checked directly. Check libmemcached-dev instead. This example shows version 0.44::

  % dpkg -s libmemcached-dev
  Package: libmemcached-dev
  Status: install ok installed
  -- output omitted --
  Version: 0.44-1.1build1
  -- output omitted --

On Red Hat Enterprise Linux or CentOS, check for libmemcached. This example shows version 0.31::

  % rpm -q libmemcached
  libmemcached-0.31-1.1.el6.x86_64

For production use, libmemcached-0.53 is recommended. If you have a different version, it will 
be necessary to uninstall libmemcached-dev. This section uninstalls libmemcached-dev, downloads 
libmemcached-0.53, and builds and installs libmemcached-0.53 from its source code.

Start by uninstalling libmemcached. On Ubuntu, uninstall libmemcached-dev::

  % apt-get remove libmemcached-dev

On Red Hat Enterprise Linux or CentOS, uninstall libmemcached (which will also 
uninstall libmemcached-devel)::

  % yum remove libmemcached

First, install some libraries and packages needed to build libmemcached::

  % apt-get install -y build-essential g++ libcloog-ppl-dev libcloog-ppl0
  
Next, create the makahiki-temp-downloads directory to download the libmemcached-0.53 source code 
archive into. Do not create this directory in any directory that is shared with a Windows 
file system. The Windows file system is not compatible with the creation of symbolic links 
that occurs during the libmemcached installation process. Create the directory and switch 
to it::

  % mkdir <path-to-parent-directory>/makahiki-temp-downloads
  % cd <path-to-parent-directory>/makahiki-temp-downloads
 
Next, download the source code archive::
 
  % wget http://launchpad.net/libmemcached/1.0/0.53/+download/libmemcached-0.53.tar.gz

Next, extract the archive and switch into the extracted directory::

  % tar xzvf libmemcached-0.53.tar.gz
  % cd libmemcached-0.53

Next, configure, make, and make install:: 

  % ./configure
  % make
  % make install
  
After "make install" finishes, check for the location of the libmemcached.so library. 
On a Linux system, your output should be similar to the output shown below::

  % stat /usr/local/lib/libmemcached.so
  vagrant@precise32:~$ stat /usr/local/lib/libmemcached.so
  File: `/usr/local/lib/libmemcached.so' -> `libmemcached.so.8.0.0'
  -- output omitted --

If libmemcached.so was found successfully, the installation is complete. 
The makahiki-temp-downloads directory can be removed if desired::

  % rm -rf <path-to-parent-directory>/makahiki-temp-downloads

Continue to the next section to configure environment variables.

Environment Variables
---------------------

Open the $WORKON_HOME/makahiki/bin/postactivate file. Add these lines to the end::

  export MAKAHIKI_USE_MEMCACHED=True
  # Don't add libmemcached paths more than once
  if [ ! $LIBMEMCACHED_PATHS_ADDED ];
      then
          export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:$LD_LIBRARY_PATH
          export LIBMEMCACHED_PATHS_ADDED=True
  fi

Next, workon makahiki to apply the changes::

  % workon makahiki

Continue to the next section to start the memcached service.

Start the memcached Service
---------------------------

Next, the memcached service must be started if it is not running::

  % sudo service memcached start
  
On Ubuntu, the memcached daemon will automatically run at startup. 
In Red Hat / CentOS systems, however, the user must use chkconfig to enable the daemon to run at startup::

  % sudo chkconfig memcached on

Verify Memcached Settings
-------------------------
To test your Memcached settings, switch to the makahiki virtual environment::

  % workon makahiki
  
Then, change to the makahiki/makahiki directory and run the manage.py shell::

  % cd ~/makahiki/makahiki
  % ./manage.py shell

This will open a Python shell. 

In the shell, run the below commands to test whether Memcached is configured and running::

  Python 2.7.3 (default, Apr 10 2013, 05:46:21) 
  [GCC 4.6.3] on linux2
  Type "help", "copyright", "credits" or "license" for more information.
  (InteractiveConsole)
  >>> from django.core.cache import cache
  >>> cache
  <django_pylibmc.memcached.PyLibMCCache object at 0xa669c0c>
  >>> cache == None
  False
  >>> cache.set('test','Hello World')
  True
  >>> cache.get('test')
  'Hello World'
  >>> exit()

Troubleshooting
---------------

If running ``manage.py shell`` causes the error ``django.core.cache.backends.base.InvalidCacheBackendError: Could not import pylibmc``, 
then the LD_LIBRARY_PATH may not be set correctly in $WORKON_HOME\makahiki\bin\postactivate. This error occurs when ``MAKAHIKI_USE_MEMCACHED=True`` but 
LD_LIBRARY_PATH does not include the location of pylibmc.

If any of the following errors occurs, memcached is not correctly configured:

* cache is a ``DummyCache object``
* ``cache == None`` returns True
* ``cache.set('test','Hello World')`` returns ``False``
* ``cache.get('test')`` causes a segmentation fault or exits the Python shell

Verify that your postactivate settings for MAKAHIKI_USE_MEMCACHED and LD_LIBRARY PATH match 
the settings added in these instructions.

If you are testing memcached on your local machine, verify that the makahiki/makahiki/settings.py file
specifies a ``django_pylibmc.memcached.PyLibMCCache`` cache as its backend cache for location 127.0.0.1.
The settings.py file should include the following lines::

    else:
        CACHES = {'default':
                    {'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                     'LOCATION': '127.0.0.1',
                     'BINARY': True,
         }}










