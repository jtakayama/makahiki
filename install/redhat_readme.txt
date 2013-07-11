redhat_readme.txt
=================

INTRODUCTION:
-------------------------------------------------------------------------------
This is a README file for the Makahiki installation scripts.

The install_altinstall.py script calls a set of Python scripts which partially 
automate the process of installing Makahiki on Red Hat Enterprise Linux x64.

The scripts rely on the yum package manager. The script has been tested on 
CentOS 6 x64. Other Red Hat-based operating systems are not supported.

If you would prefer to install Makahiki manually, see 
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html.

Makahiki source code is available from https://github.com/csdl/makahiki.
-------------------------------------------------------------------------------

WARNING:
-------------------------------------------------------------------------------
This script should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

For Makahiki to work on RHEL 6, you must install Python 2.7.3 as an altinstall.
The default version on RHEL 6 is Python 2.6.6, which cannot be changed without 
causing problems with operating system tools.

1. Compile and install Python 2.7.3 as an altinstall:
-------------------------------------------------------------------------------
Switch to your top-level makahiki directory:
% cd ~/makahiki

Run the install/python273_altinstall.py script as follows:
1. Run it with --pythonsetup to install programs needed to 
   compile Python:
% sudo ./install/python273_altinstall.py --pythonsetup

2. Run it with --altinstall to compile Python into an altinstall:
% sudo ./install/python273_altinstall.py --altinstall
-------------------------------------------------------------------------------

2. Installing and configuring other dependencies:
-------------------------------------------------------------------------------
The install/ folder contains the install_altinstall.py script.

Usage of install_altinstall.py:
-------------------------------------------------------------------------------
./install_altinstall.py < --dependencies | --pip | --initialize_instance | --update_instance> 
                        --os < redhat > --arch < x64 >
    
All options require Python 2.7.3 or higher (but not Python 3) to run.
    
    --dependencies: Installs dependencies.

    --pip: Runs "pip install -r requirements.txt" via install/pip/pip_install.py.

    --initialize_instance: Initializes the Makahiki instance with default options.

    --update_instance: Runs the makahiki/scripts/update_instance.py script with default options.
    
    --os: Only redhat (RHEL 6) is supported by this script.
    
    --arch: For RHEL 6, only the x64 architecture is currently supported.

Instructions
------------
In these instructions, a % represents your terminal prompt.

It is assumed that your Makahiki installation is placed in your user home directory.
For a user named "robot," the user home directory would be /home/robot,
and the makahiki directory would be at /home/robot/makahiki.

0. Check your prerequisites:
----------------------------
(1.) Python 2.7.3 or higher (Not Python 3)
At a minimum, you need to have Python 2.7.3 or higher (but not Python 3) 
installed. Use python --version in the terminal to check the version of 
your default Python installation:

% python --version
Python 2.6.6

Red Hat Enterprise Linux 6 (and CentOS 6) come with Python 2.6.6 installed by 
default. This is required as the default version in order for certain system 
tools to work correctly. Any installation of Python 2.7.3 will need to be 
an altinstall.

If you have been following this guide, the python273_altinstall.py script 
created a Python 2.7.3 altinstall for you under /usr/local/bin/python2.7.
Check that it exists:

% /usr/local/bin/python2.7 --version
Python 2.7.3

(2.) Internet connection
Steps 1 and 3 require an Internet connection.

1. Install system environment dependencies:
-------------------------------------------
Switch to your top-level makahiki directory:
% cd ~/makahiki

Run the script with the options specified for your operating system:

RHEL 6 x64:
% sudo ./install/install_altinstall.py --dependencies --os redhat --arch x64

The script installs these packages and their dependencies, if not already installed:
- git
- gcc
- Two versions of python-setuptools (a.k.a. easy_install):
  - For Python 2.6.6: python-setuptools rpm from the default repository
  - For Python 2.7.3: setuptools-0.8 from the pypi repository
    (https://pypi.python.org/packages/source/s/setuptools/setuptools-0.8.tar.gz) 
- Two versions of pip:
  - Installed for Python 2.6.6 and 2.7.3 via setuptools
- Python Imaging Library (packages: python-dev, python-imaging, libjpeg-dev)
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
- libmemcached-dev
- virtualenvwrapper (for Python 2.6.6)

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_dependencies_<timestamp>.log," where <timestamp> is a 
sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.

2. Set up the makahiki virtual environment:
------------------------------------------- 
You will need to add the following lines to the current user's .bashrc file:

# Virtualenvwrapper settings for makahiki
export WORKON_HOME=home/<username>/.virtualenvs
export PROJECT_HOME=home/<username>/makahiki
export PATH=/usr/pgsql-9.1/bin:$PATH
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
source /usr/bin/virtualenvwrapper.sh

Replace <username> with the user's username.

After you are done editing .bashrc, source it to apply the 
new settings to your shell:

% source ~/.bashrc

Switch to the top-level makahiki directory:
% cd ~/makahiki

Then, create the makahiki virtual environment: 

% makahiki$ mkvirtualenv makahiki -p /usr/local/bin/python2.7

Creating a virtual environment should switch you to the virtual environment.
The terminal prompt will be preceded by the name of the virtual environment.
On Ubuntu, this looks like:

(makahiki)robot@computer:~/makahiki$

If creating the virtual environment did not switch you to the virtual 
environment, use "workon" to switch to it:

robot@computer:~/makahiki$ workon makahiki
(makahiki)robot@computer:~/makahiki$

Check that the system can find the location of Postgresql 9.1's 
pg_config library, which is needed for pip to compile psycopg2:

% which pg_config

Check that your Python version in the virtual environment is 2.7.3:

% python --version
Python 2.7.3

Note for developers:
-------------------------------------------------------------------------------
If you plan to develop Python scripts in this virtual environment, note that 
any script that is run with sudo will use the default Python 2.6.6 unless you 
insert a "shebang line" (a line starting with #!) at the start of the file. 
This shebang line tells the system to use the Python 2.7.3 interpreter:

#!/usr/local/bin/python2.7

A script with a "shebang line" can be run as an executable file
in Linux if you alter its permissions with chmod +x:

% chmod +x filename.py

To run an executable script:

% ./<path-to-file>/filename.py
-------------------------------------------------------------------------------

3. Install dependencies with pip:
---------------------------------
You should still be in the makahiki virtual environment.

Switch to the makahiki directory:

% cd ~/makahiki

Check that the pg_config library's location is part of the PATH.
This is needed to compile psycopg2:

% which pg_config
/usr/pgsql-9.1/bin/pg_config

Run the script with the options specified for your operating system:

RHEL 6 x64:
% ./install/install_altinstall.py --pip --os redhat --arch x64

The list of packages that this step will attempt to install with pip are 
listed in the makahiki/requirements.txt file.

After it attempts to install the packages, the script will check that 
the correct versions were installed.

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_pip_<timestamp>.log," where <timestamp> is a sequence of 
numbers representing a timestamp in the system local time. For more information, 
see Appendix A.

4. PostgreSQL and Environment Variables Configuration
-----------------------------------------------------
You should still be in the makahiki virtual environment.

After the script completes, you must configure PostgreSQL, set up 
environment variables, initialize Makahiki, and start the Makahiki server. 

To configure PostgreSQL, go to the Makahiki documentation and follow 
section 2.1.1.1.1.8, "Install PostgreSQL," to edit the pg_hba.conf file:
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html#install-postgresql

The pg_hba.conf file is located in /var/lib/pgsql/9.1/data/pg_hba.conf.
It is owned by user postgres and group postgres, and it must be opened 
with sudo:

sudo vi /var/lib/pgsql/9.1/data/pg_hba.conf

The vi editor is installed by default, but any text editor can be used.

To set up environment variables, follow the Makahiki documentation in 
section 2.1.1.1.1.13, "Setup environment variables:"
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html#setup-environment-variables

5. Initialize Makahiki
----------------------
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
(discussed in Section 7 of this document) to update source code without losing 
subsequent configuration actions.

The script runs a script at makahiki/makahiki/scripts/initialize_instance.py 
with default options, and is equivalent to the following:
% initialize_instance.py --type default
-------------------------------------------------------------------------------

Run the script with the options specified for your operating system:

RHEL 6 x64:
% ./install/install_altinstall.py --initialize_instance --os redhat --arch x64

You will need to answer "Y" to the question "Do you wish to continue (Y/n)?"

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_initialize_instance_<timestamp>.log," where <timestamp> is 
a sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.

6. Start the Server
-------------------
You should still be in the makahiki virtual environment.

Switch to the top-level makahiki directory:
% cd ~/makahiki

You can now start the web server using manage.py or gunicorn. The manage.py 
web server is better for development, while gunicorn is better for production 
use.

To start the server with manage.py:
% ./manage.py runserver

To start the server with gunicorn:
% ./manage.py run_gunicorn

In a web browser, go to http://localhost:8000 to see the landing page.

7. Update the Makahiki Instance
------------------------------------------
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

Run the script with the options specified for your operating system:

RHEL 6 x64:
% python ./install/install_altinstall.py --update_instance --os redhat --arch x64

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_update_instance_<timestamp>.log," where <timestamp> is 
a sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.

(5.) Start the server with runserver or gunicorn:
To start the server with manage.py:
% ./manage.py runserver

To start the server with gunicorn:
% ./manage.py run_gunicorn

Appendix A. Notes on Log Files
-------------------------------
Log files are created by install.py in in makahiki/install/logs.
The log file names follow this format:
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
