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
2.1.3. Check for the Makahiki Source Code
2.1.4. Start the Server
2.1.5. If the Server Does Not Start
2.1.6. If the Site Is Unreachable
Appendix A.0. Troubleshooting Configuration Files
Appendix A.0.1. Troubleshooting /etc/bash.bashrc
Appendix A.0.2. Troubleshooting pg_hba.conf
Appendix A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh
Appendix A.0.4. Troubleshooting /home/vagrant/.bashrc
Appendix B.0. Makahiki Maintenance Tasks
Appendix B.0.1. Initialize Makahiki
Appendix B.0.2. The Makahiki Server
Appendix B.0.2.1. Testing The Server Without a Web Browser
Appendix B.0.3. Update the Makahiki Instance
Appendix B.0.4. Check The Memcached Installation
Appendix C. Vagrant Commands
Appendix D. Re-Provisioning Vagrant
Appendix E. Configure the RAM of the Virtual Machine
Appendix F. Configure Networking on the Virtual Machine

Instructions in appendices are optional.
-------------------------------------------------------------------------------

0.0. Introduction
===============================================================================
This is a README file that describes the process for deploying Makahiki in a 
Vagrant virtual machine on a given host machine. The virtual machine is 
intended for testing or development use. It is not suitable for use in a 
production deployment of the Makahiki software.

If you would prefer to install Makahiki manually, without using Vagrant, see 
the documentation at:
- Windows: http://makahiki.readthedocs.org/en/latest/installation-makahiki-windows.html
- OS X and Unix: http://makahiki.readthedocs.org/en/latest/installation-makahiki-unix.html

The Makahiki source code is available from https://github.com/csdl/makahiki.

In the examples in this document, the > represents a generic terminal prompt.

This guide assumes a basic level of familiarity with your host operating 
system.

System requirements:
- Operating System:
  - Windows 7 or 8 
  - Mac OS X
  - A recent Red Hat-based or Debian-based Linux distro 
    (Vagrant comes in .rpm or .deb installers).
  - The applications used in this guide are compatible with 
    x86 (32-bit) and x64 (64-bit) operating systems.
  - The virtual machine that will be configured will have x86 architecture
    and is compatible with x86 or x64 host operating systems.
  - Linux users:
    It is recommended that the host machine have a graphical user interface 
    or a window manager. This guide assumes the use of a graphical user 
    interface in some sections. It is required if you choose to use Eclipse.
- Hardware:
  - CPU: Modern dual or quad core
  - RAM: 4 GB
  - The Vagrant virtual machine will be configured by default to have 1.5 GB 
    of RAM (1536 MB). To change this amount, see Appendix E.

WARNING:
-------------------------------------------------------------------------------
This guide should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

WARNING FOR DEVELOPERS:
-------------------------------------------------------------------------------
Though not required, it is STRONGLY RECOMMENDED that you use Eclipse or 
another integrated development environment (IDE) that can maintain 
UTF-8 encoding and LF line endings within the project. UTF-8 and LF line 
endings are required by certain Makahiki dependencies.

Eclipse is available for Windows, OS X, and many Linux distributions.
Linux users should note that Eclipse is a graphical application.

To set up Eclipse for Makahiki development, see vagrant_and_eclipse_readme.txt.

Above all, Windows users SHOULD NOT EDIT OR CREATE ANY FILES IN NOTEPAD:
1. Notepad ends lines with Windows line endings (CR-LF). Linux 
   applications expect LF endings and may have problems parsing CR-LF.
2. Notepad defaults to ANSI encoding when a file is saved. Some Linux 
   applications expect UTF-8.
3. Notepad adds a Byte Order Mark (BOM) to the beginning of each new file
   that is saved with an encoding other than ANSI. On Linux, this appears 
   as random characters (e.g., "ï»?") that appear before the first word in 
   the file. Linux applications may not be able to process files that start 
   with a BOM.
-------------------------------------------------------------------------------
===============================================================================

1.0. VirtualBox and Vagrant Setup
===============================================================================
This section installs VirtualBox and Vagrant onto a computer.

This guide uses the terms "virtual machine" and "host machine." 
A virtual machine is an operating system running on simulated hardware, which 
is simulated using the hardware of the host machine. The host machine is the 
computer that Vagrant and VirtualBox use to run the virtual machine.
===============================================================================

1.0.1. Install VirtualBox
===============================================================================
Download VirtualBox from https://www.virtualbox.org/wiki/Downloads.
To install VirtualBox, follow the instructions at 
https://www.virtualbox.org/manual/ch02.html.

Select "Yes" when you are asked to install drivers for USB support and 
VirtualBox Host-Only Networking.

This guide was tested with VirtualBox 4.2.16. It should be compatible with 
later versions, but this has not been tested.
===============================================================================

1.0.2. Install Vagrant
===============================================================================
Download the Vagrant installer from http://downloads.vagrantup.com/.
- Windows users: download the .msi file.
- Mac OS X users: download the .dmg file.
- Linux users: download the .rpm or .deb package appropriate for your 
  host machine's distribution and architecture.
To install Vagrant on your operating system, follow the instructions at 
http://docs.vagrantup.com/v2/installation/index.html.

This guide was tested with Vagrant 1.2.4. It should be compatible with 
later versions of Vagrant 1.2, but this has not been tested.
===============================================================================

2.0. Vagrant Virtual Machine Setup 
===============================================================================
Section 2.0 and subsections contain instructions for creating the Vagrant 
virtual machine. Start by opening a terminal window in your host operating 
system.

- Windows Users: Open a Windows Command Prompt (cmd) terminal window. 
  If you can't find the Command Prompt, type "cmd.exe" in Run.
- OS X Users: Open a Terminal window.
  - bash has been the default Terminal shell since OS X 10.3.
  - If your default shell is different, type "bash" to temporarily 
    switch to bash.
- Linux users: Open a Terminal window.
===============================================================================

2.0.1. Download the Makahiki Source Code
===============================================================================
Downloading the Makahiki source code will create the "makahiki" directory.

There are two ways of obtaining the Makahiki source code. (If you have this 
text file, you likely already have the Makahiki source code, and can skip this 
section.)

A. If you do not have Git or Git for Windows, download the source code from 
   Github as a .zip file:
    A1. In a web browser, go to https://github.com/csdl/makahiki.
    A2. Click the button to "Download ZIP."
    A3. Extract the makahiki.zip file that is downloaded.

B. If you have Git, or Git for Windows, you can clone the repository:
   ----------------------------------------------------------------------------
   > git clone http://github.com/csdl/makahiki.git
   ----------------------------------------------------------------------------
   Windows: Get "Git for Windows" from http://git-scm.com/download/win.
   OS X and Unix: Git is available through various package managers and
            installers; see https://help.github.com/articles/set-up-git
            for further instructions.

Now switch your working directory to makahiki:
-------------------------------------------------------------------------------
> cd makahiki
-------------------------------------------------------------------------------
===============================================================================

2.0.2. Download the Base Virtual Machine
===============================================================================
This step adds the base virtual machine specified in the last step, 
"precise32," for Vagrant to use.
-------------------------------------------------------------------------------
> vagrant box add precise32 http://files.vagrantup.com/precise32.box
-------------------------------------------------------------------------------
This will download the virtual machine from Vagrant's servers.

It is only necessary to download each specific box once; if you create more 
virtual machines with the same base box ("precise32") specified in the 
Vagrantfile, you can skip this step.
===============================================================================

2.1. Set up Makahiki in the Virtual Machine
===============================================================================
Section 2.1's subsections describe the process of configuring Makahiki in 
the virtual machine. 
===============================================================================

2.1.1. Start the Virtual Machine and Run the Provisioning Script
===============================================================================
You should be in the top-level Makahiki directory, where the Vagrantfile is.
Use the "vagrant up" command to start the virtual machine:
-------------------------------------------------------------------------------
> vagrant up
-------------------------------------------------------------------------------
Each time you start Vagrant with "vagrant up," it will run the 
"run_bootstrap.sh" script specified in the Vagrantfile. This script runs and 
logs the "bootstrap.sh" script.

While "vagrant up" is running, Windows users may see the following warnings: 
1. A Windows Firewall warning about vboxheadless.exe. This exception is needed 
   for Vagrant, and should be allowed.
2. A warning that VirtualBox is attempting to make changes to the system. 
   This is needed for the host-only networking to work correctly, and should 
   be allowed.

WARNING:
-------------------------------------------------------------------------------
Each time the provisioning script is run, it drops the PostgreSQL cluster data 
directory and re-initializes it, then re-initializes the Makahiki database. 
This will erase ALL DATA in ALL DATABASES on the system.

To start the virtual machine without provisioning it, use --no-provision: 
-------------------------------------------------------------------------------
> vagrant up --no-provision
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

The bootstrap.sh script: 
1. Overwrites the default /etc/bash.bashrc with en_US.UTF-8 locale settings
2. Generates the en_US.UTF-8 locale
3. Calls dpkg-reconfigure to reconfigure package manager locales
4. Updates the apt package lists
5. Installs the following packages and their dependencies:
   5a. git
   5b. gcc
   5c. python-setuptools
   5d. pip
   5e. Python Imaging Library
       5e1. python-dev
       5e2. python-imaging
       5e3. libjpeg-dev
       5e4. Creates symbolic links to libz.so and libjpeg.so in /usr/lib:
            5e4a. /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so
            5e4b. /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so
   5f. PostgreSQL 9.1
       5f1. postgresql-9.1
       5f2. libpq-dev
       5f3. Drops, then re-initializes the database cluster with the locale 
            en_US.UTF-8, version 9.1, and name "main."
       5f4. Overwrites the default pg_hba.conf file with Makahiki 
            authentication settings.
       5f5. Restarts the postgresql service.
   5g. memcached
   5h. libmemcached-0.53
   5j. virtualenvwrapper
6. Copies /home/vagrant/makahiki_env.sh to the vagrant user's home 
   directory to set Makahiki environment variables in the shell
7. Edits /home/vagrant/.bashrc so that it will source 
   /home/vagrant/makahiki_env.sh
8. Executes "pip install -r requirements.txt" in the makahiki directory 
   (/vagrant on the virtual machine), installing Makahiki dependencies 
   with pip.
9. Initializes the Makahiki database. (Note any errors that occur 
   during this phase; the script is not aware of them and will continue on 
   regardless.)

The bootstrap_runner.sh script logs the output of bootstrap.sh to a text 
file. This file is called "ubuntu_x86_<timestamp>.log," where <timestamp> is 
in the format yyyy-mm-dd-HH-MM-SS (year, month, day, hour, minute, second).
These logs are stored at:
- On the host machine: <path-to-makahiki>/makahiki/vagrant/logs.
- On the virtual machine: /vagrant/vagrant/logs

If run more than once, the script will:
1. Update the apt package lists: Every time
2. Overwrite bash.bashrc: First run only
3. Regenerate and reconfigure locale settings: Every time
4. Install packages: First run only
5. Edit /home/vagrant/.bashrc: First run only
6. Creates /home/vagrant/makahiki_env.sh: On first run or if file is deleted
7. Drop/regenerate the PostgreSQL cluster data directory, which erases all 
   databases on the system: Every time
8. Install pip packages: First run only
9. Re-initialize the Makahiki database: Every time

When the script finishes, look at the last few lines of output:
-------------------------------------------------------------------------------
Configuration setup results:
-------------------------------------------------------------------------------
1. Copying locale settings to /etc/bash.bashrc: [Succeeded]"
2. Copying settings to pg_hba.conf: [Succeeded]"
3. Creating /home/vagrant/makahiki_env.sh: [Succeeded]"
4. Appending to /home/vagrant/.bashrc: [Succeeded]"
-------------------------------------------------------------------------------
If the value for a task is "Succeeded" or "Already completed," continue.

If Task 1's result is "Failed," go to: 
   "A.0.1. Troubleshooting bash.bashrc"
If Task 2's result is "Failed," go to: 
   "A.0.2. Troubleshooting pg_hba.conf"
If Task 2's result is "Failed," go to: 
   "A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh" 
If Task 4's result is "Failed," go to: 
   "A.0.4. Troubleshooting /home/vagrant/.bashrc"
If you noticed errors when the script was initializing the database, go to:
   "A.0.2. Troubleshooting pg_hba.conf" or "B.0.1. Initializing Makahiki."
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

2.1.3. Check For Makahiki Source Code
===============================================================================
The makahiki source code should show up in the /vagrant/ directory.
-------------------------------------------------------------------------------
vagrant@precise32:~$ cd /vagrant
vagrant@precise32:/vagrant/$ ls
-------------------------------------------------------------------------------

The output of ls should match the contents of the makahiki directory on your 
host machine.
===============================================================================

2.1.4. Start The Server
===============================================================================
The Makahiki server is started manually from the /vagrant/makahiki directory: 
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant$ cd /vagrant/makahiki
-------------------------------------------------------------------------------

To start the server with manage.py:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000
-------------------------------------------------------------------------------

To start the server with gunicorn:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000
-------------------------------------------------------------------------------

The web server can be accessed in a browser on the host machine at 
http://192.168.56.4:8000. 

If this fails, see "2.1.6. If the Site Is Unreachable."

Stop the server by typing Control-C in the terminal.

For more information, see "Appendix B.0.2. The Makahiki Server."
===============================================================================

2.1.5. If the Server Does Not Start
===============================================================================
Continue to Appendix A.0., "Troubleshooting Configuration Files."
===============================================================================

2.1.6. If The Site Is Unreachable
===============================================================================
Continue to Appendix F, "Configure Networking on the Virtual Machine."
===============================================================================

Appendix A.0. Troubleshooting Configuration Files
===============================================================================
Appendix A contains troubleshooting instructions for configuration files.
The instructions refer to the GNU nano text editor, which is installed 
by default in the "precise32" Ubuntu virtual machine. GNU nano is one of many 
Linux text editors (including vi, emacs, pico, etc.)

Basic nano Controls
-------------------
Move the cursor with the arrow keys.
Type to insert text at the cursor.
Control-G (^G) opens Help and Control-X (^X) closes it.
Control-O (^O) saves the document.
Control-X (^X) closes a document.
Control-W (^W) searches the document for a string that you specify.
Control-Y (^Y) is Page Up.
Control-V (^V) is Page Down.
Control-K (^K) cuts the entire current line.
Control-U (^U) pastes the last line that was cut.
Control-C (^C) shows the current position of the cursor in a readout at the 
            bottom of the screen.
Other controls are displayed along the bottom of the screen.

If you close a document without saving changes, you will be prompted:
"Save modified buffer (ANSWERING "No" WILL DESTROY CHANGES) ?"
Y is yes, N is no, ^C is cancel.

When you save a document (e.g., one called test.txt), you will be prompted:
"File Name to Write: test.txt"
Press Enter to continue, or type to edit the file name.

For the full nano documentation, see http://www.nano-editor.org/docs.php.
===============================================================================

Appendix A.0.1. Troubleshooting /etc/bash.bashrc and UTF-8 Encodings
===============================================================================
You need to change the system and postgresql database encodings if one of the 
following applies:
A. You experience a DatabaseError when the initialize_instance.py script runs, 
   with the message "character 0x##### of encoding "UTF8" has no equivalent 
   in "LATIN1"."
B. The "locale" command returns a non-UTF-8 encoding setting:
   ----------------------------------------------------------------------------
   vagrant@precise32:~$ locale
   LANG=en_US.LATIN1
   LANGUAGE=en_US.LATIN1
   ...
   LC_ALL=en_US.LATIN1
   ----------------------------------------------------------------------------

If this is the case, continue.

Open /etc/bash.bashrc with sudo:
-------------------------------------------------------------------------------
vagrant@precise32:~$ sudo nano /etc/bash.bashrc
-------------------------------------------------------------------------------

Add these lines to the end of the file:
-------------------------------------------------------------------------------
# UTF-8 locale settings for Makahiki
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
-------------------------------------------------------------------------------

After you are done editing the file, run these commands:
-------------------------------------------------------------------------------
vagrant@precise32:~$ sudo locale-gen en_US.UTF-8
vagrant@precise32:~$ sudo dpkg-reconfigure locales
vagrant@precise32:~$ sudo pg_dropcluster 9.1 main --stop
vagrant@precise32:~$ sudo pg_createcluster --locale en_US.UTF8 9.1 main
vagrant@precise32:~$ sudo cp /vagrant/vagrant/config_examples/pg_hba.conf.ubuntu.makahiki /etc/postgresql/9.1/main/pg_hba.conf
vagrant@precise32:~$ sudo /etc/init.d/postgresql restart
-------------------------------------------------------------------------------
Continue to Appendix A.0.2., "Troubleshooting pg_hba.conf."
===============================================================================

Appendix A.0.2. Troubleshooting pg_hba.conf
===============================================================================
Begin by verifying the PostgreSQL server authentication settings.
At the prompt, type "psql -U postgres." If it succeeds, type \q to quit.
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant$ psql -U postgres
psql (9.1.9)
Type "help" for help.

postgres=#\q
vagrant@precise32:/vagrant$
-------------------------------------------------------------------------------
If you cannot connect to the database with "psql -U postgres," or experience 
errors when running initialize_instance.py, check that the pg_hba.conf file 
has the correct settings applied.

On Ubuntu 12.04 LTS, pg_hba.conf is at /etc/postgresql/9.1/main/pg_hba.conf.
Open it in the nano text editor with sudo (root) privileges:

vagrant@precise32:/vagrant$ sudo nano /etc/postgresql/9.1/main/pg_hba.conf

1. To configure PostgreSQL, edit the "local all postgres", "local all all", 
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

2. After you have edited the pg_hba.conf file, restart the Postgresql service:
vagrant@precise32:/vagrant$ sudo /etc/init.d/postgresql restart
===============================================================================

Appendix A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh
===============================================================================
makahiki_env.sh sets values for Makahiki environment variables 
MAKAHIKI_DATABASE_URL and MAKAHIKI_ADMIN_INFO. Check that these values 
have been set:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant$ echo $MAKAHIKI_DATABASE_URL
postgres://makahiki:makahiki@localhost:5432/makahiki
vagrant@precise32:/vagrant$ echo $MAKAHIKI_ADMIN_INFO
admin:admin
-------------------------------------------------------------------------------
If "echo" returns nothing, source home/vagrant/.bashrc (~/.bashrc) and 
check again:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant$ source ~/.bashrc
-------------------------------------------------------------------------------

If MAKAHIKI_DATABASE_URL and MAKAHIKI_ADMIN_INFO are still not set after 
sourcing ~/.bashrc, you need to add them to /home/vagrant/makahiki_env.sh.

1. Create this file if it does not exist:
-------------------------------------------------------------------------------
vagrant@precise32:~$ touch makahiki_env.sh
-------------------------------------------------------------------------------

2. Open the file in the nano text editor. (The ~ is a shortcut for the 
current user's home directory, which is /home/vagrant.)
-------------------------------------------------------------------------------
vagrant@precise32:~$ nano makahiki_env.sh
-------------------------------------------------------------------------------

The file should contain the lines shown below:
-------------------------------------------------------------------------------
# Makahiki environment variables
# Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki
# Syntax: <admin_name>:<admin_password>
export MAKAHIKI_ADMIN_INFO=admin:admin
-------------------------------------------------------------------------------
These settings are only used to initialize the Makahiki database. If you change 
the username or password in the Makahiki user interface, these settings will 
no longer apply.

Note:
-----
The username:password combination of admin:admin is meant for use in 
development. In a production server, the value of MAKAHIKI_ADMIN_INFO would be 
changed to a more secure value.

3. When you are done editing makahiki_env.sh, source the .bashrc file. This will 
source the makahiki_env.sh file, which will set the environment variables:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant$ source ~/.bashrc
vagrant@precise32:/vagrant$ echo $MAKAHIKI_DATABASE_URL
postgres://makahiki:makahiki@localhost:5432/makahiki
vagrant@precise32:/vagrant$ echo $MAKAHIKI_ADMIN_INFO
admin:admin
-------------------------------------------------------------------------------
If this fails, continue to A.0.4., "Troubleshooting /home/vagrant/.bashrc."
===============================================================================

Appendix A.0.4. Troubleshooting /home/vagrant/.bashrc
===============================================================================
bootstrap.sh normally appends this line to the "vagrant" user's .bashrc file:
-------------------------------------------------------------------------------
source /home/vagrant/makahiki_env.sh
-------------------------------------------------------------------------------

Open /home/vagrant/.bashrc in the nano editor. (The ~ is a shortcut for the 
current user's home directory, which is /home/vagrant.)
-------------------------------------------------------------------------------
vagrant@precise32:~$ nano ~/.bashrc
-------------------------------------------------------------------------------

Add the line "source /home/vagrant/makahiki_env.sh" to the end of the file.
Save the file and source it for changes to take effect:
vagrant@precise32:~$ source ~/.bashrc
===============================================================================

Appendix B.0. Makahiki Maintenance Tasks
===============================================================================
This section covers common Makahiki maintenance tasks.
1. To (re)initialize the Makahiki database: 
   See "Appendix B.0.1. Initialize Makahiki."
2. To start/stop the server manually: 
   See "Appendix B.0.2. The Makahiki Server."
3. To update the Makahiki instance: 
   See "Appendix B.0.3. Update the Makahiki Instance."
===============================================================================

Appendix B.0.1. Initialize Makahiki
===============================================================================
WARNING:
-------------------------------------------------------------------------------
Running the initialize_instance.py script will:
- Install and/or update all pip-installed packages required by Makahiki.
- Reinitialize the database contents and perform any needed database 
  migrations.
- Initialize the system with data.
- Set up static files.

This script should be run only a single time in production scenarios, because 
any subsequent configuration modifications will be lost if initialize_instance 
is invoked again.

The script initializes the Makahiki database and populates it with default 
information and users.
-------------------------------------------------------------------------------

Switch to the /vagrant/makahiki directory:
-------------------------------------------------------------------------------
vagrant@precise32:~/$ cd /vagrant/makahiki
vagrant@precise32:/vagrant/makahiki$ ./scripts/initialize_instance.py --type default
-------------------------------------------------------------------------------
You will need to answer "Y" to the question "Do you wish to continue (Y/n)?"

If the script experiences errors while connecting to the database, see 
"Appendix A.0.2. Troubleshooting pg_hba.conf".
===============================================================================

Appendix B.0.2. The Makahiki Server
===============================================================================
The Makahiki server must be started manually.

This guide assumes you are currently in the directory /vagrant/makahiki on 
your virtual machine.

The servers provided by manage.py are runserver and gunicorn. The manage.py 
web server is better for development, while gunicorn is better for production 
use. It is important to bind the server to IP 0.0.0.0 (accepts incoming 
connections on any IP address) and port 8000 in order to work with the port 
forwarding settings in the Vagrantfile.

To start the server with manage.py:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000
-------------------------------------------------------------------------------

To start the server with gunicorn:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000
-------------------------------------------------------------------------------

View the site in your host machine's web browser at http://192.168.56.4:8000.

Log in with the username (admin) and password (admin) in MAKAHIKI_ADMIN_INFO. 
See "Appendix A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh" to change 
them.

To stop either of the servers, type Control-C in the virtual machine terminal.
===============================================================================

Appendix B.0.2.1. Testing the Server Without a Web Browser
===============================================================================
If you are having problems accessing the web server from the host machine and 
want to verify that it is working, you will need to use wget to test the 
server on the virtual machine.
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver &
Validating models...

Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
vagrant@precise32:/vagrant/makahiki$^M    # Note: Press "Enter" here.
vagrant@precise32:/vagrant/makahiki$ cd ~/
vagrant@precise32:~$ mkdir test
vagrant@precise32:~/test$ cd test
vagrant@precise32:~/test$ wget http://127.0.0.1:8000
--2013-08-09 11:19:25--  http://127.0.0.1:8000/
Connecting to 127.0.0.1:8000... connected.
HTTP request sent, awaiting response... 302 FOUND
Location: http://127.0.0.1:8000/landing/ [following]
[09/Aug/2013 11:19:26] "GET / HTTP/1.0" 302 0
--2013-08-09 11:19:26--  http://127.0.0.1:8000/landing/
Connecting to 127.0.0.1:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
[09/Aug/2013 11:19:26] "GET /landing/ HTTP/1.0" 200 6181
Saving to: “index.html"

    [ <=>                                   ] 6,181       --.-K/s   in 0s

2013-08-09 11:19:26 (192 MB/s) - “index.html" saved [6181]
-------------------------------------------------------------------------------
If your HTTP response is "200 OK," the server is running correctly. You can 
delete the "test" directory when you are done.

Because this server was started in the background with &, you cannot stop it 
with Control-C. You will need to find the PID of the process first:
-------------------------------------------------------------------------------
vagrant@precise32:~/test$ ps ax | grep manage.py
21791 tty1     S     0:00 python ./manage.py runserver
21798 tty1     Sl    0:52 /root/.virtualenvs/makahiki/bin/python ./manage.py ru
nserver
21893 tty1     S+    0:00 grep manage.py
% kill -9 21791
% 
[1]+  Killed                 ./manage.py runserver  (wd: ~/makahiki/makahiki)
(wd now: ~/test)
-------------------------------------------------------------------------------
The PID of the process is 21791 here, but will be different each time.
"kill -9 <PID>" forces the OS to stop the process, and the 
"python ./manage.py runserver" is what needs to be stopped.

Later, if you restart the web server and get an error stating that the port 
is already in use, you may need to use kill -9 to stop the other process,
"/root/.virtualenvs/makahiki/bin/python ./manage.py runserver," as well.
===============================================================================

Appendix B.0.3. Update the Makahiki Instance
===============================================================================
Makahiki is designed to support post-installation updating of your configured 
system when bug fixes or system enhancements become available. Updating an 
installed Makahiki instance using the update_instance.py script requires the 
following steps:

(The % indicates that the command can be done from anywhere in the virtual 
 machine, regardless of working directory.)

(1.) Close the running server in the shell process that is running Makahiki:
(type control-c in the shell running the makahiki server process)

(2.) Go to the vagrant directory (the makahiki directory on the host machine):
-------------------------------------------------------------------------------
% cd /vagrant
vagrant@precise32:/vagrant$
-------------------------------------------------------------------------------

(3.) Download the updated source code into the Makahiki installation:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant$ git pull origin master
-------------------------------------------------------------------------------

(4.) Run the update_instance.py script:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant$ cd makahiki
vagrant@precise32:/vagrant/makahiki$ ./scripts/update_instance.py
-------------------------------------------------------------------------------

(5.) Start the server with runserver or gunicorn:
To start the server with manage.py:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver
-------------------------------------------------------------------------------

To start the server with gunicorn:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn
-------------------------------------------------------------------------------
===============================================================================

Appendix B.0.4. Check The Memcached Installation
===============================================================================
The provisioning script installed Memcached and libmemcached-0.53 on the 
system. If you plan to configure Memcached, you will need to test the 
Memcached installation.

In the virtual machine, switch to the /vagrant/makahiki directory and run some 
commands in the manage.py shell:
-------------------------------------------------------------------------------
vagrant@precise32:~$ sudo service memcached restart
vagrant@precise32:~$ export LD_LIBRARY_PATH_OLD=$LD_LIBRARY_PATH
vagrant@precise32:~$ export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:$LD_LIBRARY_PATH
vagrant@precise32:~$ export MAKAHIKI_USE_MEMCACHED=True
vagrant@precise32:~$ cd /vagrant/makahiki
vagrant@precise32:/vagrant/makahiki$ ./manage.py shell
Python 2.7.3 (default, Apr 10 2013, 05:46:21)
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.core.cache import cache
>>> cache
<django_pylibmc.memcached.PyLibMCCache object at 0x8c93c4c>
>>> cache == None
False
>>> cache.set('test','Hello World')
True
>>> cache.get('test')
'Hello World'
>>> exit()
vagrant@precise32:/vagrant/makahiki$ unset MAKAHIKI_USE_MEMCACHED
vagrant@precise32:/vagrant/makahiki$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_OLD
vagrant@precise32:/vagrant/makahiki$ unset LD_LIBRARY_PATH_OLD
-------------------------------------------------------------------------------
If any of the following errors occur, then Memcached is not working:
(1) cache prints a blank to the console, or cache == None returns True.
(2) cache.set returns False.
(3) cache.get returns False or causes a segmentation fault.

If the tests succeed, you can configure Makahiki to use Memcached. To do this, 
add these lines to the end of the makahiki_env.sh file:
-------------------------------------------------------------------------------
export MAKAHIKI_USE_MEMCACHED=True
# Don't add libmemcached paths more than once
if [ ! $LIBMEMCACHED_PATHS_ADDED ];
    then
        export LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:$LD_LIBRARY_PATH
        export LIBMEMCACHED_PATHS_ADDED=True
fi
-------------------------------------------------------------------------------

On Vagrant, the memcached service should run automatically once installed by 
the provisioning script. If it does not run, start it manually:
-------------------------------------------------------------------------------
vagrant@precise32:~$ sudo service memcached start
-------------------------------------------------------------------------------
===============================================================================

Appendix C. Vagrant Commands
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

Appendix D. Re-Provisioning Vagrant
===============================================================================
If you are developing for Makahiki using a Vagrant virtual machine and change 
the provisioning scripts (bootstrap.sh or run_bootstrap.sh), you will need 
to provision the virtual machine again. You can do this in one of two ways.

A. Re-provision the virtual machine on startup with "vagrant up":
In the makahiki/vagrant directory, start the virtual machine with "vagrant up."
This will run the provisioning script designated in the Vagrantfile.
> vagrant up 

An error may occur during virtual machine startup:
"dpkg-preconfigure: unable to re-open stdin: No such file or directory"
This error does not affect the provisioning script and can be ignored.

B. Re-provision a virtual machine that is already running:
> vagrant provision
===============================================================================

Appendix E. Configure the RAM of the Virtual Machine
===============================================================================
The default settings in the Vagrantfile that comes with this project limit 
the virtual machine to 1536 MB (1.5 GB) of RAM. To change these settings, you 
will need to edit the Vagrantfile while the virtual machine is shut down.

(The % indicates that the command can be done from anywhere in the virtual 
 machine, regardless of working directory.)

Stop the web server by pressing Control-C in the SSH terminal.
Then shut down the virtual machine:
-------------------------------------------------------------------------------
% sudo shutdown -h now
-------------------------------------------------------------------------------

This will end the SSH session.

To increase the RAM allocated to the Virtualbox VM, edit the "vb.customize" 
line in the Vagrantfile by changing the number after the "--memory" flag.
-------------------------------------------------------------------------------
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", 1536]
  end
-------------------------------------------------------------------------------

After saving your changes, restart the VM and start the SSH session:
-------------------------------------------------------------------------------
> vagrant up --no-provision
> vagrant ssh
-------------------------------------------------------------------------------

In the SSH session, switch to makahiki/makahiki and start the server:
-------------------------------------------------------------------------------
vagrant@precise32:~$ cd /vagrant/makahiki 
-------------------------------------------------------------------------------

To start the server with manage.py:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000
-------------------------------------------------------------------------------

To start the server with gunicorn:
-------------------------------------------------------------------------------
vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000
-------------------------------------------------------------------------------
===============================================================================

Appendix F. Configure Networking on the Virtual Machine
===============================================================================
By default, the Vagrantfile specifies the IP address 192.168.56.4 for the 
virtual machine's eth1 interface. This is part of a host-only network. It 
assumes the host machine has the first usable address in the 192.168.56.0/24 
subnet, 192.168.56.1.

If the Makahiki site is unreachable from the host machine after the web 
server is started, the 192.168.56.0/24 network may not be correct.

To fix this, check the IP addresses assigned to VirtualBox's networking 
interfaces.
1. Open VirtualBox.

2. Go to File --> Preferences. This will launch the 
   "VirtualBox - Settings" window.

3. In the left sidebar, click "Network."

4. Click on "VirtualBox Host-Only Ethernet Adapter" once to select it, 
   and click the screwdriver icon (or the icon which, when moused over, shows 
   "Edit host-only network.")

5. The "Host-only Network Details" window should show the following:
   "IPv4 Address: 192.168.56.1
    IPv4 Network Mask: 255.255.255.0"
   If the settings are different, you will need to change the settings 
   in the Vagrantfile to match. Continue to the next step.

6. Open the Vagrantfile in a text editor. Look for the line:
   ----------------------------------------------------------------------------
   config.vm.network :private_network, ip: "192.168.56.4"
   ----------------------------------------------------------------------------
   Change the address in quotes after the "ip:" field to something 
   in the address range that was specified in "Host-only Network Details."
   For example, if the "IPv4 Address" is 192.168.56.1 and the 
   "IPv4 Network Mask" is 255.255.255.0, the range of usable addresses is 
   192.168.56.1 - 192.168.56.254. VirtualBox reserves the first usable 
   address, 192.168.56.1, for the host machine.
   An explanation of IPv4 network addresses is beyond the scope of this guide.

7. Switch to the directory holding the Vagrantfile. Then, reload the virtual 
   machine configuration.
   ----------------------------------------------------------------------------
   > vagrant reload
   ----------------------------------------------------------------------------

8. SSH into the virtual machine and check the network interfaces:
   ----------------------------------------------------------------------------
   > vagrant ssh
   Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic-pae i686)
   
    * Documentation:  https://help.ubuntu.com/
   Welcome to your Vagrant-built virtual machine.
   Last login: Thu Aug  8 07:55:06 2013 from 10.0.2.2
   vagrant@precise32:~$ ifconfig
   eth0      Link encap:Ethernet  HWaddr 08:00:27:12:96:98
             inet addr:10.0.2.15  Bcast:10.0.2.255  Mask:255.255.255.0
             inet6 addr: fe80::a00:27ff:fe12:9698/64 Scope:Link
   -- output omitted -- 
   eth1      Link encap:Ethernet  HWaddr 08:00:27:fd:05:73
             inet addr:192.168.56.4  Bcast:192.168.56.255  Mask:255.255.255.0
             inet6 addr: fe80::a00:27ff:fefd:573/64 Scope:Link
   -- output omitted --
   lo        Link encap:Local Loopback
             inet addr:127.0.0.1  Mask:255.0.0.0
             inet6 addr: ::1/128 Scope:Host
   -- output omitted --
   vagrant@precise32:~$
   ----------------------------------------------------------------------------
   The eth0 interface is used for port forwarding.
   The eth1 interface should match the IP address you just configured.
   The lo interface is the loopback interface.
   
9. Ping the host machine's "VirtualBox Host Adapter Network Address" 
   from the virtual machine. Press Control-C (^C) to stop.
   ----------------------------------------------------------------------------
   vagrant@precise32:~$ ping 192.168.56.1
   PING 192.168.56.1 (192.168.56.1) 56(84) bytes of data.
   64 bytes from 192.168.56.1: icmp_req=1 ttl=128 time=1.49 ms
   64 bytes from 192.168.56.1: icmp_req=2 ttl=128 time=0.710 ms
   64 bytes from 192.168.56.1: icmp_req=3 ttl=128 time=0.609 ms
   64 bytes from 192.168.56.1: icmp_req=4 ttl=128 time=0.685 ms
   ^C
   --- 192.168.56.1 ping statistics ---
   4 packets transmitted, 4 received, 0% packet loss, time 3000ms
   rtt min/avg/max/mdev = 0.609/0.874/1.493/0.359 ms
   vagrant@precise32:~$
   ----------------------------------------------------------------------------
   If the ping succeeds, then networking is correctly configured.
   
   From now on, you should use the IP address configured in the Vagrantfile 
   to access the site when the webserver is running.

For more information on VirtualBox host-only networking, see 
http://www.virtualbox.org/manual/ch06.html.
===============================================================================