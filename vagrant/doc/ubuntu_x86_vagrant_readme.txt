ubuntu_x86_vagrant_readme.txt
=============================

Contents:
-------------------------------------------------------------------------------
0.0. Introduction
1.0. VirtualBox and Vagrant Setup
1.0.1. Install VirtualBox
1.0.2. Install Vagrant
2.0. Vagrant Virtual Machine Setup
2.0.1. Download the Makahiki Source Code
2.0.2. Download the Base Virtual Machine
2.1. Set up Makahiki in the Virtual Machine
2.1.1. Start the Virtual Machine and Run the Provisioning Script
2.1.2. Connect to the Vagrant Virtual Machine with SSH
2.1.3. Download the Makahiki Source Code
2.1.4. Environment Variables Verification
2.1.5. PostgreSQL Configuration Verification
2.1.7. Install Dependencies With Pip
2.1.8. Environment Variables Configuration
2.1.9. Initialize Makahiki
2.1.10. Start the Server
2.1.11. Update the Makahiki Instance
Appendix A. Vagrant Commands
Appendix B. Re-Provisioning Vagrant
Appendix C. Configure the RAM of the Virtual Machine
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

2.0.1. Download the Makahiki Source Code
===============================================================================
Downloading the Makahiki source code will create a folder called "makahiki."

There are two ways of obtaining the Makahiki source code. (If you have this 
text file, you likely already have the Makahiki source code and can skip this 
section.)

A. If you do not have Git for Windows, download the source code from 
   Github as a .zip file:
    A1. In a web browser, go to https://github.com/csdl/makahiki.
    A2. Click the button to "Download ZIP."
    A3. Extract the makahiki.zip file that is downloaded.

B. If you have Git for Windows, you can clone the repository:
   > git clone http://github.com/csdl/makahiki.git

Git for Windows can be downloaded from http://git-scm.com/download/win.

Now switch your working directory to makahiki/vagrant:
> cd makahiki/vagrant
===============================================================================

2.0.2. Download the Base Virtual Machine
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
4. Creates /home/vagrant/makahiki_env.sh, which sets Makahiki environment variables in the shell
5. Edits /home/vagrant/.bashrc so it will source /home/vagrant/makahiki_env.sh
6. Initializes the postgresql cluster data directory with en_US.UTF-8 encoding

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
Check that the bootstrap.sh script downloaded the makahiki repository:
-------------------------------------------------------------------------------
vagrant@precise32:~$ ls
makahiki postinstall.sh
-------------------------------------------------------------------------------
If there is no "makahiki" directory listed in the "ls" output, you will have 
to clone the repository:
vagrant@precise32:~$ git clone http://github.com/csdl/makahiki.git
===============================================================================

2.1.4. Environment Variables Verification
===============================================================================
bootstrap.sh appended this line to the "vagrant" user's .bashrc file:
-------------------------------------------------------------------------------
source /home/vagrant/makahiki_env.sh
-------------------------------------------------------------------------------
makahiki_env.sh sets values for Makahiki environment variables 
MAKAHIKI_DATABASE_URL and MAKAHIKI_ADMIN_INFO. Check that these values 
have been set:
-------------------------------------------------------------------------------
vagrant@precise32:~/makahiki/makahiki$ echo $MAKAHIKI_DATABASE_URL
postgres://makahiki:makahiki@localhost:5432/makahiki
vagrant@precise32:~/makahiki/makahiki$ echo $MAKAHIKI_ADMIN_INFO
admin:admin
-------------------------------------------------------------------------------
If your output matches the example shown above, skip "Troubleshooting" 
and continue.

Troubleshooting:
*******************************************************************************
Source the .bashrc file, then check the variables again:
vagrant@precise32:~/makahiki/makahiki$ source ~/.bashrc
vagrant@precise32:~/makahiki/makahiki$ echo $MAKAHIKI_DATABASE_URL
postgres://makahiki:makahiki@localhost:5432/makahiki
vagrant@precise32:~/makahiki/makahiki$ echo $MAKAHIKI_ADMIN_INFO
admin:admin

If MAKAHIKI_DATABASE_URL and MAKAHIKI_ADMIN_INFO are still not set after 
sourcing ~/.bashrc, you need to add them to /home/vagrant/makahiki_env.sh.
Create this file if it does not exist.

When you are done editing .bashrc, source it:
vagrant@precise32:~/makahiki/makahiki$ source ~/.bashrc
*******************************************************************************

Note:
-----
The username:password combination of admin:admin is meant for use in 
development. In a production server, the value of MAKAHIKI_ADMIN_INFO would be 
changed to a more secure value. To edit this value, edit 
/home/vagrant/makahiki_env.sh.
===============================================================================

2.1.5. PostgreSQL Configuration Verification
===============================================================================
The next step is to verify the PostgreSQL server authentication settings.
At the prompt, type "psql -U postgres." If it succeeds, type \q to quit.
-------------------------------------------------------------------------------
vagrant@precise32:~$ psql -U postgres
psql (9.1.9)
Type "help" for help.

postgres=#\q
vagrant@precise32:~$
-------------------------------------------------------------------------------
If it succeeds, skip "Troubleshooting" and continue.

Troubleshooting:
*******************************************************************************
If you cannot connect to the database with "psql -U postgres," you will need to 
edit the pg_hba.conf file manually.

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
*******************************************************************************
===============================================================================

2.1.9. Initialize Makahiki
===============================================================================
You should still be in the makahiki virtual environment.

WARNING:
-------------------------------------------------------------------------------
Running the initialize_instance.py script will:
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
information and users.
-------------------------------------------------------------------------------

If you are not currently in the second-level makahiki directory 
(/home/vagrant/makahiki/makahiki in this guide), switch to it:
vagrant@precise32:~/$ cd ~/makahiki/makahiki
vagrant@precise32:~/makahiki/makahiki$ ./scripts/initialize_instance.py --type default

You will need to answer "Y" to the question "Do you wish to continue (Y/n)?"
===============================================================================

2.1.10. Start the Server
===============================================================================
You should still be in the makahiki virtual environment. This guide assumes 
you are currently in the directory ~/makahiki/makahiki.

You can now start the web server using manage.py or gunicorn. The manage.py 
web server is better for development, while gunicorn is better for production 
use.

To start the server with manage.py:
(makahiki)vagrant@precise32:~/makahiki/makahiki$ ./manage.py runserver 0.0.0.0:8000

To start the server with gunicorn:
(makahiki)vagrant@precise32:~/makahiki/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000

View the site in your host machine's web browser at http://localhost:8001.
===============================================================================

2.1.11. Update the Makahiki Instance
===============================================================================
Makahiki is designed to support post-installation updating of your configured 
system when bug fixes or system enhancements become available. Updating an 
installed Makahiki instance using the ubuntu_installer.py script requires the 
following steps (the % represents any working directory):

(1.) Close the running server in the shell process that is running Makahiki:
(type control-c in the shell running the makahiki server process)

(2.) Go to the makahiki directory:
% cd ~/makahiki
vagrant@precise32:~/makahiki$

(3.) Download the updated source code into the Makahiki installation:
vagrant@precise32:~/makahiki$ git pull origin master

(4.) Run the update_instance.py script:
vagrant@precise32:~/makahiki$ cd makahiki
vagrant@precise32:~/makahiki/makahiki$ ./scripts/

(5.) Start the server with runserver or gunicorn:
To start the server with manage.py:
% ./manage.py runserver

To start the server with gunicorn:
% ./manage.py run_gunicorn
===============================================================================

Appendix A. Vagrant Commands
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
vagrant destroy: Deletes a virtual machine. The Vagrantfile is not deleted.

The Vagrant 1.2 documentation can be found at http://docs.vagrantup.com/v2/.
===============================================================================

Appendix B. Re-Provisioning Vagrant
===============================================================================
If you are developing for Makahiki using a Vagrant virtual machine and change 
the provisioning scripts (bootstrap.sh or run_bootstrap.sh), you will need 
to provision the virtual machine again. You can do this in one of two ways.

A. Re-provision the virtual machine on startup with "vagrant up":
In the makahiki/vagrant directory, start the virtual machine with "vagrant up."
This will run the provisioning script designated in the Vagrantfile.
> vagrant up 

B. Re-provision a virtual machine that is already running:
> vagrant provision
===============================================================================

Appendix C. Configure the RAM of the Virtual Machine
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