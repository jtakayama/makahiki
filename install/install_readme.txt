install_readme.txt
==================

This is a README file for the Makahiki installation scripts.

The install.py script calls a set of Python scripts which partially 
automate the process of installing Makahiki on Ubuntu Linux x86, 
Ubuntu Linux x64, and Red Hat Enterprise Linux 6 (RHEL 6) x64.

Makahiki is available at https://github.com/csdl/makahiki.

The install/ folder contains the install.py script and its dependencies.
install.py:
----------
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

Instructions
------------
In these instructions, a % represents your terminal prompt.

It is assumed that your Makahiki installation is placed in your user home directory.
For a user named "robot," the user home directory would be /home/robot,
and the makahiki directory would be at /home/robot/makahiki.

1. Install system environment dependencies:
-------------------------------------------
Assuming you started in your top-level makahiki directory, 
switch to the makahiki/install directory:
% cd ~/makahiki/install

Run the script with the following options according to 
your operating system:

Ubuntu x86:
% sudo python install.py --dependencies --os ubuntu --arch x86

Ubuntu x64:
% sudo python install.py --dependencies --os ubuntu --arch x86

RHEL 6 x64:
% sudo python install.py --dependencies --os redhat --arch x64

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

2. Set up the makahiki virtual environment:
------------------------------------------- 
Switch to the top-level makahiki directory:
% cd ~/makahiki

When the environment_setup.sh script finishes, reload the startup file: 

% source ~/.bashrc

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
[Work in progress]
