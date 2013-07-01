ubuntu_x86_script_readme.txt
============================

This is the README file for the two Makahiki local installation scripts 
in the makahiki/environmentsetup/ubuntu_x86 directory.

Table of Contents
-----------------
1.0.0. Usage of the scripts
|__1.1.0. Prerequisites
|____1.1.0.1. Prerequisites: Python
|____1.1.0.2. Prerequisites: Git
|____1.1.0.3. Prerequisites: Download Makahiki
|__1.1.1. Run environment_setup.sh
|____1.1.1.1. Packages that will be installed
|____1.1.1.2. Changes to .bashrc
|__1.1.2. Configure makahiki virtual environment
|__1.1.3. Run pip_install.sh
|____1.1.3.1. Packages that will be installed
|__1.1.4. Post-install setup instructions

1.0.0. Usage of the scripts
---------------------------
These scripts automate parts of the Makahiki installation process. The full 
Unix installation process without use of the scripts is documented at 
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html.

1.1.0. Prerequisites
--------------------
These shell scripts are intended for use on the Ubuntu Linux 32-bit (x86) 
operating system. Debian-based 32-bit distributions which use apt as their 
package manager may also work, but have not been tested.

environment_setup.sh and pip_install.sh both require an Internet connection.

1.1.0.1. Prerequisites: Python
------------------------------
Python 2.7.3 or higher (but not Python 3) should be installed. To check 
your Python version, type

python --version

in the terminal.

The environment_setup.sh script will ask the user if Python 2.7.3 or 
higher (not Python 3) is installed.

1.1.0.2. Prerequisites: Git
---------------------------
The rest of this guide presents terminal examples using the user "robot" 
on a computer called "computer."

The scripts are part of Makahiki, which is normally obtained by cloning 
its repository from Github using Git. It is likely that Git is already 
installed and configured on your system. Check your git version:

robot@computer:~$ git --version

If not, install Git: 
robot@computer:~$ sudo apt-get install git

Next, configure Git by setting a global username and email 
to use in commits to repositories. The below example demonstrates how to do 
this for a user with username robot and email robot@example.com:

robot@computer:~$ git config --global user.name robot
robot@computer:~$ git config --global user.email robot@example.com

If you are developing software using Makahiki and / or will be committing to a 
Github repository, the username and email should match your Github username 
and email. Full setup instructions for using Git with a Github account can be 
found at https://help.github.com/articles/set-up-git.

1.1.0.3. Prerequisites: Download Makahiki
-----------------------------------------
Both script files are part of Makahiki. If you are reading this file, you 
have probably already downloaded Makahiki, and can skip to the next section.

Use Git to clone the Makahiki repository from Github. Both scripts assume by 
default that you will be cloning the repository to your user home directory. 
This will create a new folder and download the code from the repository.

If not, go to the user's home directory and clone the repository:

robot@computer:~$ cd ~/
robot@computer:~$ git clone git://github.com/csdl/makahiki.git

The rest of this guide assumes that Makahiki was cloned to the user's 
home directory, into the folder "makahiki."

Switch to the makahiki directory:

robot@computer:~$ cd makahiki
robot@computer:~/makahiki$

1.1.1. Run environment_setup.sh
-------------------------------
You should be in the makahiki directory (makahiki, not makahiki/makahiki).
This guide assumes the makahiki folder is in the user's home directory. 

Do not run environment_setup.sh with sudo. The script will use sudo commands 
on its own.

robot@computer:~/makahiki$ sh environmentsetup/ubuntu_x86/environment_setup.sh

For a list of packages that will be installed, see the next section, 1.1.1.1.

1.1.1.1. Packages that will be installed
----------------------------------------
The environment_setup.sh script will install the latest available versions of 
these packages and their dependencies:
1. gcc
2. python-setuptools
3. pip
4. virtualenvwrapper
5. Python Imaging Library: 
   - python-imaging
   - python-dev
   - libjpeg-dev
6. postgresql-9.1
7. libpq-dev
8. Memcached: 
   - memcached
   - libmemcached-dev

1.1.1.2. Changes to .bashrc
---------------------------
The script will ask you for the directory you have cloned Makahiki to.
The default is <user home directory>/makahiki (e.g., home/robot/makahiki). 
Based on this, three lines will be appended to the .bashrc file in your user 
home directory: 

export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/makahiki
source /usr/local/bin/virtualenvwrapper.sh

1.1.2. Configure makahiki virtual environment
---------------------------------------------
When the environment_setup.sh script finishes, reload the startup file: 

robot@computer:~/makahiki$ source ~/.bashrc

Then, create the makahiki virtual environment: 

robot@computer:~/makahiki$ mkvirtualenv makahiki

Creating a virtual environment should switch you to the virtual environment.
The terminal prompt will be preceded by the name of the virtual environment: 

(makahiki)robot@computer:~/makahiki$

If creating the virtual environment did not switch you to the virtual 
environment, use "workon" to switch to it:

robot@computer:~/makahiki$ workon makahiki
(makahiki)robot@computer:~/makahiki$

For further instructions, see the Makahiki documentation for section 
2.1.1.1.1.6, "Install Virtual Environment Wrapper":
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html#install-virtual-environment-wrapper

1.1.3. Run pip_install.sh
-------------------------
You should be in the makahiki directory (makahiki, not makahiki/makahiki). 
This guide assumes the makahiki folder is in the user's home directory.
If you have been following this guide, you should be in the virtual environment. 
If not, switch to the virtual environment:

robot@computer:~/makahiki$ workon makahiki
(makahiki)robot@computer:~/makahiki$

Do not run pip_install.sh with sudo. To run pip_install.sh:

(makahiki)robot@computer:~/makahiki$ sh environmentsetup/ubuntu_x86/pip_install.sh

The script will ask you to confirm that you have:
(1) Run the environment_setup.sh file previously 
(2) Created the makahiki virtual environment 
(3) run the script in the makahiki virtual environment.

If you have been following this guide, answer Y (yes) to all. After this, 
pip will begin to install packages. 

It is normal for pip to produce a lot of output.

1.1.3.1. Packages that will be installed
----------------------------------------
The requirements.txt file in the top-level makahiki directory (in makahiki, 
not in makahiki/makahiki) lists the packages that pip will install in the 
local directory. These will only be installed for makahiki, not for the 
entire operating system.

1.1.4. Post-install setup instructions
--------------------------------------
After completing both scripts, you must configure PostgreSQL, set up 
environment variables, initialize Makahiki, and start the Makahiki server. 

To configure PostgreSQL, go to the Makahiki documentation and follow 
section 2.1.1.1.1.8, "Install PostgreSQL," to edit the pg_hba.conf file:
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html#install-postgresql

To set up environment variables, initialize Makahiki, and start the Makahiki 
server, follow the Makahiki documentation starting from section 2.1.1.1.1.13, 
"Setup environment variables," and continue until the end of the page:
https://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html#setup-environment-variables
