redhat_readme.txt
=================

Contents:
-------------------------------------------------------------------------------
0.0. Introduction
1.0. Install Python 2.7.3 from SCL
2.0. Installing and Configuring Dependencies
2.1. Instructions
2.1.1. Check Prerequisites
2.1.2. Install System Environment Dependencies
2.1.3. Install Pip
2.1.4. Set Up the "makahiki" Virtual Environment
2.1.5. PostgreSQL Configuration
2.1.6. Install Dependencies With Pip
2.1.7. Environment Variables Configuration
2.1.8. Initialize Makahiki
2.1.9. Start the Server
2.1.10. Update the Makahiki Instance
Appendix A. Notes on Log Files
-------------------------------------------------------------------------------

0.0. Introduction
===============================================================================
This is a README file for the Makahiki installation scripts.

The redhat_installer.py script calls a set of Python scripts which partially 
automate the process of installing Makahiki on Red Hat Enterprise Linux 6 x64.

In these instructions, a % represents your terminal prompt.

The scripts rely on the yum package manager. The scripts have been tested on 
CentOS 6 x64. Other Red Hat-based operating systems are not supported.

If you would prefer to install Makahiki manually, see 
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html.

Makahiki source code is available from https://github.com/csdl/makahiki.

WARNING:
-------------------------------------------------------------------------------
This script should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

For Makahiki to work on RHEL 6, you must install Python 2.7.3.
The default version on RHEL 6 is Python 2.6.6, which cannot be changed without 
causing problems with operating system tools.
===============================================================================

1.0. Install Python 2.7.3 from SCL
===============================================================================
This step requires an Internet connection.

(1) Obtain the Makahiki source code:
This readme file usually comes with the Makahiki source code. If you already 
have the Makahiki source code, move or copy the top-level makahiki directory 
to your home directory:
% cp makahiki ~/makahiki

If you do not have the Makahiki source code, clone the GitHub repository into 
your user home directory:
% cd ~/makahiki
% git clone http://github.com/csdl/makahiki.git

(1) Install wget if it is not already installed:
% sudo yum install wget

(2) Switch to your top-level makahiki directory:
% cd ~/makahiki

(3) Run the install/python273_sclinstall.py script to install Python 2.7.3 
    from Red Hat Software Collections:
% sudo ./install/python273_sclinstall.py

This script will:
A. Add the repository file for Red Hat's Python 2.7.3 software collection, 
   http://people.redhat.com/bkabrda/scl_python27.repo, to your 
   /etc/yum.repos.d directory.
B. Install Python 2.7.3 in /opt/rh/python27.

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_sclinstall_<timestamp>.log," where <timestamp> is a 
sequence of numbers representing a timestamp in the system local time. For 
more information, see Appendix A.

After the script finishes, open a terminal and run this command 
to set Python 2.7.3 as the default in the current user's shell:

% scl enable python27 bash

IMPORTANT:
-------------------------------------------------------------------------------
You will need to run this command again each time you launch a new shell where 
you need Python 2.7.3.
-------------------------------------------------------------------------------

The rest of this guide assumes the use of the SCL installation 
of Python 2.7.3.

The SCL installation comes with easy_install (a.k.a. setuptools 
or distribute) and virtualenv (a.k.a. virtualenvwrapper).

Check that these packages are present:

% which easy_install
/opt/rh/python27/root/usr/bin/easy_install

% which virtualenv
/opt/rh/python27/root/usr/bin/virtualenv
===============================================================================

2.0. Installing and Configuring Dependencies
===============================================================================
The install/ directory in the top-level makahiki directory contains the 
redhat_installer.py script. It is used to install dependencies for Makahiki.

Usage of redhat_installer.py:
-------------------------------------------------------------------------------
./redhat_installer.py < --dependencies | --pip | --initialize_instance | 
                        --update_instance > --os < redhat > --arch < x64 >
    
All options require Python 2.7.3 or higher (but not Python 3) to run.
    
    --dependencies: Installs dependencies.

    --pip: Runs "pip install -r requirements.txt." The requirements.txt file 
      is located in the top-level makahiki directory.

    --initialize_instance: Initializes the Makahiki instance with default 
      settings, users, and data.

    --update_instance: Runs the makahiki/scripts/update_instance.py script 
      with default options.
    
    --os: Only redhat (RHEL 6) is supported by this script.
    
    --arch: For RHEL 6, only the x64 architecture is currently supported.
-------------------------------------------------------------------------------
===============================================================================

2.1. Instructions
===============================================================================
In these instructions, a % represents your terminal prompt.

It is assumed that your Makahiki installation is placed in the user's home 
directory. For a user named "robot," the user home directory would be 
/home/robot, and the makahiki directory would be at /home/robot/makahiki.
===============================================================================

2.1.1. Check Prerequisites
===============================================================================
(1.) Python 2.7.3 or higher (Not Python 3)
At a minimum, you need to have Python 2.7.3 or higher (but not Python 3) 
installed. If you have been following this guide, Python 2.7.3 is now 
the default Python for the current user's shell. Check this with 
python --version:

% python --version
Python 2.7.3

(2.) Internet connection
This software requires an internet connection in order to install packages.
===============================================================================

2.1.2. Install System Environment Dependencies
===============================================================================
Switch to your top-level makahiki directory:
% cd ~/makahiki

Run the script as specified:
% sudo ./install/redhat_installer.py --dependencies --os redhat --arch x64

The script installs these packages and their dependencies, if they are not 
already installed:
- All packages in the groupinstall of "Development tools"
- git
- gcc
- Python Imaging Library (packages: python-devel, python-imaging, libjpeg-devel)
  - This also checks that the libjpeg.so and libz.so libraries (or symlinks 
    to them) exist in /usr/lib64. These symlinks should be created automatically 
    upon installation.
- PostgreSQL 9.1:
  - The repository http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch.rpm
    will be added to the yum repositories. 
  - postgresql91-server 
  - postgresql91-contrib
  - postgresql91-devel
- memcached
- libmemcached-0.53
- zlib-devel

The groupinstall may appear to freeze. This is normal: it installs a large 
number of packages, and the script does not print the output until it is 
finished. This step alone can take up to a half-hour on some connections.

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_dependencies_<timestamp>.log," where <timestamp> is a 
sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.
===============================================================================

2.1.3. Install Pip
===============================================================================
If you are not the root user, you will need to log on as the root user.

Sudo does not work: it will try to execute the command in Python 2.6.6.

(1) In the terminal, enable Python 2.7.3 for the shell if you have not already:
% scl enable python27 bash

(2) Install pip:
% easy_install pip

(3) Install virtualenvwrapper:
% pip install virtualenvwrapper
===============================================================================

2.1.4. Set Up the "makahiki" Virtual Environment
===============================================================================
You will need to add the following lines to the current user's .bashrc file.

~/.bashrc settings:
-------------------------------------------------------------------------------
# Virtualenvwrapper settings for makahiki
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/makahiki
if [ !$PROFILE_ENV ]; 
    then
        source /opt/rh/python27/root/usr/bin/virtualenvwrapper.sh
fi
export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:$LD_LIBRARY_PATH
------------------------------------------------------------------------------
After you are done editing .bashrc, source it to apply the 
new settings to your shell:

% source ~/.bashrc

NOTE:
-------------------------------------------------------------------------------
Because virtualenvwrapper was not installed to the default Python installation, 
the user will see this error at logon:
-------------------------------------------------------------------------------
/usr/bin/python: No module named virtualenvwrapper
virtualenvwrapper.sh: There was a problem running the initialization hooks.

If Python could not import the module virtualenvwrapper.hook_loader, 
check that virtualenv has been installed for
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python and that PATH is 
set properly.
-------------------------------------------------------------------------------
To fix this, enable Python 2.7.3 again:

% scl enable python27 bash

Without Python 2.7.3 enabled in the shell, the system will not find the 
virtualenvwrapper installation.
-------------------------------------------------------------------------------

Switch to the top-level makahiki directory:
% cd ~/makahiki

Then, create the makahiki virtual environment: 

% mkvirtualenv makahiki -p /opt/rh/python27/root/usr/bin/python

Creating a virtual environment should switch you to the virtual environment.
The terminal prompt will be preceded by the name of the virtual environment.
On RHEL, this looks like:

(makahiki)[robot@computer makahiki]$

If creating the virtual environment did not switch you to the virtual 
environment, use "workon" to switch to it:

[robot@makahiki makahiki]$ workon makahiki
(makahiki)[robot@computer makahiki]$ 

Check that your Python version in the virtual environment is 2.7.3:

% python --version
Python 2.7.3

Note for developers:
-------------------------------------------------------------------------------
If you plan to develop Python scripts in this virtual environment, note that 
any script that is run with sudo will use the default Python 2.6.6.
-------------------------------------------------------------------------------
===============================================================================

2.1.5. PostgreSQL Configuration
===============================================================================
You should still be in the makahiki virtual environment.

Now that Postgresql is installed, you must enable it as a service 
and configure its authentication settings.

Initialize the Postgresql database and turn the Postgresql service on:

% sudo service postgresql-9.1 initdb
Initializing database:                                     [  OK  ]
% sudo chkconfig postgresql-9.1 on

The pg_hba.conf file is located in /var/lib/pgsql/9.1/data/pg_hba.conf.
It is owned by user postgres and group postgres, and it must be opened 
with sudo:

% sudo vi /var/lib/pgsql/9.1/data/pg_hba.conf

The vi editor is installed by default, but any text editor can be used.

You should edit the pg_hba.conf file so that the settings for "local", 
IPV4 local connections, and IPv6 local connections match the examples below:

Example pg_hba.conf settings:
-------------------------------------------------------------------------------
# TYPE  DATABASE        USER            ADDRESS                 METHOD
# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
-------------------------------------------------------------------------------

WARNING:
-------------------------------------------------------------------------------
The "trust" setting lets local processes like Makahiki or the postgres 
database user connect to the database server without authentication. This is 
useful for development and configuration, but may not be secure enough for 
production use.
-------------------------------------------------------------------------------

Restart the Postgresql server after editing the file:

% sudo service postgresql-9.1 restart
Stopping postgresql-9.1 service:                           [  OK  ]
Starting postgresql-9.1 service:                           [  OK  ]
===============================================================================

2.1.6. Install Dependencies With Pip
===============================================================================
You should still be in the makahiki virtual environment.

Switch to the makahiki directory:

% cd ~/makahiki

Use "export" to temporarily add the Postgresql binaries to the 
system PATH. This is temporary. If you exit the current shell, 
you will need to do this again.

% export PATH=/usr/pgsql-9.1/bin:$PATH
% export PATH=/usr/pgsql-9.1/lib:$PATH
% export PATH=/usr/pgsql-9.1/include:$PATH

Check that the pg_config library's location is part of the PATH.

% which pg_config
/usr/pgsql-9.1/bin/pg_config

If the system cannot find pg_config, pip will not be able to compile the 
psycopg2 module.

Run the script as specified:
% ./install/redhat_installer.py --pip --os redhat --arch x64

The list of packages that this step will attempt to install with pip are 
listed in the makahiki/requirements.txt file.

After it attempts to install the packages, the script will check that 
the correct versions were installed.

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_pip_<timestamp>.log," where <timestamp> is a sequence of 
numbers representing a timestamp in the system local time. For more 
information, see Appendix A.
===============================================================================

2.1.7. Environment Variables Configuration
===============================================================================
The environment variables MAKAHIKI_DATABASE_URL and MAKAHIKI_ADMIN_INFO need 
to be added to the shell environment. To make them permanently available 
whenever you "workon makahiki," add these variables to the 
$WORKON_HOME/makahiki/bin/postactivate file:
-------------------------------------------------------------------------------
# Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki

# Syntax: <admin_name>:<admin_password>
export MAKAHIKI_ADMIN_INFO=admin:admin
-------------------------------------------------------------------------------
Production instances of Makahiki should change the <admin_password> to 
something other than "admin."

You will need to do "workon makahiki" after you have edited the postactivate 
file for the changes to take effect:

% workon makahiki
===============================================================================

2.1.8. Initialize Makahiki
===============================================================================
You should still be in the makahiki virtual environment.

Switch to the makahiki directory:
% cd ~/makahiki

WARNING:
-------------------------------------------------------------------------------
Running the script with --initialize_instance will:
- Install and/or update all Python packages required by Makahiki.
- Reinitialize the database contents and perform any needed database 
  migrations.
- Initialize the system with data.
- Set up static files.

This script should be run only a single time in production scenarios, because 
any subsequent configuration modifications will be lost if install.py is 
invoked with --initialize_instance again. Use the --update_instance option
(discussed in Section 2.1.9, below) to update source code without losing 
subsequent configuration actions.

The script initializes the Makahiki database and populates it with default 
information and users. It is equivalent to running the standalone 
makahiki/makahiki/scripts/initialize_instance.py script with 
"--type default" options.
-------------------------------------------------------------------------------

Run the script as follows:
% ./install/redhat_installer.py --initialize_instance --os redhat --arch x64

You will need to answer "Y" to the question "Do you wish to continue (Y/n)?"

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_initialize_instance_<timestamp>.log," where <timestamp> is 
a sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.
===============================================================================

2.1.9. Start the Server
===============================================================================
You should still be in the makahiki virtual environment.

Switch to the makahiki directory:
% cd ~/makahiki/makahiki

You can now start the web server using manage.py or gunicorn. The manage.py 
web server is better for development, while gunicorn is better for production 
use.

To start the server with manage.py:
% ./manage.py runserver

To start the server with gunicorn:
% ./manage.py run_gunicorn

In a web browser, go to http://localhost:8000 to see the landing page.
===============================================================================

2.1.10. Update the Makahiki Instance
===============================================================================
Makahiki is designed to support post-installation updating of your configured 
system when bug fixes or system enhancements become available. Updating an 
installed Makahiki instance using the install.py script requires the 
following steps:

(1.) Close the running server in the shell process that is running Makahiki:
% (type control-c in the shell running the makahiki server process)

(2.) In the current shell or a new shell, go to the makahiki directory and 
     set up the Makahiki virtual environment:
% cd ~/makahiki
% workon makahiki

(3.) Download the updated source code into the Makahiki installation:
% git pull origin master

(4.) Run the install.py script with --update_instance:

Run the script as specified:
% python ./install/redhat_installer.py --update_instance --os redhat --arch x64

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_update_instance_<timestamp>.log," where <timestamp> is 
a sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.

(5.) Start the server with runserver or gunicorn:
To start the server with manage.py:
% ./manage.py runserver

To start the server with gunicorn:
% ./manage.py run_gunicorn
===============================================================================

Appendix A. Notes on Log Files
===============================================================================
Log files are created by python273_sclinstall.py and redhat_installer.py in 
makahiki/install/logs. The log file names follow this format: 
<script-type>_<timestamp>.log

The timestamp in log file names breaks down as follows:
    year (4 places)
    month (2 places)
    day (2 places)
    hour (2 places)
    minute (2 places)
    second (2 places)
    microsecond (6 places)

The example timestamp 20130101000000102542 breaks down as follows:
Year: 2013, month: 01, day: 01, hour: 00, minute: 00, seconds: 00, 
microseconds: 102542.
===============================================================================