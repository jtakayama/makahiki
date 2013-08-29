.. _section-installation-makahiki-vagrant-quickstart:

Quick Start Guide: Makahiki on Vagrant 
======================================

These instructions configure a VirtualBox Ubuntu 12.04 LTS 32-bit virtual 
machine with Vagrant and start the Makahiki server.

Throughout this guide, ``>`` indicates a command prompt on the host OS.

With the exception of Windows users, this guide assumes that you are using a 
Bourne-type shell (such as bash), which is the default on Mac OS X and Linux. 
Using a C-shell variant (like tcsh) is possible but not recommended.

Hardware Requirements
---------------------

A modern dual core CPU with 4 GB RAM should be sufficient to run the virtual machine.

Host Operating System Recommendations
-------------------------------------

The host OS is the OS that Vagrant and VirtualBox will be installed on. 
If your OS is not listed here, make sure that Vagrant and VirtualBox are 
available for your OS.

  * Windows 7 or 8
  * Mac OS X
  * Recent version of Red Hat Enterprise Linux, CentOS Linux, or Ubuntu Linux

Install VirtualBox
------------------

Download VirtualBox for your host OS by following the instructions 
on the `VirtualBox downloads page`_.

Follow the installation instructions for your operating system in 
Chapter 02 of the `VirtualBox manual`_. Select **Yes** 
when asked to install drivers for USB support and VirtualBox Host-Only Networking.

.. _VirtualBox downloads page: http://www.virtualbox.org/wiki/Downloads
.. _VirtualBox manual: https://www.virtualbox.org/manual/ch02.html

Install Vagrant
---------------

Download the `Vagrant installer`_ for your host OS. Vagrant 1.2.4 is recommended.

Follow the `Vagrant installation instructions`_.

.. _Vagrant installer: http://downloads.vagrantup.com/
.. _Vagrant installation instructions: http://docs.vagrantup.com/v2/installation/index.html

Vagrant Virtual Machine Setup
-----------------------------

Open a terminal on your system.

Windows
*******

Open a **Command Prompt** or type "cmd.exe" in **Run**.

Mac OS X
********

Open a **Terminal**. If your default shell is not **bash**, type ``bash`` to temporarily 
switch to a **bash** shell.

Linux
*****

Open a **Terminal**. If you are in a headless OS (no graphical user interface), you are 
already in the Terminal.

Download the Makahiki Source Code
---------------------------------

Downloading the Makahiki source code will create the "makahiki" directory.

There are two ways of obtaining the Makahiki source code: downloading it as 
an archive, or cloning the Git repository.

.. note:: The makahiki directory created by extracting the .zip or 
   cloning the repository will be the directory Vagrant uses as a 
   reference point for accessing the virtual machine.

Download the Archive
********************

Follow these instructions if you do not have **Git** or **Git for Windows**.

1. Go to https://github.com/csdl/makahiki
2. Click the button to "Download ZIP."
3. Extract the makahiki.zip file that is downloaded.

Clone the Repository
********************
  
Windows users can install `Git for Windows`_.

OS X and Linux users should be able to download Git for their operating 
system. See `GitHub's setup guide`_ for instructions.

.. _Git for Windows: http://git-scm.com/download/win
.. _Github's setup guide: http://help.github.com/articles/set-up-git

If you have Git or Git for Windows, you can clone the repository::

  > git clone http://github.com/csdl/makahiki.git

Download the Base Virtual Machine
---------------------------------

Download the base virtual machine image ``precise32`` from Vagrant's servers::

  > vagrant box add precise32 http://files.vagrantup.com/precise32.box
  
.. note:: It is only necessary to download each base virtual machine once. 
   Once downloaded, the "precise32" box can be reused by Vagrant to create 
   any virtual machines that specify "precise32" in their Vagrantfiles.
   
Set up Makahiki in the Virtual Machine
--------------------------------------

Cloning the repository or extracting the .zip file created a ``makahiki`` directory.
Switch your working directory to makahiki::

  > cd makahiki
  
This directory contains the Vagrantfile which defines the settings 
of the Vagrant virtual machine.

Use the ``vagrant up`` command to start the virtual machine::

  > vagrant up
  
.. warning:: Each time Vagrant is started with ``vagrant up``, it will run the 
   ``run_bootstrap.sh`` provisioning script specified in the Vagrantfile. This 
   script:
   
     * Sets the system locale to en_US.UTF-8
     * Drops the PostGreSQL cluster data directory, **erasing all data in all databases**
     * Re-initializes the cluster data directory
     * Re-initializes the Makahiki database
   
   If you are not starting Vagrant for the first time and do not want to lose 
   your configuration, start Vagrant with ``--no-provision``::
   
     > vagrant up --no-provision
     
.. warning:: Windows users may see multiple warnings while ``vagrant up`` is running for the first time.

     * A Windows Firewall warning about ``vboxheadless.exe``. This application should be allowed.
     * A warning that VirtualBox is attempting to make changes to the system. This should be allowed. It is needed for Vagrant / VirtualBox host-only networking to work.
      
The output of run_bootstrap.sh is logged to a file in makahiki/vagrant/logs.
This file will be called "ubuntu_x86_<timestamp>.log," where **timestamp** is a 
string in the format yy-mm-dd-HH-MM-SS (year, month, day, hour, minute, second).

When the script finishes, look at the last few lines of output::

  -------------------------------------------------------------------------------
  Configuration setup results:
  -------------------------------------------------------------------------------
  1. Copying locale settings to /etc/bash.bashrc: [Succeeded]
  2. Copying settings to pg_hba.conf: [Succeeded]
  3. Creating /home/vagrant/makahiki_env.sh: [Succeeded]
  4. Appending to /home/vagrant/.bashrc: [Succeeded]
  -------------------------------------------------------------------------------
  
If the value for a task is "Succeeded" or "Already completed," continue to the 
next step. If the value for a task is "Failed," go to :ref:`section-installation-makahiki-vagrant-troubleshooting`.

Connect to the Vagrant Virtual Machine
--------------------------------------

Start an SSH session with the Ubuntu virtual machine::

  > vagrant ssh

An Ubuntu command prompt will be displayed:: 

  vagrant@precise32:~$
  
.. note::
   You can end your SSH session by typing ``exit`` in the SSH terminal::

     vagrant@precise32:~$ exit 

Check for Makahiki Source Code
------------------------------

.. note:: The Vagrantfile is configured to mount the directory that contains 
   it as a synchronized folder called ``/vagrant`` at the root of the virtual 
   machine. Any file added to ``/vagrant`` on the virtual machine will be added to 
   ``makahiki`` on the host machine, and vice versa.

Check that the /vagrant directory on the virtual machine contains the same 
contents as the makahiki directory on the host machine::

  vagrant@precise32:~$ cd /vagrant
  vagrant@precise32:/vagrant$ ls
   
Start the Server
----------------

Makahiki provides two servers. runserver is better for development, and 
gunicorn is better for production.

Switch to /vagrant/makahiki::

  vagrant@precise32:/vagrant/$ cd /vagrant/makahiki
  
To start the server with manage.py::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000

To start the server with gunicorn::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000

The web server can be accessed in a browser on the host machine at 
http://192.168.56.4:8000.

In the virtual machine, stop either server with Control+C when you are finished.

If the site is not reachable from your host machine, or your host machine is headless 
and has no GUI, refer to :ref:`section-installation-makahiki-vagrant-running-makahiki-vagrant` 
and read the section on **Testing the Server Without a Web Browser**.




