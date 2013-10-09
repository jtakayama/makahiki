.. _section-installation-makahiki-vagrant-quickstart:

Quick Start Guide: Makahiki on Vagrant 
======================================

If you have not already installed VirtualBox and Vagrant and downloaded the Makahiki source code, 
complete :ref:`section-installation-makahiki-vagrant-environment-setup` before completing this section.

.. note::
   Throughout this guide, a "``>``" indicates a command prompt on the host OS.
   
.. note::
   The "``makahiki>``" prompt indicates that the working directory is in the 
   "Makahiki directory" on the host machine. The file path preceding "makahiki"
   (e.g., "``C:\Users\username\Vagrant\makahiki>``") will be different depending 
   on the location of the directory in the file system.

If a Command Prompt (Windows) or Terminal (OS X and Linux) shell is not open on 
your host machine, open one.

Set up Makahiki in the Virtual Machine
--------------------------------------

In your Command Prompt or Terminal, switch your working directory to the
"makahiki" directory that was created in :ref:`section-installation-makahiki-vagrant-environment-setup`::

  > cd <path-to-makahiki>\makahiki
  
Replace ``<path-to-makahiki>`` with the file system path to the "makahiki" directory. On Windows, if 
your "makahiki" directory is located at ``C:\Users\username\Vagrant\makahiki``, you would use the command 
``cd C:\Users\username\Vagrant\makahiki`` here. On Linux, if your "makahiki" directory is at 
``/home/username/vagrant/makahiki``, you would use the command ``cd /home/username/vagrant/makahiki`` here.
  
The "makahiki" directory contains the Vagrantfile which defines the settings 
of the Vagrant virtual machine.

Use the ``vagrant up`` command to start the virtual machine for the first time::

  makahiki> vagrant up
  
.. warning:: Windows users may see multiple warnings while ``vagrant up`` is running for the first time.

     * **A Windows Firewall warning about vboxheadless.exe**: This application should be allowed.
     * **VirtualBox is attempting to make changes to the system**: This should be allowed. It is needed for Vagrant / VirtualBox host-only networking to work.
      
.. warning:: If you are not starting Vagrant for the first time and do not want to lose 
   your configuration, start Vagrant with ``--no-provision``::
   
     makahiki> vagrant up --no-provision

   Each time Vagrant is started with ``vagrant up``, it will run the 
   ``run_bootstrap.sh`` provisioning script specified in the Vagrantfile. This 
   script:
   
     * Sets the system locale to en_US.UTF-8
     * Drops the PostgreSQL cluster data directory, **erasing all data in all databases**
     * Re-initializes the cluster data directory
     * Re-initializes the Makahiki database
     
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

  makahiki> vagrant ssh

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

Check that the /vagrant directory on the virtual machine contains the files 
from the makahiki directory on the host machine. Enter the ``cd`` and ``ls`` commands 
as shown below. The output of the commands should be similar to this example::

  vagrant@precise32:~$ cd /vagrant
  vagrant@precise32:/vagrant$ ls
  DnD-example.html  Procfile   SGG_Designer_notes.txt  bootstrap.sh  deploy  makahiki          run_bootstrap.sh
  LICENSE.md        README.md  Vagrantfile             caminator     doc     requirements.txt  vagrant

Start the Server
----------------

Makahiki provides two web servers. runserver is better for development, and 
gunicorn is better for production use.

Switch to /vagrant/makahiki::

  vagrant@precise32:/vagrant$ cd /vagrant/makahiki
  
To start the runserver server::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000

To start the gunicorn server::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000

Verify that Makahiki Is Running
-------------------------------

Open a browser on the host machine and go to http://192.168.56.4:8000 to see 
the landing page, which should look similar to this:

  .. figure:: figs/vagrant/kukui-cup-demo-landing.png
      :width: 600 px
      :align: center

In the virtual machine, stop either server with control-c when you are finished::

  vagrant@precise32:/vagrant/makahiki$ (type control-c in the shell running the makahiki server process)

If the site is not reachable from your host machine, or your host machine is headless 
and has no GUI, refer to :ref:`section-installation-makahiki-vagrant-running-makahiki-vagrant` 
and follow the section on **Testing the Server Without a Web Browser**.



