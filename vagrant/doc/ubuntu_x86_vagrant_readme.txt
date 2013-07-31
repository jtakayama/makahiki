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
2.1.4. Environment Variables Verification
2.1.5. PostgreSQL Configuration Verification
2.1.6. Initialize Makahiki
2.1.7. Start the Server
2.1.8. Update the Makahiki Instance
Appendix A.0. Troubleshooting Configuration Files - Editing Configuration Files
Appendix A.0.1. Troubleshooting /etc/bash.bashrc
Appendix A.0.2. Troubleshooting pg_hba.conf
Appendix A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh
Appendix A.0.4. Troubleshooting /home/vagrant/.bashrc
Appendix B. Vagrant Commands
Appendix C. Re-Provisioning Vagrant
Appendix D. Configure the RAM of the Virtual Machine
Appendix E. Using Eclipse To Develop with Vagrant
Appendix F. Import Makahiki as an Eclipse Project

Instructions in appendices are optional.
-------------------------------------------------------------------------------

0.0. Introduction
===============================================================================
This is a README file that describes the process for deploying Makahiki in a 
Vagrant virtual machine on a Windows host machine. The virtual machine is 
intended for testing or development use. It is not suitable for use in a 
production deployment of the Makahiki software.

If you would prefer to install Makahiki on Windows manually, without using 
Vagrant, see the documentation at:
http://makahiki.readthedocs.org/en/latest/installation-makahiki-windows.html

The Makahiki source code is available from https://github.com/csdl/makahiki.

In the examples in this document, the > represents the Windows command prompt.

This guide assumes a basic level of familiarity with Windows.

System requirements:
- Operating System:
  - Windows 7 or 8 are recommended.
  - The applications used in this guide are compatible with 
    x86 (32-bit) and x64 (64-bit) operating systems.
  - The virtual machine that will be configured will have x86 architecture
    and is compatible with x86 or x64 host operating systems.
- Hardware:
  - CPU: Modern dual or quad core
  - RAM: 4 GB
  - The Vagrant virtual machine will be configured by default to have 1.5 GB 
    of RAM (1536 MB). To change this amount, see Appendix D.

WARNING:
-------------------------------------------------------------------------------
This guide should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

WARNING FOR DEVELOPERS:
-------------------------------------------------------------------------------
If you plan to use Makahiki for software development:

Though not required, it is STRONGLY RECOMMENDED that you use Eclipse or 
another integrated development environment (IDE) that can maintain 
UTF-8 encoding and LF line endings within the project. UTF-8 and LF line 
endings are required by certain Makahiki dependencies.

To set up Eclipse, see Appendix E.
To import Makahiki into Eclipse, see Appendix F.

Above all, DO NOT EDIT OR CREATE ANY FILES IN NOTEPAD:
1. Notepad ends lines with Windows line endings (CR-LF). Linux 
   applications expect LF endings and may have problems parsing CR-LF.
2. Notepad defaults to ANSI encoding when a file is saved. Some Linux 
   applications like PostgreSQL require UTF-8 input.
3. Notepad adds a Byte Order Mark (BOM) to the beginning of each new file
   that is saved with an encoding other than ANSI. On Linux, this appears 
   as random characters (e.g., "ï»?") that appear before the first word in 
   the file. Linux applications may not be able to process files that start 
   with a BOM.
4. If you are using Windows and accidentally add a BOM to a text file, you 
   can use the Notepad++ application to remove it. In Notepad++, use 
   "Encoding" --> "Encode in UTF-8 Without BOM" to remove the BOM from 
   the beginning of a text file. Doing this for each new file you create 
   is not recommended; it is easier if your IDE can enforce it for you.
-------------------------------------------------------------------------------
===============================================================================

1.0. VirtualBox and Vagrant Setup
===============================================================================
This section installs VirtualBox and Vagrant onto a Windows computer.

This guide uses the terms "virtual machine" and "host machine." 
A virtual machine is an operating system running on simulated hardware, which 
is simulated using the hardware of the host machine. The host machine is the 
computer that Vagrant and VirtualBox use to run the virtual machine.
===============================================================================

1.0.1. Install VirtualBox
===============================================================================
Download VirtualBox from https://www.virtualbox.org/wiki/Downloads.
To install VirtualBox on Windows, follow the instructions at 
https://www.virtualbox.org/manual/ch02.html#installation_windows.

Select "Yes" when you are asked to install drivers for USB support and 
VirtualBox Host-Only Networking.

This guide was tested with VirtualBox 4.2.16. It should be compatible with 
later versions, but this has not been tested.
===============================================================================

1.0.2. Install Vagrant
===============================================================================
Download the Vagrant .msi installer from http://downloads.vagrantup.com/.
To install Vagrant on Windows, follow the instructions at 
http://docs.vagrantup.com/v2/installation/index.html.

This guide was tested with Vagrant 1.2.4. It should be compatible with 
later versions of Vagrant 1.2, but this has not been tested.
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
text file, you likely already have the Makahiki source code, and can skip this 
section.)

A. If you do not have Git for Windows, download the source code from 
   Github as a .zip file:
    A1. In a web browser, go to https://github.com/csdl/makahiki.
    A2. Click the button to "Download ZIP."
    A3. Extract the makahiki.zip file that is downloaded.

B. If you have Git for Windows, you can clone the repository:
   > git clone http://github.com/csdl/makahiki.git

Git for Windows can be downloaded from http://git-scm.com/download/win.

Now switch your working directory to makahiki:
> cd makahiki
===============================================================================

2.0.2. Download the Base Virtual Machine
===============================================================================
This step adds the base virtual machine specified in the last step, 
"precise32," for Vagrant to use.

> vagrant box add precise32 http://files.vagrantup.com/precise32.box

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

> vagrant up

Each time you start Vagrant with "vagrant up," it will run the 
"run_bootstrap.sh" script specified in the Vagrantfile. This 
script runs and logs the "bootstrap.sh" script.

(Later, if you want to start the virtual machine without provisioning 
 it, use --no-provision: vagrant up --no-provision)

The bootstrap.sh script: 
1. Updates the apt package lists
2. Sets the system encoding and locale to en_US.UTF8
   - Note that this will also set the system time to UTC.
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
4. Creates /home/vagrant/makahiki_env.sh, which sets Makahiki environment 
   variables in the shell
5. Edits /home/vagrant/.bashrc so it will source /home/vagrant/makahiki_env.sh
6. Initializes the postgresql cluster data directory with en_US.UTF-8 encoding
7. Copies the Makahiki pg_hba.conf file over the default pg_hba.conf file

The bootstrap_runner.sh script logs the output of bootstrap.sh to a text 
file in the logs directory. This file is called "ubuntu_x86_<timestamp>.log,"
where <timestamp> is in the format yyyy-mm-dd-HH-MM-SS (year, month, day, 
hour, minute, second).

If run more than once, the script will:
1. Installs packages only on its first run.
2. Overwrites bash.bashrc and /home/vagrant/.bashrc only on its first run.
3. Creates /home/vagrant/makahiki_env.sh only on its first run, or 
   unless it is deleted.
4. [WARNING] Reset the PostgreSQL cluster data directory, which 
   erases all databases on the system.  This happens each time that the 
   script is run.

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

If Task 1's result is "Failed," go to "A.0.1. Troubleshooting bash.bashrc"
If Task 2's result is "Failed," go to "A.0.2. Troubleshooting pg_hba.conf"
If Task 2's result is "Failed," go to "A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh" 
If Task 4's result is "Failed," go to "A.0.4. Troubleshooting /home/vagrant/.bashrc" 
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
vagrant@precise32:~$ cd /vagrant
vagrant@precise32:/vagrant/$ ls

The output of ls should match the contents of the makahiki directory on your 
host machine.
===============================================================================

2.1.4. Environment Variables Verification
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
If "echo" returns nothing, or you want to change the administrator username or 
password, see "A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh."

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
vagrant@precise32:/vagrant$ psql -U postgres
psql (9.1.9)
Type "help" for help.

postgres=#\q
vagrant@precise32:/vagrant$
-------------------------------------------------------------------------------
If this fails, go to section "Appendix A.0.2: Troubleshooting pg_hba.conf."
===============================================================================

2.1.6. Initialize Makahiki
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
vagrant@precise32:~/$ cd /vagrant/makahiki
vagrant@precise32:/vagrant/makahiki$ ./scripts/initialize_instance.py --type default

You will need to answer "Y" to the question "Do you wish to continue (Y/n)?"

If the script causes errors while connecting to the database, see 
"Appendix A.0.2. Troubleshooting pg_hba.conf".
===============================================================================

2.1.7. Start the Server
===============================================================================
This guide assumes you are currently in the directory /vagrant/makahiki on 
your virtual machine.

You can now start the web server using manage.py or gunicorn. The manage.py 
web server is better for development, while gunicorn is better for production 
use. It is important to bind the server to IP 0.0.0.0 (accepts incoming connections 
on any IP address) and port 8000 in order to work with the port forwarding settings 
in the Vagrantfile.

To start the server with manage.py:
vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000

To start the server with gunicorn:
vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000

View the site in your host machine's web browser at http://localhost:8001.
===============================================================================

2.1.8. Update the Makahiki Instance
===============================================================================
Makahiki is designed to support post-installation updating of your configured 
system when bug fixes or system enhancements become available. Updating an 
installed Makahiki instance using the ubuntu_installer.py script requires the 
following steps:

(The % indicates that the command can be done from anywhere in the virtual 
 machine, regardless of working directory.)

(1.) Close the running server in the shell process that is running Makahiki:
(type control-c in the shell running the makahiki server process)

(2.) Go to the vagrant directory (this is the makahiki directory 
     on the host machine):
% cd /vagrant
vagrant@precise32:/vagrant$

(3.) Download the updated source code into the Makahiki installation:
vagrant@precise32:/vagrant$ git pull origin master

(4.) Run the update_instance.py script:
vagrant@precise32:/vagrant$ cd makahiki
vagrant@precise32:/vagrant$ ./scripts/

(5.) Start the server with runserver or gunicorn:
To start the server with manage.py:
% ./manage.py runserver

To start the server with gunicorn:
% ./manage.py run_gunicorn
===============================================================================

Appendix A.0. Troubleshooting Configuration Files - Editing Configuration Files
===============================================================================
Appendix A contains troubleshooting instructions for configuration files.
The instructions refer to the GNU nano text editor, which is installed 
by default in the "precise32" Ubuntu virtual machine. GNU nano is one of many 
Linux text editors (including vi, emacs, pico, etc.)

Basic nano Controls
-------------------
Move the cursor with the arrow keys.
Type to insert text at the cursor.
Ctrl-G (^G) opens Help and Ctrl-X (^X) closes it.
Ctrl-O (^O) saves the document.
Ctrl-X (^X) closes a document.
Ctrl-W (^W) searches the document for a string that you specify.
Ctrl-Y (^Y) is Page Up.
Ctrl-V (^V) is Page Down.
Ctrl-K (^K) cuts the entire current line.
Ctrl-U (^U) pastes the last line that was cut.
Ctrl-C (^C) shows the current position of the cursor in a readout at the 
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
If the UTF-8 settings were not properly applied, you will need to reconfigure 
the system encodings.

Open /etc/bash.bashrc with sudo:
vagrant@precise32:~$ sudo nano /etc/bash.bashrc

Add these lines to the end of the file:
-------------------------------------------------------------------------------
# UTF-8 locale settings for Makahiki
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
-------------------------------------------------------------------------------
After you are done editing the file, run these commands:

vagrant@precise32:~$ sudo locale-gen en_US.UTF-8
vagrant@precise32:~$ sudo dpkg-reconfigure locales
vagrant@precise32:~$ sudo pg_dropcluster 9.1 main --stop
vagrant@precise32:~$ sudo pg_createcluster --locale en_US.UTF8 9.1 main
vagrant@precise32:~$ sudo /etc/init.d/postgresql restart
===============================================================================

Appendix A.0.2. Troubleshooting pg_hba.conf
===============================================================================
If you cannot connect to the database with "psql -U postgres," or experience 
errors when running initialize_instance.py, check that the pg_hba.conf file 
has the correct settings applied.

On Ubuntu 12.04 LTS, pg_hba.conf is at /etc/postgresql/9.1/main/pg_hba.conf. 
Open it in the nano text editor with sudo (root) privileges:

vagrant@precise32:/vagrant$ sudo nano /etc/postgresql/9.1/main/pg_hba.conf

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
vagrant@precise32:/vagrant$ sudo /etc/init.d/postgresql restart
===============================================================================

Appendix A.0.3. Troubleshooting /home/vagrant/makahiki_env.sh
===============================================================================
If MAKAHIKI_DATABASE_URL and MAKAHIKI_ADMIN_INFO are still not set after 
sourcing ~/.bashrc, you need to add them to /home/vagrant/makahiki_env.sh.

Create this file if it does not exist:

vagrant@precise32:~$ touch makahiki_env.sh

Open the file in the nano text editor. (The ~ is a shortcut for the 
current user's home directory, which is /home/vagrant.)

vagrant@precise32:~$ nano makahiki_env.sh

The file should contain the lines shown below:
-------------------------------------------------------------------------------
# Makahiki environment variables
# Syntax: postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
export MAKAHIKI_DATABASE_URL=postgres://makahiki:makahiki@localhost:5432/makahiki
# Syntax: <admin_name>:<admin_password>
export MAKAHIKI_ADMIN_INFO=admin:admin
-------------------------------------------------------------------------------

When you are done editing makahiki_env.sh, source the .bashrc file. This will 
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

vagrant@precise32:~$ nano ~/.bashrc

Add the line "source /home/vagrant/makahiki_env.sh" to the end of the file.
Save the file and source it for changes to take effect:
vagrant@precise32:~$ source ~/.bashrc
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
vagrant destroy: Deletes a virtual machine. The Vagrantfile is not deleted.

The Vagrant 1.2 documentation can be found at http://docs.vagrantup.com/v2/.
===============================================================================

Appendix C. Re-Provisioning Vagrant
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

Appendix D. Configure the RAM of the Virtual Machine
===============================================================================
The default settings in the Vagrantfile that comes with this project limit 
the virtual machine to 1536 MB (1.5 GB) of RAM. To change these settings, you 
will need to edit the Vagrantfile while the virtual machine is shut down.

(The % indicates that the command can be done from anywhere in the virtual 
 machine, regardless of working directory.)

Stop the web server by pressing Ctrl-C in the SSH terminal.
Then shut down the virtual machine:
% sudo shutdown -h now

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

In the SSH session, switch to makahiki/makahiki and start the server with 
manage.py or gunicorn:

vagrant@precise32:~$ cd /vagrant/makahiki 

To start the server with manage.py:
vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000

To start the server with gunicorn:
vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000
===============================================================================

Appendix E. Using Eclipse To Develop with Vagrant
===============================================================================
Developing in Eclipse is OPTIONAL. However, Eclipse is the development 
environment of the Makahiki development team, and .project and .pydevproject 
are provided for the convenience of Eclipse users.

Host Machine Prerequisites:
[REQUIRED] Python 2.7.3 or later (but not Python 3).
[REQUIRED] Java JRE or JDK (Java 6 or newer required)
[REQUIRED] Eclipse IDE (Eclipse 4.2 Juno or newer recommended)
[REQUIRED] PyDev Eclipse Add-on
[REQUIRED] Configure Line Endings and Character Encodings
[OPTIONAL] Eclipse Add-ons: Web, XML, Java EE and OSGi Enterprise Development:
           - [RECOMMENDED] Eclipse Web Developer Tools (HTML/XHTML/CSS editors)
           - [RECOMMENDED] JavaScript Development Tools (JavaScript editor)
[OPTIONAL] Set Hidden Files and Folders as Visible

Prerequisites: Python [REQUIRED]
-------------------------------------------------------------------------------
For Python binaries and installation instructions, see http://python.org.
- Makahiki requires Python 2.7.3 or later, or a newer version of Python 2.
- Makahiki IS NOT compatible with Python 3.
-------------------------------------------------------------------------------

Prerequisites: Eclipse [REQUIRED]
-------------------------------------------------------------------------------
Eclipse is an Integrated Development Environment (IDE) available 
from http://eclipse.org. 
- If you do not have Eclipse, follow the instructions at 
  http://wiki.eclipse.org/Eclipse/Installation.
- Eclipse requires that the Java JRE (Java 6 or later) be installed on the host 
  machine. The full Java JDK (which includes the JRE) is useful for Java 
  development, but it is NOT required for Makahiki development.
-------------------------------------------------------------------------------

Prerequisites: PyDev [REQUIRED]
-------------------------------------------------------------------------------
PyDev is an Eclipse add-on that is required for Python development. 
See http://pydev.org for installation instructions.
-------------------------------------------------------------------------------

Prerequisites: Configure Line Endings and Character Encodings [REQUIRED]
-------------------------------------------------------------------------------
If you are using Eclipse, it is very important to set these preferences before 
editing any of the project files or creating new ones.

1. In Eclipse, go to Window --> Preferences.
2. Go to Preferences --> General --> Workspace. Click DIRECTLY ON "Workspace."
3. In "Workspace:" 
   3a. Under "Text File Encoding," select "Other," then select "UTF-8" from 
       the dropdown menu. 
   3b. Under "New Text File Line Delimiter," select "Other," then select 
       "Unix" from the dropdown menu.
5. Click "Apply" when finished.
-------------------------------------------------------------------------------

Prequisites: Web Development Add-Ons [OPTIONAL]
-------------------------------------------------------------------------------
The "Web, XML, Java EE and OSGi Enterprise Development" set of add-ons is 
available from within Eclipse. None of these add-ons are required for Python 
development, but some are useful for general web development. Makahiki 
uses Django and contains JavaScript, HTML, and CSS files.

1. In the Help menu, select "Install New Software."
2. For the "Work with:" dropdown menu, select the "releases" URL that matches 
   your Eclipse version. For Eclipse 4.2 Juno, for example, this 
   would be "Juno - http://download.eclipse.org/releases/juno."
3. In the list of packages that appears below, click on the 
   arrow to the left of "Web, XML, Java EE and OSGi Enterprise Development."
   to expand the category. 
   - The "Eclipse Web Developer Tools" provide HTML/XHTML/CSS editors.
   - The "JavaScript Development Tools" provide a JavaScript (.js) editor.
4. Check the boxes for the add-ons you want to install. 
5. Click "Next," then "Next." You may need to agree to one or more licenses.
6. Restart Eclipse when prompted. After the restart, any new editors or 
   features will be installed and ready for use.
-------------------------------------------------------------------------------

Prerequisites: Set Hidden Files and Folders as Visible [OPTIONAL]
-------------------------------------------------------------------------------
1. Open Eclipse.
2. In the "Package Explorer" sidebar, click on the white down-pointing arrow 
   (the leftmost toolbar item). In this menu, click "Filters."
3. In the "Java Element Filters" popup that appears, uncheck the checkbox 
   for ".*resources," then click "OK."
4. The hidden files and folders that start with a "." character (e.g., 
   ".project" and ".pydevproject") should now be visible in Eclipse.
-------------------------------------------------------------------------------
===============================================================================

Appendix F. Import Makahiki as an Eclipse Project
===============================================================================
If you followed the previous instructions to set up a Vagrant virtual machine 
in the earlier part of this guide, your Vagrant virtual machine and its 
.vagrant folder should be located at the top level of the cloned makahiki 
repository, where the Vagrantfile is.

Importing the makahiki directory as an Eclipse project when the makahiki 
directory is also the Vagrant shared directory allows you to modify Makahiki 
source files on your host machine, then deploy the changes in your Vagrant 
virtual machine immediately.

1. Open Eclipse.
2. When prompted to select a workspace, select the directory that you cloned the 
   Makahiki repository into earlier (e.g., the directory that contains the 
   top-level makahiki folder). For example, if Makahiki had been cloned into 
   C:/Users/Tester/Vagrant, that would be the workspace directory.   Click "OK."
3. Select File --> Import.
    3a. Click the arrow to expand "General," then select 
        "Existing Projects Into Workspace." Click "Next."
    3b. Uncheck the checkbox for "Copy Projects into Workspace."
        Then select the top-level makahiki directory as the root directory.
        For example, if Makahiki had been cloned into C:/Users/Tester/Vagrant, 
        the root directory of the project would be located at 
        C:/Users/Tester/Vagrant/makahiki.
    3c. Check the checkbox for "makahiki" when it appears. Click "Finish."
4. Assuming that you installed PyDev, you will receive a warning:
   "It seems that the Python interpreter is not currently configured."
   Select "Auto config" if your Python interpreter is on the Windows PATH; 
   otherwise, use "Manual config" to select it manually. These instuctions 
   assume you selected "Auto config."
5. If you selected "Auto config," you will get a "Selection needed" popup.
   The defaults are usually fine. Click "OK" to continue. 
6. You will be shown the "Interpreter - Python" menu.
   Click "Apply" to configure the Pythonpath for Eclipse.
   If you need to change these libraries later, go to 
   "Window" --> "Preferences" --> "PyDev" --> "Interpeter - Python," 
   and select the "Libraries" tab.
===============================================================================