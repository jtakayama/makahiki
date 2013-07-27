ubuntu_readme.txt
=================

Contents:
-------------------------------------------------------------------------------
0.0. Introduction
1.0. Installing and Configuring Dependencies
1.1. Instructions
1.1.1. Check Prerequisites
1.1.2. Install System Environment Dependencies
1.1.3. Set Up the "makahiki" Virtual Environment
1.1.4. PostgreSQL Configuration
1.1.5. Install Dependencies With Pip
1.1.6. Environment Variables Configuration
1.1.7. Initialize Makahiki
1.1.8. Start the Server
1.1.9. Update the Makahiki Instance
Appendix A. Notes on Log Files
-------------------------------------------------------------------------------

0.0. Introduction
===============================================================================
This is a README file for the Makahiki installation scripts.

The ubuntu_installer.py script calls a set of Python scripts which partially 
automate the process of installing Makahiki on Ubuntu Linux x86 and
Ubuntu Linux x64.

The scripts rely on the apt package manager. Other Debian-based systems 
have not been tested - use at your own risk.

If you would prefer to install Makahiki manually, see 
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html.

Makahiki source code is available from https://github.com/csdl/makahiki.

WARNING:
-------------------------------------------------------------------------------
This script should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

WARNING:
-------------------------------------------------------------------------------
If the default version of Python on your system is not a version of Python 2.7 
that is 2.7.3 or higher (but not Python 3), the ubuntu_installer.py file, and 
this guide, will not work for you. 

If you are using Ubuntu Linux 12.04.1 LTS or higher, Python 2.7.3, or a higher 
version of Python 2.7, should be the system default. If this is not the case, 
you will need to:
1. Build and install Python 2.7.3 as an altinstall, manually
2. Install packages manually with apt.
3. Install Python packages (easy_install, pip, virtualenvwrapper).
-------------------------------------------------------------------------------
===============================================================================

1.0. Installing and Configuring Dependencies
===============================================================================
The install/ folder contains the ubuntu_installer.py script.

Usage of ubuntu_installer.py:
-------------------------------------------------------------------------------
./ubuntu_installer.py < --dependencies | --pip | --initialize_instance | 
                        --update_instance > --os < ubuntu > 
                        --arch < x86 | x64 >
                        
All options require Python 2.7.3 or higher (but not Python 3) to run.
    
    --dependencies: Installs dependencies. This script must be run with root 
      privileges.

    --pip: Runs "pip install -r requirements.txt." The requirements.txt file 
      is located in the top-level makahiki directory.

    --initialize_instance: Initializes the Makahiki instance with default 
      options.

    --update_instance: Runs the makahiki/scripts/update_instance.py script 
      with default options.
    
    --os: This script supports ubuntu (Ubuntu Linux).
    
    --arch: This script supports Ubuntu x86 and x64 architectures.
-------------------------------------------------------------------------------
===============================================================================

1.1. Instructions
===============================================================================
In these instructions, a % represents your terminal prompt.

It is assumed that your Makahiki installation is placed in your user home 
directory. For a user named "robot," the user home directory would be 
/home/robot, and the makahiki directory would be at /home/robot/makahiki.
===============================================================================

1.1.1. Check Prerequisites
===============================================================================
(1.) Python 2.7.3 or higher (Not Python 3)
At a minimum, you need to have Python 2.7.3 or higher (but not Python 3) 
installed. Use python --version in the terminal to check the version of 
your default Python installation:

% python --version

Ubuntu versions 12.04.1 LTS and later LTS versions come with Python 2.7.3 
installed by default. If Python 2.7.3, or a higher version of Python 2.7, is 
not the default Python installation on your system, you will need to download 
the source tarball from python.org and install it as an altinstall. The 
ubuntu_installer.py script does not support installing Makahiki dependencies 
to an altinstall.

(2.) Internet connection
Makahiki setup requires an Internet connection.
===============================================================================

1.1.2. Install System Environment Dependencies:
===============================================================================
Switch to your top-level makahiki directory:
% cd ~/makahiki

Run the script with the options specified for your operating system:

Ubuntu x86:
% sudo ./install/ubuntu_installer.py --dependencies --os ubuntu --arch x86

Ubuntu x64:
% sudo ./install/ubuntu_installer.py --dependencies --os ubuntu --arch x86

The script installs these packages and their dependencies:
- git
- gcc
- python-setuptools
- pip
- Python Imaging Library
  - python-dev
  - python-imaging
  - libjpeg-dev
  - This also creates symbolic links to libz.so and libjpeg.so 
    in /usr/lib/. The symbolic links are different for each architecture.
    Ubuntu x86: 
    1. /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so
    2. /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so
    Ubuntu x64:
    1. /usr/lib/libjpeg.so --> /usr/lib/x86_64-linux-gnu/libjpeg.so
    2. /usr/lib/libz.so --> /usr/lib/x86_64-linux-gnu/libz.so 
- PostgreSQL 9.1
  - postgresql-9.1
  - libpq-dev
- memcached
- libmemcached-dev
- virtualenvwrapper

The script also appends lines to the end of the current user's .bashrc 
file (~/.bashrc). The example below uses a user named "robot":
# Virtualenvwrapper settings for makahiki
export WORKON_HOME=home/robot/.virtualenvs
export PROJECT_HOME=home/robot/makahiki
source /usr/local/bin/virtualenvwrapper.sh

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_dependencies_<timestamp>.log," where <timestamp> is a 
sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.
===============================================================================

1.1.3. Set Up the "makahiki" Virtual Environment
===============================================================================
When the ubuntu_installer.py script finishes, source the ~/.bashrc file:

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

For further instructions, see the Makahiki documentation for section 
2.1.1.1.1.6, "Install Virtual Environment Wrapper":
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html#install-virtual-environment-wrapper
===============================================================================

1.1.4. PostgreSQL Configuration
===============================================================================
The next step is to configure the PostgreSQL server authentication settings.

On Ubuntu 12.04.1 LTS and later, the pg_hba.conf file is usually located at 
/etc/postgresql/9.1/main/pg_hba.conf. Open it in a text editor with sudo (root) 
privileges:
% sudo nano /etc/postgresql/9.1/main/pg_hba.conf

To configure PostgreSQL, edit the "local all postgres", "local all all", 
"host all all 127.0.0.1/32", and "host all all ::1/128" lines in the 
pg_hba.conf file to match the below example:
-------------------------------------------------------------------------------
# Database administrative login by Unix domain socket
local   all             postgres                                trust

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
-------------------------------------------------------------------------------

After you have edited the pg_hba.conf file, restart the Postgresql service:
% sudo /etc/init.d/postgresql restart
 * Restarting PostgreSQL 9.1 database server                             [ OK ]
===============================================================================
   
1.1.5. Install Dependencies With Pip
===============================================================================
You should still be in the makahiki virtual environment.

Switch to the makahiki directory:
% cd ~/makahiki

Run the script with the options specified for your operating system:

Ubuntu x86:
% ./install/ubuntu_installer.py --pip --os ubuntu --arch x86

Ubuntu x64:
% ./install/ubuntu_installer.py --pip --os ubuntu --arch x64

The list of packages that this step will attempt to install with pip are 
listed in the makahiki/requirements.txt file.

After it attempts to install the packages, the script will check that 
the correct versions were installed.

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_pip_<timestamp>.log," where <timestamp> is a sequence of 
numbers representing a timestamp in the system local time. For more information, 
see Appendix A.
===============================================================================

1.1.6. Environment Variables Configuration
===============================================================================
The environment variables MAKAHIKI_DATABASE_URL and MAKAHIKI_ADMIN_INFO need 
to be added to the shell environment. To make them permanently available 
whenever you "workon makahiki," add these variables to the 
$WORKON_HOME/makahiki/bin/postactivate file:

# Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki

# Syntax: <admin_name>:<admin_password>
export MAKAHIKI_ADMIN_INFO=admin:admin

Production instances of Makahiki should change the <admin_password> to something 
other than "admin."

You will need to do "workon makahiki" after you have edited the postactivate file
for the changes to take effect:

% workon makahiki
===============================================================================

1.1.7. Initialize Makahiki
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
any subsequent configuration modifications will be lost if ubuntu_installer.py 
is invoked with --initialize_instance again. Use the --update_instance option 
(discussed in Section 1.1.9, below) to update source code without losing 
subsequent configuration actions.

The script initializes the Makahiki database and populates it with default 
information and users. It is equivalent to running the standalone 
makahiki/makahiki/scripts/initialize_instance.py script with 
"--type default" options.
-------------------------------------------------------------------------------

Run the script with the options specified for your operating system:

Ubuntu x86:
% ./install/ubuntu_installer.py --initialize_instance --os ubuntu --arch x86

Ubuntu x64:
% ./install/ubuntu_installer.py --initialize_instance --os ubuntu --arch x64

You will need to answer "Y" to the question "Do you wish to continue (Y/n)?"

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_initialize_instance_<timestamp>.log," where <timestamp> is 
a sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.
===============================================================================

1.1.8. Start the Server
===============================================================================
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
===============================================================================

1.1.9. Update the Makahiki Instance
===============================================================================
Makahiki is designed to support post-installation updating of your configured 
system when bug fixes or system enhancements become available. Updating an 
installed Makahiki instance using the ubuntu_installer.py script requires the 
following steps:

(1.) Close the running server in the shell process that is running Makahiki:
% (type control-c in the shell running the makahiki server process)

(2.) In the current shell or a new shell, go to the makahiki directory and 
     set up the Makahiki virtual environment:
% cd ~/makahiki
% workon makahiki

(3.) Download the updated source code into the Makahiki installation:
% git pull origin master

(4.) Run the ubuntu_installer.py script with --update_instance:

Run the script with the options specified for your operating system:

Ubuntu x86:
% python ./install/ubuntu_installer.py --update_instance --os ubuntu --arch x86

Ubuntu x64:
% python ./install/ubuntu_installer.py --update_instance --os ubuntu --arch x64

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
Log files are created by ubuntu_installer.py in makahiki/install/logs.
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
===============================================================================