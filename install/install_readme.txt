install_readme.txt
==================

This is a README file for the Makahiki installation scripts.

The install.py script calls a set of Python scripts which partially 
automate the process of installing Makahiki on Ubuntu Linux x86, 
Ubuntu Linux x64, and Red Hat Enterprise Linux 6 (RHEL 6) x64.

Makahiki is available at https://github.com/csdl/makahiki.

The install/ folder contains the install.py script and its dependencies.
install.py, or install_altinstall.py:
-------------------------------------
    Usage: python install.py [--dependencies | --pip | initialize_instance | update_instance] --os [ubuntu | redhat] --arch [x86 | x64]
    
    This is the only script the user runs from the terminal. All options require 
    Python 2.7.3 or higher (but not Python 3) to run.
    
    --dependencies: Runs one of the scripts in install/dependency, depending 
                    on the --os and --arch flags.
                    This script must be run with sudo:
                    sudo python install.py --dependencies --os [ubuntu | redhat] --arch [x86 | x64]
    --pip: Runs "pip install -r requirements.txt" via install/pip/pip_install.py.

    --initialize_instance: Runs the makahiki/scripts/initialize_instance.py with default options.

    --update_instance: Runs the makahiki/scripts/update_instance.py script with default options.
    
    --os: Only ubuntu (Ubuntu Linux) or redhat (RHEL 6) are currently supported.
    
    --arch: Ubuntu has x86 and x64 support. For RHEL 6, only the x64 architecture is currently supported.

The --pip, --initialize_instance, and --update_instance options are run the same way regardless of operating system.

WARNING:
-------------------------------------------------------------------------------
This script should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

WARNING 2:
-------------------------------------------------------------------------------
If the default version of Python on your system is not a version of Python 2.7 
that is 2.7.3 or higher, you will need to install Python 2.7 as an altinstall 
(if you have not already done so) and use install_altinstall.py instead. 
All commands for install_altinstall.py are the same. 

See Section 0 and 0.1 for instructions to install Python 2.7.3 as an 
altinstall.
-------------------------------------------------------------------------------

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

Ubuntu versions 12.04.1 LTS and later LTS versions come with Python 2.7.3 installed 
by default. If Python 2.7.3, or a higher version of Python 2.7, is not the default 
Python installation on your system, you will need to download the source tarball from 
python.org and install it as an altinstall. This is left as an exercise for the 
user.

Red Hat Enterprise Linux 6 (and CentOS 6) come with Python 2.6.6 installed by 
default. This is required as the default version in order for certain system 
tools to work correctly. Any installation of Python 2.7.3 will need to be 
an altinstall. The install.py script and its dependency scripts assume 
that, in a RHEL-based system, Python 2.7.3 is an altinstall in 
/usr/bin/python2.7/

Compiling and installing Python 2.7.3 is handled by python273_altinstall.py, 
which is targeted at RHEL 6 x64 systems. For further instructions, see 
section 0.1.

(2.) Internet connection
Steps 1 and 3 require an Internet connection.

0.1. Setting Up Python 2.7.3 as an altinstall:
----------------------------------------------
This section applies to RHEL 6 x64 systems only.

Switch to your top-level makahiki directory:
% cd ~/makahiki

Run the install/python273_altinstall.py script as follows:
1. Run it with --pythonsetup to install programs needed to 
   compile Python:
% sudo python ./install/python273_altinstall.py --pythonsetup

2. Run it with --altinstall to compile Python into an altinstall:
% sudo python ./install/python273_altinstall.py --altinstall

1. Install system environment dependencies:
-------------------------------------------
Switch to your top-level makahiki directory:
% cd ~/makahiki

Run the script with the options specified for your operating system:

Ubuntu x86:
% sudo python ./install/install.py --dependencies --os ubuntu --arch x86

Ubuntu x64:
% sudo python ./install/install.py --dependencies --os ubuntu --arch x86

RHEL 6 x64:
% sudo python ./install/install_altinstall.py --dependencies --os redhat --arch x64

The script installs these packages and their dependencies from 
each operating system's repositories:
- git
- gcc
- python-setuptools
- pip
- Python Imaging Library (packages: python-dev, python-imaging, libjpeg-dev)
  - This also creates symbolic links to libz.so and libjpeg.so 
    in /usr/lib/. What the symbolic links point to is different 
    for each operating system and architecture:
    Ubuntu x86: 
    1. /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so
    2. /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so
    Ubuntu x64:
    1. /usr/lib/libjpeg.so --> /usr/lib/x86_64-linux-gnu/libjpeg.so
    2. /usr/lib/libz.so --> /usr/lib/x86_64-linux-gnu/libz.so 
- PostgreSQL 9.1
  - On Ubuntu, the packages postgresql-9.1 and libpq-dev will be installed.
  - On RHEL 6, the script will add the repository at 
    http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch.rpm
    to the system repositories. The postgresql91-server and postgresql91-contrib packages will be installed.
- memcached
- libmemcached-dev
- virtualenvwrapper

The script also appends these lines to the end of the current user's ~/.bashrc 
file (the example assumes a user named "robot"):
# Virtualenvwrapper settings for makahiki
export WORKON_HOME=home/robot/.virtualenvs
export PROJECT_HOME=home/robot/makahiki
source /usr/local/bin/virtualenvwrapper.sh

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_dependencies_<timestamp>.log," where <timestamp> is a 
sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.

2. Set up the makahiki virtual environment:
------------------------------------------- 
When the environment_setup.sh script finishes, reload the startup file: 

% source ~/.bashrc

Switch to the top-level makahiki directory:
% cd ~/makahiki

Then, create the makahiki virtual environment: 

% makahiki$ mkvirtualenv makahiki

Creating a virtual environment should switch you to the virtual environment.
The terminal prompt will be preceded by the name of the virtual environment.
On Ubuntu, this looks like:

(makahiki)robot@computer:~/makahiki$

If creating the virtual environment did not switch you to the virtual 
environment, use "workon" to switch to it:

robot@computer:~/makahiki$ workon makahiki
(makahiki)robot@computer:~/makahiki$

The same commands will work on RHEL 6.

For further instructions, see the Makahiki documentation for section 
2.1.1.1.1.6, "Install Virtual Environment Wrapper":
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html#install-virtual-environment-wrapper
   
3. Install dependencies with pip:
---------------------------------
You should still be in the makahiki virtual environment.

Switch to the makahiki directory:
% cd ~/makahiki

Run the script with the options specified for your operating system:

Ubuntu x86:
% python ./install/install.py --pip --os ubuntu --arch x86

Ubuntu x64:
% python ./install/install.py --pip --os ubuntu --arch x64

RHEL 6 x64:
% python ./install/install_altinstall.py --pip --os redhat --arch x64

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

Ubuntu x86:
% python ./install/install.py --initialize_instance --os ubuntu --arch x86

Ubuntu x64:
% python ./install/install.py --initialize_instance --os ubuntu --arch x64

RHEL 6 x64:
% python ./install/install_altinstall.py --initialize_instance --os redhat --arch x64

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

Ubuntu x86:
% python ./install/install.py --update_instance --os ubuntu --arch x86

Ubuntu x64:
% python ./install/install.py --update_instance --os ubuntu --arch x64

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

The timestamp in log file names breaks down as follows:
    year (4 places)
    month (2 places)
    day (2 places)
    hour (2 places)
    minute (2 places)
    second (2 places)
    microsecond (6 places)

For example, a log file called install_dependencies_20130413061210254269
was created in 2013 on April 13 at 06:12 hours, 10 seconds, and 254269 microseconds.
