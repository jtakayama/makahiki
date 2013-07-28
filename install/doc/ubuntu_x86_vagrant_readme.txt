ubuntu_x86_vagrant_readme.txt
=============================

Contents:
-------------------------------------------------------------------------------
0.0. Introduction
1.0. VirtualBox and Vagrant Setup
1.0.1. Install VirtualBox
1.0.2. Install Vagrant
2.0. Vagrant Virtual Machine Setup
2.0.1. Virtual Machine Setup
2.0.2. Download the Makahiki Source Code
2.0.3. Copy Setup Files
2.0.4. Download the Base Virtual Machine
2.1. Set up Makahiki in the Virtual Machine
2.1.1. Start the Virtual Machine and Run the Provisioning Script
2.1.2. Connect to the Vagrant Virtual Machine with SSH
2.1.3. Download the Makahiki Source Code
2.1.4. Apply .bashrc Changes
2.1.5. Set Up the "makahiki" Virtual Environment
2.1.6. PostgreSQL Configuration
2.1.7. Install Dependencies With Pip
2.1.8. Environment Variables Configuration
2.1.9. Initialize Makahiki [BUG TENTATIVELY RESOLVED]
2.1.10. Start the Server
2.1.11. Update the Makahiki Instance
2.1.12. Optional: Configure the RAM of the Virtual Machine
2.1.13. Optional: Re-Provisioning Vagrant
Appendix A. Notes on Log Files
Appendix B. Vagrant Commands
-------------------------------------------------------------------------------

0.0. Introduction
===============================================================================
This is a README file that describes the process for deploying Makahiki in a 
Vagrant virtual machine on a Windows host machine.

If you would prefer to install Makahiki on Windows manually, without using 
Vagrant, see the documentation at:
http://makahiki.readthedocs.org/en/latest/installation-makahiki-windows.html

The Makahiki source code is available from https://github.com/csdl/makahiki.

In the examples in this document, the > represents the Windows command prompt.

This guide assumes a basic level of familiarity with Windows.

WARNING:
-------------------------------------------------------------------------------
This guide should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

System requirements:
- Operating System:
  - Windows 7 or 8 are recommended.
  - The applications used in this guide are compatible with 
    x86 (32-bit) and x64 (64-bit) architectures.
- Hardware:
  - CPU: Modern dual or quad core
  - RAM: 4 GB
  - The Vagrant virtual machine will be configured by default to have 1.5 GB 
    of RAM (1536 MB). To change this amount, see Section 2.1.12.
===============================================================================

1.0. VirtualBox and Vagrant Setup
===============================================================================
This section installs VirtualBox and Vagrant onto a Windows computer.
===============================================================================

1.0.1. Install VirtualBox
===============================================================================
Download VirtualBox from https://www.virtualbox.org/wiki/Downloads.
To install VirtualBox on Windows, follow the instructions at 
https://www.virtualbox.org/manual/ch02.html#installation_windows.

Select "Yes" when you are asked to install drivers for USB support and 
VirtualBox Host-Only Networking.

This guide was tested with VirtualBox 4.2.16.
===============================================================================

1.0.2. Install Vagrant
===============================================================================
Download the Vagrant .msi installer from http://downloads.vagrantup.com/.
To install Vagrant on Windows, follow the instructions at 
http://docs.vagrantup.com/v2/installation/index.html.

This guide was tested with Vagrant 1.2.4.
===============================================================================

2.0. Vagrant Virtual Machine Setup 
===============================================================================
This section contains instructions for creating the Vagrant virtual machine.

Open a Windows Command Prompt (cmd) terminal window. (If you can't find the 
Command Prompt, type "cmd.exe" in Run.) This terminal will be used to configure 
and access the Vagrant virtual machine.
===============================================================================

2.0.1. Virtual Machine Setup
===============================================================================
First, create a new directory for your Vagrant virtual machine. This guide 
uses the example directory "ubuntu_x86_makahiki." A Vagrant virtual machine 
can be "placed" anywhere. The virtual machine files will not really be located 
here, but you will issue Vagrant commands for the virtual machine in this 
directory.

> mkdir ubuntu_x86_makahiki
> cd ubuntu_x86_makahiki
===============================================================================

2.0.2. Download the Makahiki Source Code
===============================================================================
There are two ways of obtaining the Makahiki source code. (If you have this 
text file, you likely already have the Makahiki source code and can skip this 
section.)

This guide assumes that you will be placing the source code in the 
ubuntu_x86_makahiki directory.

A. If you do not have Git for Windows, download the source code from 
   Github as a .zip file:
    A1. In a web browser, go to https://github.com/csdl/makahiki.
    A2. Click the button to "Download ZIP."
    A3. Extract the makahiki.zip file that is downloaded.
    A4. Copy or move the resulting "makahiki" directory to your 
        ubuntu_x86_makahiki directory.

B. If you have Git for Windows, you can clone the repository:
   B1. If you are not in it, change to the "ubuntu_x86_makahiki" directory.
   B2. Clone the repository into this directory:
> git clone http://github.com/csdl/makahiki.git

Git for Windows can be downloaded from http://git-scm.com/download/win.
===============================================================================

2.0.3. Copy Setup Files
===============================================================================
Copy some configuration files and the logs/ directory to the current 
ubuntu_x86_makahiki directory from the makahiki directory:

> cd makahiki\install
> copy_ubuntu_scripts.bat
> cd ../../

On the Vagrant virtual machine, the ubuntu_x86_makahiki directory will be 
the /vagrant directory, which is shared with the virtual machine.
===============================================================================

2.0.4. Download the Base Virtual Machine
===============================================================================
This step adds the base virtual machine specified in the last step, 
"precise32," for Vagrant to use. (Replace "precise32" with whatever 
value you specified for config.vm.box in the last step.)

> vagrant box add precise32 http://files.vagrantup.com/precise32.box

This will download the virtual machine from Vagrant's servers.

It is only necessary to download each specific box once; if you create more 
virtual machines with the same base box ("precise32"), you can skip this step.
===============================================================================

2.1. Set up Makahiki in the Virtual Machine
===============================================================================
Section 2.1's subsections describe the process of configuring Makahiki in 
the virtual machine. 
===============================================================================

2.1.1. Start the Virtual Machine and Run the Provisioning Script
===============================================================================
Use the "vagrant up" command to start the virtual machine:

> vagrant up

Each time you start Vagrant with "vagrant up," it will run the 
"bootstrap_runner.sh" script specified in the Vagrantfile. This 
script runs and logs the "bootstrap.sh" script.

(Later, if you want to start the virtual machine without provisioning 
 it, use --no-provision: vagrant up --no-provision)

The bootstrap.sh script: 
1. Updates the apt package lists
2. Sets the system encoding to en_US.UTF8
3. Installs the following packages and their dependencies:
    git
    gcc
    python-setuptools
    pip
    Python Imaging Library
    - python-dev
    - python-imaging
    - libjpeg-dev
    - Creates symbolic links to libz.so and libjpeg.so in /usr/lib:
      1. /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so
      2. /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so
    PostgreSQL 9.1
    - postgresql-9.1
    - libpq-dev
    memcached
    libmemcached-dev
    virtualenvwrapper
4. Appends virtualenv settings to /home/vagrant/.bashrc
5. Initializes the postgresql cluster data directory with en_US.UTF-8 encoding

The bootstrap_runner.sh script logs the output of bootstrap.sh to a text 
file in the logs directory. This file is called "ubuntu_x86_<timestamp>.log,"
where <timestamp> is in the format yyyy-mm-dd-HH-MM-SS (year, month, day, 
hour, minute, second).
===============================================================================

2.1.2. Connect to the Vagrant Virtual Machine with SSH
===============================================================================
When the script is finished, use "vagrant ssh" to start an SSH connection to 
the virtual machine in the Command Prompt:
-------------------------------------------------------------------------------
> vagrant ssh
Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic-pae i686)

 * Documentation:  https://help.ubuntu.com/
Welcome to your Vagrant-built virtual machine.
Last login: Fri Sep 14 06:22:31 2012 from 10.0.2.2
vagrant@precise32:~$
-------------------------------------------------------------------------------
The SSH session will log you in as the "vagrant" user, in the "vagrant" user's 
home directory, /home/vagrant (the current user's home directory is also 
referred to as ~). The Ubuntu Linux terminal prompt will look like this:

vagrant@precise32:~$
===============================================================================

2.1.3. Download the Makahiki Source Code
===============================================================================
Assuming that Git installed successfully, clone the CSDL Makahiki repository 
from Github into the vagrant user's home directory:

vagrant@precise32:~$ git clone http://github.com/csdl/makahiki.git
===============================================================================

2.1.4. Apply .bashrc Changes
===============================================================================
bootstrap.sh appended these lines to the "vagrant" user's .bashrc file:
-------------------------------------------------------------------------------
# Virtualenvwrapper settings for makahiki
export WORKON_HOME=/home/vagrant/.virtualenvs
export PROJECT_HOME=/home/vagrant/makahiki
source /usr/local/bin/virtualenvwrapper.sh
-------------------------------------------------------------------------------
Source the .bashrc file in order for the changes to take effect.

vagrant@precise32:~$ source .bashrc
===============================================================================

2.1.5. Set Up the "makahiki" Virtual Environment
===============================================================================
Switch to the top-level makahiki directory:

vagrant@precise32:~$ cd makahiki

Then, create the makahiki virtual environment: 

vagrant@precise32:~/makahiki$ mkvirtualenv makahiki

Creating a virtual environment should switch you to the virtual environment.
The terminal prompt will be preceded by the name of the virtual environment.
On Ubuntu, this looks like:

(makahiki)vagrant@precise32:~/makahiki$

If creating the virtual environment did not switch you to the virtual 
environment, use "workon" to switch to it:

vagrant@precise32:~/makahiki$ workon makahiki
(makahiki)vagrant@precise32:~/makahiki$
===============================================================================

2.1.6. PostgreSQL Configuration
===============================================================================
The next step is to configure the PostgreSQL server authentication settings.
Run the md5test_ubuntu_pg_hba_conf.sh script to replace the default settings 
with Makahiki settings:
(makahiki)vagrant@precise32:~/makahiki sudo sh /vagrant/md5test_ubuntu_pg_hba_conf.sh

If the script succeeds, you will see this message:
"Checksums match. pg_hba.conf will be overwritten with Makahiki settings."
"sudo cp /vagrant/pg_hba.conf.ubuntu.makahiki /etc/postgresql/9.1/main/pg_hba.conf"
"pg_hba.conf copy succeeded. [ OK ]"

If the script was edited previously and matches the Makahiki settings, you will 
see this message:
"pg_hba.conf file already overwritten with makahiki settings. [ OK ]"

If you see either of these messages, the correct settings have been applied.
Now, restart the Postgresql service:
(makahiki)vagrant@precise32:~/makahiki$ sudo /etc/init.d/postgresql restart

IF THE SCRIPT FAILS:
-------------------------------------------------------------------------------
If the pg_hba.conf file is different from the expected file, you will 
see this message indicating that the script has failed:
"WARNING! pg_hba.conf default file is different from expected file."
 File could not be safely overwritten with Makahiki defaults.
 You will need to edit it manually."
If this happens, follow the instructions below.

On Ubuntu 12.04 LTS, pg_hba.conf is at /etc/postgresql/9.1/main/pg_hba.conf. 
Open it in a text editor with sudo (root) privileges:

(makahiki)vagrant@precise32:~/makahiki$ sudo nano /etc/postgresql/9.1/main/pg_hba.conf

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
(makahiki)vagrant@precise32:~/makahiki$ sudo /etc/init.d/postgresql restart
-------------------------------------------------------------------------------
===============================================================================

2.1.7. Install Dependencies With Pip
===============================================================================
You should still be in the makahiki virtual environment.

If you are not currently in the top-level makahiki directory 
(/home/vagrant/makahiki in this guide), switch to it:
(makahiki)vagrant@precise32:~/$ cd ~/makahiki

Run the script with the options specified for your operating system:
(makahiki)vagrant@precise32:~/makahiki$ ./install/ubuntu_installer.py --pip --os ubuntu --arch x86

The list of packages that this step will attempt to install with pip are 
listed in the makahiki/requirements.txt file.

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_pip_<timestamp>.log," where <timestamp> is a sequence of 
numbers representing a timestamp in the system local time. For more information, 
see Appendix A.
==============================================================================

2.1.8. Environment Variables Configuration
==============================================================================
The next step is to configure the Makahiki environment variables.
Run the md5test_ubuntu_postactivate.sh script to replace the default settings 
with Makahiki settings:
(makahiki)vagrant@precise32:~/makahiki sh /vagrant/md5test_ubuntu_postactivate.sh

If the script succeeds, you will see this message:
"Checksums match. postactivate will be overwritten with Makahiki settings."
"sudo cp /vagrant/postactivate.makahiki $WORKON_HOME/makahiki/bin/postactivate"
"postactivate copy succeeded. [ OK ]"

If the script was edited previously and matches the Makahiki settings, you 
will see this message:
"postactivate file already overwritten with makahiki settings. [ OK ]"

If you see either of these messages, the correct settings have been applied.
Now, apply the new virtual environment settings:
(makahiki)vagrant@precise32:~/makahiki$ workon makahiki

IF THE SCRIPT FAILS:
-------------------------------------------------------------------------------
If the postactivate file is different from the expected file, you will 
see this message indicating that the script has failed:
"WARNING! postactivate default file is different from expected file."
 File could not be safely overwritten with Makahiki defaults.
 You will need to edit it manually."
If this happens, follow the instructions below.

Edit $WORKON_HOME/bin/makahiki/postactivate:
(makahiki)vagrant@precise32:~/makahiki$ nano $WORKON_HOME/makahiki/bin/postactivate

Add these lines to the end of the file:
------------------------------------------------------------------------------
# Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki

# Syntax: <admin_name>:<admin_password>
export MAKAHIKI_ADMIN_INFO=admin:admin
------------------------------------------------------------------------------
Production instances of Makahiki should change the <admin_password> to something 
other than "admin."

You will need to do "workon makahiki" for the changes to take effect:

(makahiki)vagrant@precise32:~/makahiki$ workon makahiki
===============================================================================

2.1.9. Initialize Makahiki [BUG TENTATIVELY RESOLVED]
===============================================================================
You should still be in the makahiki virtual environment.

If you are not currently in the top-level makahiki directory 
(/home/vagrant/makahiki in this guide), switch to it:
(makahiki)vagrant@precise32:~/$ cd ~/makahiki

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
(makahiki)vagrant@precise32:~/makahiki$ ./install/ubuntu_installer.py --initialize_instance --os ubuntu --arch x86

You will need to answer "Y" to the question "Do you wish to continue (Y/n)?"

The script will create a log file in makahiki/install/logs with a filename of 
the format "install_initialize_instance_<timestamp>.log," where <timestamp> is 
a sequence of numbers representing a timestamp in the system local time. 
For more information, see Appendix A.
===============================================================================

2.1.10. Start the Server
===============================================================================
You should still be in the makahiki virtual environment.

Switch to the makahiki/makahiki directory:
(makahiki)vagrant@precise32:~/makahiki$ cd makahiki

You can now start the web server using manage.py or gunicorn. The manage.py 
web server is better for development, while gunicorn is better for production 
use.

To start the server with manage.py:
(makahiki)vagrant@precise32:~/makahiki/makahiki$ ./manage.py runserver

To start the server with gunicorn:
(makahiki)vagrant@precise32:~/makahiki/makahiki$ ./manage.py run_gunicorn

View the site in your host machine's web browser at http://localhost:8080.
===============================================================================

2.1.11. Update the Makahiki Instance
===============================================================================
Makahiki is designed to support post-installation updating of your configured 
system when bug fixes or system enhancements become available. Updating an 
installed Makahiki instance using the ubuntu_installer.py script requires the 
following steps (the % represents a Linux terminal prompt):

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

2.1.12. Optional: Re-Provisioning Vagrant
===============================================================================
If you are developing for Makahiki using a Vagrant virtual machine and change 
the provisioning scripts (bootstrap.sh or run_bootstrap.sh), you will need 
to provision the virtual machine again. You can do this in one of two ways.

A. Re-provision the virtual machine on startup with "vagrant up":
In the ubuntu_x86_makahiki folder, start the virtual machine with "vagrant up."
This will run the provisioning script designated in the Vagrantfile.
> vagrant up 

B. Re-provision a virtual machine that is already running:
> vagrant provision
===============================================================================

2.1.13. Optional: Configure the RAM of the Virtual Machine
===============================================================================
The default settings in the Vagrantfile that comes with this project limit 
the virtual machine to 1536 MB (1.5 GB) of RAM. To change these settings, you 
will need to edit the Vagrantfile while the virtual machine is shut down.

Stop the web server by pressing Ctrl-C in the SSH terminal.
Then shut down the virtual machine:
(makahiki)vagrant@precise32:~/makahiki/makahiki$ sudo shutdown -h now

This will end the SSH session.

To increase the RAM allocated to the Virtualbox VM, edit the "vb.customize" 
line in the Vagrantfile by changing the number after the "--memory" flag.
-------------------------------------------------------------------------------
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", 1536]
  end
-------------------------------------------------------------------------------

After saving your changes, restart the VM and start the SSH session:
> vagrant up --no-provision
> vagrant ssh

In the SSH session, switch to makahiki/makahiki, activate the virtual 
environment, and start the server with manage.py:
vagrant@precise32:~$ workon makahiki
(makahiki)vagrant@precise32:~$ cd makahiki/makahiki
(makahiki)vagrant@precise32:~/makahiki/makahiki$ ./manage.py runserver
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

Appendix B. Vagrant Commands
===============================================================================
vagrant up: Start the virtual machine and run the provisioning script.
            If the virtual machine defined in the Vagrantfile does 
            not exist, it will be created.
            (Use up --no-provision to start the machine without 
             provisioning it.)
vagrant suspend: Freeze the current state of the virtual machine.
vagrant resume: Reactivate a machine that has been suspended.
vagrant halt: Attempt to shut down the virtual machine gracefully.
              (Use halt --force to force a shutdown. This is equivalent 
               to pulling the plug on an actual computer.)
vagrant status: Show the status of the virtual machine.
vagrant destroy: Deletes a virtual machine. The Vagrantfile remains.

The Vagrant 1.2 documentation can be found at http://docs.vagrantup.com/v2/.
===============================================================================