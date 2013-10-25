.. _section-installation-makahiki-vagrant-configuration-updating-virtualbox-guest-additions:

Updating The VirtualBox Guest Additions with vbguest
====================================================

.. note::
   This article is not applicable to any user whose VirtualBox version is 4.2.18 or lower.

This article covers only users who are using Virtualbox 4.3.0 and cannot use older versions 
of VirtualBox. It is not recommended that Makahiki on Vagrant be used with any VirtualBox version 
newer than 4.2.18.

If your version of VirtualBox uses a different version of the VirtualBox Guest Additions
than your Vagrant virtual machine, you will see this warning when you start the virtual machine::

  [default] The guest additions on this VM do not match the installed version of
  VirtualBox! In most cases this is fine, but in rare cases it can
  cause things such as shared folders to not work properly. If you see
  shared folder errors, please update the guest additions within the
  virtual machine and reload your VM.

  Guest Additions Version: 4.2.0
  VirtualBox Version: 4.3

This article covers the process of installing the **vagrant-vbguest** plugin on your system 
to update your virtual machine's installed Guest Additions automatically.

.. note::
   In the rest of this article, a "``>``" is used to indicate a generic command prompt 
   on any host OS (Windows, Mac OS X, or Linux). Commands appearing after a "``>``" prompt 
   in this article should work on all three operating systems. Though some systems automatically 
   append a space after the prompt, you do not need to type a space before a command.

Installing vagrant-vbguest
--------------------------

The **vagrant-vbguest** plugin runs automatically each time that a Vagrant virtual machine boots up 
with ``vagrant reload`` or ``vagrant up``. It installs the VirtualBox Guest Additions version that 
is provided by your host machine's current installation of VirtualBox.

.. note: The default settings for the Vagrant virtual machine's Vagrantfile turn off automatic updates.
   Manual updates are covered later in this article.
   
On your host machine, install vagrant-vbguest from the command line::

  vagrant plugin install vagrant-vbguest
  Installing the 'vagrant-vbguest' plugin. This can take a few minutes...
  Installed the plugin 'vagrant-vbguest (0.9.0)'!
  
Your version number may be different from the one in the example.

This article does not cover the full functionality of vbguest.
See the `vbguest readme`_ for the full documentation.

.. _vbguest readme: https://github.com/dotless-de/vagrant-vbguest/blob/master/Readme.md

Checking That A Virtual Machine Is Up To Date
---------------------------------------------

Open a Terminal or Command Prompt application on your host machine (the computer on which 
VirtualBox is installed).

Once you have opened a Terminal or Command Prompt, switch to your Makahiki directory.
This directory that is a clone of the Makahiki Github repository. It was created when 
you set up the virtual machine.

Start the virtual machine::

  > vagrant up --no-provision
  Bringing machine 'default' up with 'virtualbox' provider...
  [default] Clearing any previously set forwarded ports...
  [default] Creating shared folders metadata...
  [default] Clearing any previously set network interfaces...
  [default] Preparing network interfaces based on configuration...
  [default] Forwarding ports...
  [default] -- 22 => 2222 (adapter 1)
  [default] Running 'pre-boot' VM customizations...
  [default] Booting VM...
  [default] Waiting for machine to boot. This may take a few minutes...
  [default] Machine booted and ready!
  [default] Configuring and enabling network interfaces...
  [default] Mounting shared folders...
  [default] -- /vagrant

Next, use vbguest to check the status of your Guest Additions::

  > vagrant vbguest --status
  GuestAdditions 4.3.0 running --- OK.
  
Instead of 4.3.0, you should see a version number that matches your 
VirtualBox version.

If the Versions Do Not Match
****************************

If the Guest Additions do not match, you will see this output from the 
``vagrant vbguest --status`` command::

  > vagrant vbguest --status
  GuestAdditions versions on your host (4.3.0) and guest (4.2.0) do not match.  

To be able to update the Guest Additions, you will need to change the Vagrantfile 
settings temporarily.

.. warning::
   Conmpleting the instructions in this article will delete the "makahiki" database and fill 
   it with default users and settings.

When Updating is Necessary
**************************

Even if the Guest Addition versions do not match, the virtual machine may still 
work correctly. However, the following problems may occur:

* Running the make.bat script with ``make html`` fails to build documentation in /vagrant/doc, with errors similar to the below examples::
  
    vagrant@precise32:/vagrant/doc$ make html
    The program 'make' is currently not installed.  You can install it by typing:
    sudo apt-get install make
    
    vagrant@precise32:/vagrant/doc$ ./make.bat html
    ./make.bat: line 1: @ECHO: command not found
    ./make.bat: line 3: REM: command not found
    ./make.bat: line 5: syntax error near unexpected token `('
    ./make.bat: line 5: `if "%SPHINXBUILD%" == "" ('

* Libraries or installed programs are not detected

If you experience these problems, complete the instructions in this article to update your Guest Additions.

Enabling Automatic Guest Additions Updates in the Vagrantfile
-------------------------------------------------------------

In the host machine's Terminal or Command Prompt, shut down the virtual machine::

  > vagrant halt

On the host machine, open the Vagrantfile in a text editor.
Look for this line::

  config.vbguest.auto_update = false
  
Change this line to::

  config.vbguest.auto_update = true
  
Save the Vagrantfile and close it. 

As long as config.vbguest.auto_update is set to ``true``, vbguest will check the 
version of the Guest Additions that is installed in every virtual machine at startup. 
It will also attempt to update them if a newer version of the Guest Additions is 
available on your host machine.

Updating the Guest Additions
----------------------------

In the host machine's Terminal or Command Prompt, start the virtual machine::

  > vagrant up --provision

This will start the virtual machine. At this point, vbguest will attempt to 
update the Guest Additions, producing a lot of output. Eventually you will see 
output that is similar to this::

  Installing Virtualbox Guest Additions 4.3.0 - guest version is 4.2.0
  stdin: is not a tty
  Verifying archive integrity... All good.
  Uncompressing VirtualBox 4.3.0 Guest Additions for Linux............
  VirtualBox Guest Additions installer
  Removing installed version 4.2.0 of VirtualBox Guest Additions...
  Copying additional installer modules ...
  Installing additional modules ...
  Removing existing VirtualBox DKMS kernel modules ...done.
  Removing existing VirtualBox non-DKMS kernel modules ...done.
  Building the VirtualBox Guest Additions kernel modules
  Copy iso file C:\Program Files\Oracle\VirtualBox\VBoxGuestAdditions.iso into the
  box /tmp/VBoxGuestAdditions.iso
  stdin: is not a tty
  mount: warning: /mnt seems to be mounted read-only.
  Installing Virtualbox Guest Additions 4.3.0 - guest version is 4.2.0
  stdin: is not a tty
  Verifying archive integrity... All good.
  Uncompressing VirtualBox 4.3.0 Guest Additions for Linux............
  VirtualBox Guest Additions installer
  Removing installed version 4.2.0 of VirtualBox Guest Additions...
  Copying additional installer modules ...
  Installing additional modules ...
  Removing existing VirtualBox DKMS kernel modules ...done.
  Removing existing VirtualBox non-DKMS kernel modules ...done.
  Building the VirtualBox Guest Additions kernel modules ...done.
  Doing non-kernel setup of the Guest Additions ...done.
  You should restart your guest to make sure the new modules are actually used
  
  Installing the Window System drivers ...fail!
  (Could not find the X.Org or XFree86 Window System.)
  An error occurred during installation of VirtualBox Guest Additions 4.3.0. Some
  functionality may not work as intended.
  stdin: is not a tty
  [default] Waiting for machine to boot. This may take a few minutes...
  [default] Machine booted and ready!
  [default] Configuring and enabling network interfaces...
  [default] Mounting shared folders...
  [default] -- /vagrant
  
.. note::
   This warning can be safely ignored::
   
     Installing the Window System drivers ...fail!
     (Could not find the X.Org or XFree86 Window System.)
     An error occurred during installation of VirtualBox Guest Additions 4.3.0. Some
     functionality may not work as intended.
     
   The "precise32" virtual machine does not have X.Org or XFree86. It does not need 
   these programs because it has no applications that require a GUI. It does not need 
   the Window System drivers.
   
After this is complete, the system will run the rest of the provisioning script, 
reinstalling Makahiki dependencies and configuration files. This will take a while.
When the script finishes running, look at the last few lines of output::

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

Once the installation is finished, check that the guest additions version is correct::

  > vagrant vbguest --status
  GuestAdditions 4.3.0 running --- OK.

Continue to the next section.

Disabling Automatic Guest Additions Updates in the Vagrantfile
--------------------------------------------------------------

In the host machine's Terminal or Command Prompt, shut down the virtual machine::

  > vagrant halt

On the host machine, open the Vagrantfile in a text editor.
Look for this line::

  config.vbguest.auto_update = true
  
Change this line to::

  config.vbguest.auto_update = false
  
Save the Vagrantfile and close it. 

This will disable the automatic update checking that we configured previously.

Continue to the next section.

Optional: Build A Local Copy of the Makahiki Documentation
----------------------------------------------------------

Now that the Guest Additions have been updated, you can build a local version of the 
current documentation available at `http://makahiki.readthedocs.org`_. This is completely 
optional but can be useful if you are developing for Makahiki on your virtual machine.

.. _http://makahiki.readthedocs.org: http://makahiki.readthedocs.org/

Start an SSH connection to your virtual machine::

  > vagrant ssh
  Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic-pae i686)

   * Documentation:  https://help.ubuntu.com/
  Welcome to your Vagrant-built virtual machine.
  Last login: Wed Oct 23 03:26:08 2013 from 10.0.2.2
  vagrant@precise32:~$
  
Change your working directory to the /vagrant/doc directory::

  vagrant@precise32:~$ cd /vagrant/doc

Use the ``make html`` command::
  
  vagrant@precise32:/vagrant/doc$ make html

This will run the make.bat script, which will build all of the documentation into linked HTML files.
The result is a mirror of the full Makahiki documentation as it was on the date that you cloned the Makahiki repository.
  
On your host machine, you can view the HTML documentation by opening the HTML files in a web browser.
The documentation can be found in your Makahiki directory under the ``doc/_build/html`` directory.