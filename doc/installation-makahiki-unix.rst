.. _section-installation-makahiki-local-unix:

Local installation on Unix
==========================

These instructions also assume that you are using a Bourne-type shell (such as bash),
which is the default on Mac OS X and Linux. Using a C-shell variant
(like tcsh), is possible but not recommended.

Hardware requirements
---------------------

Our estimated hardware requirements for **production** use are:
  * CPU:  modern dual or quad core
  * RAM: 8 GB
  * Disk space: 10 GB

For **development** only, a modern dual core CPU with 4 GB should be ok, although the more the better.

Install Python
--------------

`Python`_ 2.7.3 or higher (but not Python 3).

To check that python is installed and has the correct version::

  % python --version 
    Python 2.7.3
    
Red Hat Enterprise Linux: Install Python 2.7.3 from SCL
-------------------------------------------------------
As of Red Hat Enterprise Linux (RHEL 6) and CentOS 6, Python 2.6.6 is the default, 
Python 2.7.3 will be installed from a Software Collections Library as a non-default 
Python interpreter.

Install wget::

  % sudo yum install wget

Retrieve the .repo file for the SCL collection and copy it to the system repos directory::

  % wget http://people.redhat.com/bkabrda/scl_python27.repo
  % sudo cp ./scl_python27.repo /etc/yum.repos.d/scl_python27.repo
  

Install Python 2.7.3 from the SCL::

  % sudo yum install python27

Finally, switch to a Python 2.7.3 shell. You will need to use this command to enable Python 2.7.3 
each time you log in::

  % scl enable python27 bash

Install C Compiler
------------------

If you are using Mac OS X, install
`Apple Developer Tools`_ (i.e. Xcode 4). This is required in order to 
build certain libraries (PIL, etc.) that require GCC (which is bundled with
Xcode). Xcode can either be found in your OS X installation DVD, or in the Mac
App Store.

If on Linux, in most cases, you will find the C/C++ compiler is already installed in your environment.

To check that C compiler is installed::

  % gcc --version 

To install gcc on Ubuntu::

  % sudo apt-get install gcc
  
To install gcc on RHEL and CentOS::

  % sudo yum install gcc

Install Git
-----------

Find a package for your operating system at the `GitHub install
wiki`_. We recommend following the GitHub setup instructions at https://help.github.com/articles/set-up-git.

To check that Git is installed::

  % git --version 


Install Pip
-----------

Install it by typing::

  % easy_install pip==1.4.1

Depending on your system configuration, you may
have to type ``sudo easy_install pip``. If you do not have easy_install,
download and install it from the `setuptools website`_. Linux (Ubuntu) users can use 
``sudo apt-get install python-setuptools``.

RHEL and CentOS users should have enabled the SCL Python 2.7.3 environment before installing pip.
They **should not** use ``sudo easy_install``: this installs pip for Python 2.6.6 instead.

RHEL and CentOS users who follow this guide have already installed easy_install as part of 
the Python 2.7.3 SCL installation.

To check that Pip is installed::

  % pip --version 

Install Virtual Environment Wrapper
-----------------------------------

`Virtualenvwrapper`_ allows you to install libraries separately from your global Python path.

Ubuntu
******
Follow the `virtualenvwrapper installation instructions`_ through the Quick Start section to install virtualenv and virtualenvwrapper. Once they are installed, create a virtual environment for makahiki as follows::

  % mkvirtualenv makahiki

To check that virtual environment wrapper is installed::

  % workon makahiki

RHEL and CentOS
***************

RHEL and CentOS users should make sure that they have enabled the SCL Python 2.7.3 environment.

Install virtualenvwrapper::

  % pip install virtualenvwrapper

Add these lines to the end of the ~/.bashrc file::

  # Virtualenvwrapper settings for makahiki
  export WORKON_HOME=$HOME/.virtualenvs
  export PROJECT_HOME=$HOME/makahiki
  # SCL Python settings
  if [ ! $PROFILE_ENV ]; 
      then
          source /opt/rh/python27/root/usr/bin/virtualenvwrapper.sh
  fi
  
Then source this file to apply changes::

  % source ~/.bashrc

Create the virtual environment::

  % mkvirtualenv makahiki

To check that virtual environment wrapper is installed::

  % workon makahiki

.. note::
   After installing virtualenvwrapper, RHEL and CentOS users will see this error at logon::
   
     /usr/bin/python: No module named virtualenvwrapper
     virtualenvwrapper.sh: There was a problem running the initialization hooks.

     If Python could not import the module virtualenvwrapper.hook_loader, 
     check that virtualenv has been installed for
     VIRTUALENVWRAPPER_PYTHON=/usr/bin/python and that PATH is 
     set properly.
   
   This error is related to the system not being able to find Python 2.7.3's virtualenvwrapper installation.
   
   Every time you log on, you must use ``scl enable python27 bash`` to re-enable the Python 2.7.3 environment.

Install Python Imaging Library
------------------------------

Makahiki requires the `Python Imaging Library`_ (PIL).

Mac OS X
********

We have found `Homebrew`_ to be the most reliable way to install PIL.
Once Homebrew is installed, install PIL by typing::

  % brew install pil

Linux
*****

In Ubuntu, install PIL by typing::

  % sudo apt-get install -y python-imaging python-dev libjpeg-dev

In RHEL and CentOS, install PIL by typing::

  % sudo yum install -y python-imaging python-devel libjpeg-devel zlib-devel

Make sure you have both libjpeg (for JPEG) and zlib (for PNG) in the /usr/lib directory. If not, you can make the symbolic link there.

To make the symbolic links in a 32-bit Ubuntu OS::

  % sudo ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/
  % sudo ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/

To make the symbolic links in a 64-bit Ubuntu OS::

  % sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
  % sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so

A 32-bit RHEL or CentOS OS should have symbolic links for libz.so and libjpeg.so in /usr/lib 
created during installation.

To make the symbolic links in a 64-bit RHEL or CentOS OS::

  % sudo ln -s /usr/lib64/libjpeg.so /usr/lib/libjpeg.so
  % sudo ln -s /usr/lib64/libz.so /usr/lib/libz.so 
  
Install PostgreSQL
------------------

Makahiki uses `PostgreSQL`_ as its standard backend database. We recommend version 9.1.3.

Mac OS X
********
Note that on Mac OS X, the installer will need to make changes in the
``sysctl`` settings and a reboot before installation can proceed. 

Linux
*****

On Ubuntu, install the latest version of PostgreSQL 9.1, and install libpq-dev::

  % sudo apt-get install -y postgresql-9.1 libpq-dev

On RHEL and CentOS, install the pgdg91 repository and the latest version of PostgreSQL 9.1, then 
initialize the database and start the server::

  % rpm -i http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch.rpm
  % sudo yum install -y postgresql91-server postgresql91-contrib postgresql91-devel
  % sudo service postgresql-9.1 initdb
  % sudo chkconfig postgresql-9.1 on

After Installation
******************

Once installed, be sure that your PostgreSQL installation's bin/ directory is on
$PATH so that ``pg_config`` and ``psql`` are defined.

RHEL and CentOS users will need to add the bin/ directory to the $PATH::

  % export PATH=/usr/pgsql-9.1/bin:$PATH
  % which pg_config
  /usr/pgsql-9.1/bin/pg_config
  % which psql
  /usr/pgsql-9.1/bin/psql

You will also need to configure authentication for the "postgres" database user.   

During development, a simple way to configure authentication is to make the postgres user
"trusted" locally.  This means that local processes such as Makahiki can connect to the
database server as the user postgres without authentication. To configure this way, edit
the pg_hba.conf file and change::

  local all postgres ident

to:: 

  local all postgres trust

The first line might be: "local all postgres peer". Change it to "local all postgres trust". 

If you update the pg_hba.conf file you will have to restart the postgres server.

Ubuntu
******

The pg_hba.conf file is located in /etc/postgresql/9.1/main/pg_hba.conf and 
must be opened with ``sudo``. Edit it to match the examples below:: 

  # Database administrative login by Unix domain socket
  local   all             postgres                                trust
  
  # TYPE  DATABASE        USER            ADDRESS                 METHOD
  
  # "local" is for Unix domain socket connections only
  local   all             all                                     trust
  # IPv4 local connections:
  host    all             all             127.0.0.1/32            md5
  # IPv6 local connections:
  host    all             all             ::1/128                 md5

Restart the server after updating pg_hba.conf::

  % /etc/init.d/postgresql restart

or::

  % sudo /etc/init.d/postgresql restart

RHEL and CentOS
***************

The pg_hba.conf file is located in /var/lib/pgsql/9.1/data/pg_hba.conf and 
must be opened with ``sudo``. Edit it to match the examples below::

  # TYPE  DATABASE        USER            ADDRESS                 METHOD
  # "local" is for Unix domain socket connections only
  local   all             all                                     trust
  # IPv4 local connections:
  host    all             all             127.0.0.1/32            md5
  # IPv6 local connections:
  host    all             all             ::1/128                 md5

Restart the server after updating pg_hba.conf::

  % sudo service postgresql-9.1 restart

All Platforms
*************

Alternatively, you can create a .pgpass file containing the credentials for the user postgres. See
the PostgreSQL documentation for more information on the .pgpass file.

To check that PostgresSQL is installed and configured with "trusted" locally::

  % psql -U postgres

It should not prompt you for a password.


Install Memcache
----------------

Makahiki can optionally use `Memcache`_ to improve performance, especially in the
production environment.  To avoid the need for alternative configuration files, we require
local installations to install Memcache and an associated library even if developers aren't
intending to use it.

Mac OS X
********
On Mac OS X, if you have installed `Homebrew`_, you can install these by typing::

  % brew install memcached
  % brew install libmemcached

Linux
*****
Linux users will need to download and build libmemcached from source. Start by installing memcached.

Ubuntu users::

  % sudo apt-get install -y memcached

RHEL and CentOS users::

  % sudo yum install -y memcached

Next, install packages needed to build libmemcached-0.53 from source.

Ubuntu users::

  % sudo apt-get install -y build-essential g++ libcloog-ppl-dev libcloog-ppl0

RHEL and CentOS users::

  % sudo yum groupinstall -y "Development tools"

Next, download the source code and extract the archive::
 
  % wget http://launchpad.net/libmemcached/1.0/0.53/+download/libmemcached-0.53.tar.gz
  % tar xzvf libmemcached-0.53.tar.gz

.. warning:: Do not download and extract the source code in a directory that is synchronized with a Windows 
   file system. This will cause the libmemcached-0.53 installation process to fail to create hard 
   links and symbolic links during installation.
   

Switch into the extracted directory, then configure, make, and make install::
  
  % cd libmemcached-0.53 
  % ./configure
  % make
  % make install
  
Finally, check the location of the libmemcached.so library:: 

  % stat /usr/local/lib/libmemcached.so

If libmemcached.so is found successfully, then the installation is complete.

.. _Python: http://www.python.org/download/
.. _Python Imaging Library: http://www.pythonware.com/products/pil/
.. _Homebrew: http://mxcl.github.com/homebrew/
.. _GitHub install wiki: http://help.github.com/git-installation-redirect
.. _setuptools website: http://pypi.python.org/pypi/setuptools
.. _Virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/
.. _virtualenvwrapper installation instructions: http://www.doughellmann.com/docs/virtualenvwrapper/install.html#basic-installation
.. _PostgreSQL: http://www.postgresql.org/
.. _Apple Developer Tools: https://developer.apple.com/technologies/mac/
.. _Memcache: http://memcached.org
.. _Heroku's memcache installation instructions: http://devcenter.heroku.com/articles/memcache#local_memcache_setup

Download the Makahiki source
----------------------------

You can download the source by cloning or forking the `Makahiki Git repository`_::

  % git clone git://github.com/csdl/makahiki.git

This will create the new folder and download the code from the repository.

.. _Makahiki Git repository: https://github.com/csdl/makahiki/

Workon makahiki
---------------

The remaining steps require you to be in the makahiki/ directory and to have
activated that virtual environment::

  % cd makahiki/
  % workon makahiki

If you start a new shell in the midst of this process, you must be sure to invoke ``workon makahiki``
and of course cd to the appropriate directory before continuing. 

Install required packages
-------------------------

You can install the required Python package for Makahiki by::

  % pip install -r requirements.txt

Don't worry that this command generates lots and lots of output.

Setup environment variables
---------------------------

At a minimum, Makahiki requires two environment variables: MAKAHIKI_DATABASE_URL and
MAKAHIKI_ADMIN_INFO.  

The following lines show example settings for these two environment variables, preceded by 
a comment line describing their syntax::

  % # Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
  % export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki

  % # Syntax:  <admin_name>:<admin_password>
  % export MAKAHIKI_ADMIN_INFO=admin:admin

You will want to either add these variables to a login script so they are
always available, or you can edit the ``postactivate`` file (in Unix, found in
``$WORKON_HOME/makahiki/bin``) so that they are defined whenever you 
``workon makahiki``.

Note that you will want to provide a stronger password for the makahiki
admin account if this server is publically accessible. 

Makahiki also utilizes a variety of other environment variables. For complete
documentation, see :ref:`section-environment-variables`.

Initialize Makahiki
-------------------

Next, invoke the initialize_instance script, passing it an argument to specify what kind
of initial data to load. You need to be in the makahiki/makahiki directory. In most cases, 
you will want to load the default dataset, as shown next::

  % cd makahiki
  % scripts/initialize_instance.py --type default

This command will:
  * Install and/or update all Python packages required by Makahiki;
  * Reinitialize the database contents and perform any needed database migrations. 
  * Initialize the system with data.
  * Set up static files. 

.. warning:: initialize_instance will wipe out all challenge configuration modifications!

   The initialize_instance script should be run only a single time in production
   scenarios, because any subsequent configuration modifications will be lost if initialize_instance is
   invoked again.   Use update_instance (discussed below) to update source code without
   losing subsequent configuration actions.

You will have to answer 'Y' to the question "Do you wish to continue (Y/n)?"
 
Start the server
----------------

Finally, you can start the Makahiki server using either::

  % ./manage.py run_gunicorn

or::

  % ./manage.py runserver

The first alternative (run_gunicorn) runs a more efficient web server, while the second (runserver) invokes a server
that is better for development (for example, :ref:`section-theme-development`).

Verify that Makahiki is running
-------------------------------

Open a browser and go to http://localhost:8000 to see the landing page, which should look
something like this:

.. figure:: figs/guided-tour/guided-tour-landing.png
   :width: 600 px
   :align: center


Configure your Makahiki instance
--------------------------------

Now that you have a running Makahiki instance, it is time to configure it for your
challenge, as documented in :ref:`section-site-configuration`.

Updating your Makahiki instance
-------------------------------

Makahiki is designed to support post-installation updating of your configured system when bug fixes or
system enhancements become available.   Updating an installed Makahiki instance is quite
simple, and consists of the following steps.

1. Bring down the running server in the shell process running Makahiki::

   % (type control-c in the shell running the makahiki server process)
 
2. In that shell or a new shell, go to your Makahiki installation directory, and ensure
   the Makahiki virtual environment is set up::

   % cd makahiki
   % workon makahiki

3. Download the updated source code into your Makahiki installation::

   % git pull origin master

4. Run the update_instance script to update your local configuration::

   % ./scripts/update_instance.py

5. Finally, restart your server, using either::

     % ./manage.py run_gunicorn

   or::

     % ./manage.py runserver



