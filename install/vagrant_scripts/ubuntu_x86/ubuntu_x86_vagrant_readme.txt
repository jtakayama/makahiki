ubuntu_x86_vagrant_readme.txt
=============================

Contents:
-------------------------------------------------------------------------------
0.0. Introduction
1.0. Prerequisites
1.0.1. Install VirtualBox
1.0.2. Install Vagrant
2.0. Vagrant Setup
2.0.1. Virtual Machine Setup
2.0.2. Download the Makahiki Source Code
2.0.3. Configure the Vagrantfile's Provisioning Script
2.0.4. Download the Base Virtual Machine
2.0.5. Copy the Provisioning Script Files
2.1. Set up Makahiki in the Virtual Machine
2.1.1. Start the Virtual Machine and Run the Provisioning Script
2.1.2. Connect to the Vagrant Virtual Machine with SSH
2.1.3. Download the Makahiki Source Code
2.1.4. Configure .bashrc Environment Variables
2.1.5. Set Up the "makahiki" Virtual Environment
2.1.6. PostgreSQL Configuration
2.1.7. Install Dependencies With Pip
2.1.8. Environment Variables Configuration
2.1.9. Initialize Makahiki [BUG NOT RESOLVED]
2.1.10. Start the Server
2.1.11. Configure Networking for the Virtual Machine [INCOMPLETE]
2.1.12. Increase the RAM of the Virtual Machine [INCOMPLETE]
2.1.13. Update the Makahiki Instance
2.1.14. Re-Provisioning Vagrant
Appendix A. Notes on Log Files
-------------------------------------------------------------------------------

0.0. Introduction.
===============================================================================
This is a README file that describes the process for deploying Makahiki in a 
Vagrant virtual machine on a Windows host machine.

If you would prefer to install Makahiki on Windows manually, without using 
Vagrant, see the documentation at:
http://makahiki.readthedocs.org/en/latest/installation-makahiki-windows.html

The Makahiki source code is available from https://github.com/csdl/makahiki.

In the examples in this document, the > represents the Windows command prompt.

This guide assumes a basic level of familiarity with Windows and little 
familiarity with Linux.

WARNING:
-------------------------------------------------------------------------------
This guide should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------
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
===============================================================================

1.0.2. Install Vagrant
===============================================================================
Download the Vagrant .msi installer from http://downloads.vagrantup.com/.
To install Vagrant on Windows, follow the instructions at 
http://docs.vagrantup.com/v2/installation/index.html.

This guide was tested with Vagrant 1.2.4.
===============================================================================

2.0. Vagrant Setup 
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

Create the Vagrantfile for the new virtual machine.

> vagrant init
===============================================================================

2.0.2. Download the Makahiki Source Code
===============================================================================
There are two ways of obtaining the Makahiki source code. (If you have this 
text file, you likely already have the Makahiki source code and can skip this 
section.)

A. If you do not have Git for Windows, download the source code from 
   Github as a .zip file:
    A1. In a web browser, go to https://github.com/csdl/makahiki.
    A2. Click the button to "Download ZIP."
    A3. Extract the makahiki.zip file that is downloaded.
    A4. Copy or move the resulting "makahiki" directory to your 
        ubuntu_x86_makahiki directory.

B. If you have Git for Windows, you can clone the repository:
   B1. Change to the "ubuntu_x86_makahiki" directory. 
   B2. Clone the repository into this directory:
> git clone http://github.com/csdl/makahiki.git

Git for Windows can be downloaded from http://git-scm.com/download/win.
===============================================================================

2.0.3. Configure the Vagrantfile's Provisioning Script
===============================================================================
(3) Open the Vagrantfile in a text editor and change the default contents 
   to the following:
-------------------------------------------------------------------------------
Vagrant.configure("2") do |config|
  config.vm.box = "precise32"
  config.vm.provision :shell, :path => "run_bootstrap.sh"
end
-------------------------------------------------------------------------------
The value you specify for config.vm.box defines the computer name of the 
virtual machine. (The virtual machine itself will be visible in VirtualBox by 
the name of its containing folder. The example virtual machine will be named 
"ubuntu_x86_makahiki_" followed by 10 digits.)

In config.vm.provision, :path => "bootstrap_runner.sh" defines the location of 
a shell script that will be run when the machine starts with the "vagrant up" 
or "vagrant reload" commands. While the machine is running, the "vagrant 
provision" command will run this shell script as well.
===============================================================================

2.0.4. Download the Base Virtual Machine
===============================================================================
This step adds the base virtual machine specified in the last step, 
"precise32," for Vagrant to use. (Replace "precise32" with whatever 
value you specified for config.vm.box in the last step.)

> vagrant box add precise32 http://files.vagrantup.com/precise32.box

This will download the virtual machine from Vagrant's servers.
===============================================================================

2.0.5. Copy the Provisioning Script Files
===============================================================================
Copy bootstrap_runner.sh, bootstrap.sh, and the logs/ directory to 
the current ubuntu_x86_makahiki directory from the makahiki directory: 
> cp ./makahiki/install/vagrant_scripts/ubuntu_x86/run_bootstrap.sh ./run_bootstrap.sh
> cp ./makahiki/install/vagrant_scripts/ubuntu_x86/bootstrap.sh ./bootstrap.sh
> cp ./makahiki/install/vagrant_scripts/ubuntu_x86/logs ./logs

On the Vagrant virtual machine, the ubuntu_x86_makahiki directory will be 
the /vagrant directory, and these files will be accessible to the virtual 
machine.
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

The shell script installs the following packages and their dependencies:
- git
- gcc
- python-setuptools
- pip
- Python Imaging Library
  - python-dev
  - python-imaging
  - libjpeg-dev
  - Creates symbolic links to libz.so and libjpeg.so in /usr/lib:
    1. /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so
    2. /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so
- PostgreSQL 9.1
  - postgresql-9.1
  - libpq-dev
- memcached
- libmemcached-dev
- virtualenvwrapper

The bootstrap_runner.sh script logs the output of bootstrap.sh to a text 
file in the logs directory. This file is called "ubuntu_x86_<timestamp>.log,"
where <timestamp> is in the format yyyy-mm-dd-HH-MM-SS (year, month, day, 
hour, minute, second).

(Later, if you want to start the virtual machine without provisioning it, 
 start it with the "vagrant up --no-provision" command.)
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

vagrant@precise32:/~$
===============================================================================

2.1.3. Download the Makahiki Source Code
===============================================================================
Assuming that Git installed successfully, clone the CSDL Makahiki repository 
from Github into the vagrant user's home directory:

vagrant@precise32:/~$ git clone http://github.com/csdl/makahiki.git

WARNING:
-------------------------------------------------------------------------------
Do not try to skip this step by putting the makahiki repository (the one 
that you cloned into Windows) into the shared folder and copying the files 
into the user home directory. These files will have Windows line endings 
and cannot be used on Linux.
-------------------------------------------------------------------------------
===============================================================================

2.1.4. Configure .bashrc Environment Variables
===============================================================================
For virtualenvwrapper to work correctly with Makahiki, environment variables 
need to be set. Open and edit the .bashrc file in the user's home directory 
using nano:

vagrant@precise32:/~$ nano .bashrc

Add the following lines to the end of the file:
# Virtualenvwrapper settings for makahiki
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/makahiki
source /usr/local/bin/virtualenvwrapper.sh

Source the .bashrc file in order for the changes to take effect.

vagrant@precise32:/~$ source .bashrc

ABOUT NANO:
-------------------------------------------------------------------------------
Nano is a text editor that is installed by default on Ubuntu.
- Use the arrow keys to navigate
- Type to insert text
- Use [backspace] to delete text
- Use Ctrl-O (^O) to save
- Use Ctrl-X (^X) to quit
Further documentation can be found at http://nano-editor.org/docs.php.
-------------------------------------------------------------------------------

NOTE FOR VI USERS:
-------------------------------------------------------------------------------
Some users may prefer the vi text editor, which is also installed on Ubuntu. 
Note that these bugs were observed when using vi on an Ubuntu Vagrant 
virtual machine in a Windows cmd terminal:
- In Insert mode, [backspace] does not delete text. 
  The "x" key must be used instead.
- Input lag.
-------------------------------------------------------------------------------
===============================================================================

2.1.5. Set Up the "makahiki" Virtual Environment
===============================================================================
Switch to the top-level makahiki directory:

vagrant@precise32:/~$ cd makahiki

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

On Ubuntu 12.04.1 LTS and later, the pg_hba.conf file is usually located at 
/etc/postgresql/9.1/main/pg_hba.conf. Open it in a text editor with sudo (root) 
privileges:

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
% sudo /etc/init.d/postgresql restart
 * Restarting PostgreSQL 9.1 database server                             [ OK ]
===============================================================================

2.1.7. Install Dependencies With Pip
==============================================================================
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

You will need to do "workon makahiki" after you have edited the postactivate 
file for the changes to take effect:

(makahiki)vagrant@precise32:~/makahiki$ workon makahiki
===============================================================================

2.1.9. Initialize Makahiki [BUG NOT RESOLVED]
===============================================================================
# TODO: Need to decide whether or not to bring up the Unicode / Latin-1 bug
# involving smartgrid_library.json's smartgridlibrary.libraryaction (pk 172).

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

The server is still not reachable from the host machine. This will be 
configured in the next step.
===============================================================================

2.1.11. Configure Networking for the Virtual Machine [INCOMPLETE]
===============================================================================
[SECTION UNDER REVISION]

Use Ctrl-C to stop the server. The server will not be reachable by the host 
machine until another network interface is added.

Next, shut down the virtual machine. This will close the SSH session:
(makahiki)vagrant@precise32:~/makahiki/makahiki$ sudo shutdown -h now

Next, add these lines to the Vagrantfile before the "end" line:
-------------------------------------------------------------------------------
config.vm.network :private_network, ip: "192.168.56.3"
config.vm.network :forwarded_port, guest: 8000, host: 8080
-------------------------------------------------------------------------------
This configures a host-only networking interface with address 192.168.56.3 
and subnet mask 255.255.255.0 (/24). The port 8000 (which Makahiki runs on 
in the virtual machine) will be forwarded to port 8080 for the host machine.

Now, open Command Prompt, go to the ubuntu_x86_makahiki folder, and restart 
the Vagrant virtual machine:

> vagrant up --no-provision
> vagrant ssh

-------------------------------------------------------------------------------
If a "Windows Security Alert" warning appears while "vagrant up" is running 
with a message similar to the following:

"Windows Firewall has blocked some features of this app

 Windows Firewall has blocked some features of vboxheadless.exe on all public 
 and private networks.
     Name: vboxheadless.exe
     Publisher: Unknown
     Path: C:\program files\oracle\virtualbox\vboxheadless.exe
     
 Allow vboxheadless.exe to communicate on these networks:
 [ ] Private networks, such as my home or work network
 [v] Public networks, such as those in airports and coffee shops (not recommended 
     because these networks often have little or no security)"

Uncheck the box for "Public networks" and click "Cancel." A host-only network 
does not need to go through the Windows firewall.

# TODO: Not sure whether it needs to be allowed through firewall or not.
# So far I've actually allowed vboxheadless through the firewall, but to no 
# effect.
-------------------------------------------------------------------------------

On the virtual machine, use ifconfig to verify that the network interface was 
added correctly. Look for an entry for "eth1," as in the example below:
-------------------------------------------------------------------------------
vagrant@precise32:~$ ifconfig eth1
eth1      Link encap:Ethernet  HWaddr 08:00:27:46:66:0d
          inet addr:192.168.56.3  Bcast:192.168.56.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fe46:660d/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:377 errors:0 dropped:0 overruns:0 frame:0
          TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:59518 (59.5 KB)  TX bytes:468 (468.0 B)
-------------------------------------------------------------------------------

Switch to makahiki/makahiki, activate the virtual environment, and start the 
server with manage.py:
vagrant@precise32:~$ workon makahiki
(makahiki)vagrant@precise32:~$ cd makahiki/makahiki
(makahiki)vagrant@precise32:~/makahiki/makahiki$ ./manage.py runserver

Host-only networking does not make the virtual machine accessible outside of 
the host computer. It is only designed for localhost testing.

Configuring a production server is left as an exercise for the deployer.
===============================================================================

2.1.12. Increase the RAM of the Virtual Machine [INCOMPLETE]
===============================================================================
[SECTION UNDER REVISION]

The default RAM of the Vagrant Ubuntu 12.04 x86 virtual machine is 384 MB. 
While this is sufficient for terminal access, it is likely to result in slow 
serving of Makahiki web pages in local network testing.

# TODO: Not sure if recommendations would be lower on a headless VM.
1.5 to 2.0 GB (1536 to 2048 MB) is about the minimum needed to run the server 
with some slowdown. 

The recommendations of the Makahiki developers are as follows:
- 4 GB (4096 MB) for local development
- 8 GB (8192 MB) for production use.

Stop the web server by pressing Ctrl-C in the SSH terminal.
Then shut down the virtual machine:
(makahiki)vagrant@precise32:~/makahiki/makahiki$ sudo shutdown -h now

This will end the SSH session.

To increase the RAM allocated to the Virtualbox VM, add these lines to the 
Vagrantfile before the "end" line. Replace "2048" with the desired amount of 
RAM, in MB.
-------------------------------------------------------------------------------
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", 2048]
  end
-------------------------------------------------------------------------------

After saving your changes, restart the VM and start the SSH session:
> vagrant up --no-provision
> vagrant ssh

In the SSH session, switch to makahiki/makahiki, activate the virtual '
environment, and start the server with manage.py:
vagrant@precise32:~$ workon makahiki
(makahiki)vagrant@precise32:~$ cd makahiki/makahiki
(makahiki)vagrant@precise32:~/makahiki/makahiki$ ./manage.py runserver
===============================================================================

2.1.13. Update the Makahiki Instance
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

2.1.14. Re-Provisioning Vagrant
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