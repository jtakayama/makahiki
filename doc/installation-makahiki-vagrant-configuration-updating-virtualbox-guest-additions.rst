.. _section-installation-makahiki-vagrant-configuration-updating-virtualbox-guest-additions.rst

Updating The VirtualBox Guest Additions
=======================================

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
is provided by your current installation of VirtualBox.

.. note: The default settings for the Vagrant virtual machine's Vagrantfile turn off automatic updates.
   Manual updates are covered later in this article.
   
Install vagrant-vbguest from the command line::

  vagrant plugin install vagrant-vbguest
  Installing the 'vagrant-vbguest' plugin. This can take a few minutes...
  Installed the plugin 'vagrant-vbguest (0.9.0)'!
  
Your version number may be different from the one in the example.

This article does not cover the full functionality of vbguest.
See the `vbguest readme`_ for the full documentation.

.. _vbguest readme: https://github.com/dotless-de/vagrant-vbguest/blob/master/Readme.md

Checking That A Virtual Machine Is Up To Date
---------------------------------------------

Open a Terminal or Command Prompt application, depending on your operating system.

Once you have opened a Terminal or Command Prompt, switch to your Makahiki directory.
This is the directory that is a clone of a Github repository. It was created when 
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
  
Instead of 4.3.0, you should see the version number that matches your 
VirtualBox version.

If the Versions Do Not Match
============================

If the Guest Additions do not match, you will see this output from the 
``vagrant vbguest --status`` command::

  > vagrant vbguest --status
  GuestAdditions versions on your host (4.3.0) and guest (4.2.0) do not match.  

To be able to update the Guest Additions, you will need to change the Vagrantfile 
settings temporarily.

When Updating is Necessary
==========================

Even if the Guest Addition versions do not match, the virtual machine may still 
work correctly. However, the following may occur:

* ``make html`` command fails to build documentation in /vagrant/doc
* Libraries or installed programs may not be detected

.. warning::
   Before continuing with this guide, make sure you have backed up any data 
   in the "makahiki" PostgreSQL database created for the Makahiki application.
   Completing the steps in this article will **erase all tables** in the database.

Enabling Automatic Guest Additions Updates in the Vagrantfile
=============================================================

[Content to be added later]

Updating the Guest Additions
=============================================================

[Content to be added later]

Disabling Automatic Guest Additions Updates in the Vagrantfile
==============================================================

[Content to be added later]