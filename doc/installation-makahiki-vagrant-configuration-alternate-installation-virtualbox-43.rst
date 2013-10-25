.. _section-installation-makahiki-vagrant-configuration-alternate-installation-virtualbox-43

Alternate Installation: Installing Makahiki on Vagrant with Virtualbox 4.3.0
============================================================================

.. note::
   This article is not applicable to any user whose VirtualBox version is 4.2.18 or lower.

This is not the recommended installation method to deploy Makahiki in a 
virtual machine. It is provided for those users who are using Virtualbox 4.3.0 
and cannot use older versions of VirtualBox. It is not recommended that 
Makahiki on Vagrant be used with any VirtualBox version newer than 4.2.18.

These instructions configure a VirtualBox Ubuntu 12.04 LTS 32-bit virtual 
machine with Vagrant, and download the Makahiki source code.

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

.. note::
   This guide assumes that you will be using VirtualBox version 4.3.0 or later.

Download VirtualBox for your host OS by following the instructions 
on the `VirtualBox downloads page`_.

Follow the installation instructions for your operating system in 
Chapter 02 of the `VirtualBox manual`_. Select **Yes** 
when asked to install drivers for USB support and VirtualBox Host-Only Networking.

.. _VirtualBox downloads page: http://www.virtualbox.org/wiki/Downloads
.. _VirtualBox manual: https://www.virtualbox.org/manual/ch02.html

Install Vagrant
---------------

Download the `Vagrant installer`_ for your host OS. Only Vagrant 1.3.5 and later are compatible with Virtualbox 4.3.0.

Follow the `Vagrant installation instructions`_.

.. _Vagrant installer: http://downloads.vagrantup.com/
.. _Vagrant installation instructions: http://docs.vagrantup.com/v2/installation/index.html

Open A Command Line Application
-------------------------------

Open a command line terminal on your system. The Windows terminal is called "Command Prompt." 
The Mac OS X terminal is called "Terminal." Most Linux systems with a graphical user interface 
call their terminal "Terminal."

Terminals usually begin each input prompt with the directory (also called a "folder") that is the user's 
current location in the file system. This is called the "working directory." Terminals 
usually end their input prompt with a special character (e.g., ``>``, ``#``, or ``$``).

When a user types a system command or program-specific command at the input prompt
and presses Enter, the operating system runs the program specified by the command.

.. note::
   In the rest of this article, a "``>``" is used to indicate a generic command prompt 
   on any host OS (Windows, Mac OS X, or Linux). Commands appearing after a "``>``" prompt 
   in this article should work on all three operating systems. Though some systems automatically 
   append a space after the prompt, you do not need to type a space before a command.
   
Windows
*******

Open a **Command Prompt** or type ``cmd.exe`` in **Run**.

An example of the Windows Command Prompt:

  .. figure:: figs/vagrant/example-windows-command-prompt.png
      :width: 600 px
      :align: center

The Windows command prompt opens with a working directory of ``C:\Users\<username>``, where ``<username>`` is the 
username of the current user. A Windows command prompt that has been opened with "Run as 
Administrator" opens in ``C:\Windows\system32``.

This guide does not require a Command Prompt to be run as an Administrator. However, 
administrative privileges may be required to resolve security and permissions issues related 
to Vagrant.

Mac OS X
********

Open a **Terminal**. If your default shell is not **bash**, type ``bash`` to temporarily 
switch to a **bash** shell. 

If you are using a recent version of OS X, you will not need to change the shell unless 
you changed the default shell in the past. The bash shell has been the default shell since 
OS X 10.3.

An example of the OS X Terminal:

  .. figure:: figs/vagrant/example-osx-terminal.png
      :width: 600 px
      :align: center

The ``~`` indicates that the user is in their user home directory. 

Linux
*****

Open a **Terminal**. If you are using a headless OS (an OS that does not have a graphical user interface), you are 
already in the Terminal.

Though every Linux distribution does this a little differently, most distributions 
open a terminal with a command prompt of the form::

  <username>@<computer_name>:<working_directory>$

An example of a Terminal shell window from Ubuntu Linux:

  .. figure:: figs/vagrant/example-ubuntu-terminal.png
      :width: 600 px
      :align: center

The ``~`` indicates that the user is in their user home directory. 
On Ubuntu, this is equivalent to ``/home/username``.
  
Download the Base Virtual Machine
---------------------------------

Download the base virtual machine image ``precise32`` from Vagrant's servers::

  > vagrant box add precise32 http://files.vagrantup.com/precise32.box
  
.. note:: It is only necessary to download each base virtual machine ("box") 
   once per user account on the host OS. Once the "precise32" box has been downloaded, 
   it can be reused by Vagrant to create any virtual machines that specify "precise32" 
   in their Vagrantfiles. If your host OS is Windows and you switch to another 
   user account, you will need to download the "precise32" box again.
   
Download the Makahiki Source Code
---------------------------------

Downloading the Makahiki source code will create the "makahiki" directory.

There are two ways of obtaining the Makahiki source code: downloading it as 
an archive, or cloning the Git repository.

.. note:: The "makahiki" directory created by extracting the .zip file or 
   cloning the repository will be the directory Vagrant uses as a 
   reference point for accessing the virtual machine. This guide refers 
   to that directory as the "makahiki directory."

Download the Archive
********************

Follow these instructions if you do not have **Git** or **Git for Windows** and are 
unable to install them.

1. Go to https://github.com/csdl/makahiki
2. Click the button to "Download ZIP."
3. Extract the makahiki.zip file that is downloaded.
4. Move the extracted "makahiki" directory to the directory you want to start the Vagrant virtual machine from.

Clone the Repository
********************

Follow these instructions if you have installed or are going to install Git or Git for Windows.
  
Windows users can install `Git for Windows`_.

OS X and Linux users should be able to download Git for their operating 
system. See `GitHub's setup guide`_ for instructions.

.. _Git for Windows: http://git-scm.com/download/win
.. _Github's setup guide: http://help.github.com/articles/set-up-git

After installing Git or Git for Windows on your operating system, go back
to your Command Prompt or Terminal.

In the Command Prompt or Terminal, change your working directory to the 
directory you want to place the Makahiki source code directory in::

  > cd <path-to-directory>

For example, if you wanted the source code to be in ``C:\Users\username\Vagrant``, you 
would use the command ``cd C:\Users\username\Vagrant`` to change your working directory.

An example in Windows:

  .. figure:: figs/vagrant/windows-command-prompt-vagrant.png
      :width: 580 px
      :align: center

Then, enter this command in your Command Prompt or Terminal to 
clone the repository::

  > git clone http://github.com/csdl/makahiki.git

.. note:: If the "git clone" command does not work in the Windows Command Prompt, 
   you will need to use the "git clone" command in the Git for Windows terminal instead.

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

Start the virtual machine with ``vagrant up``::

  > vagrant up
  
Connect to the Vagrant Virtual Machine
--------------------------------------

Start an SSH session with the Ubuntu virtual machine::

  makahiki> vagrant ssh

An Ubuntu command prompt will be displayed:: 

  vagrant@precise32:~$

Start the Server
----------------

.. note:: The /vagrant directory that contains /vagrant/makahiki is a special directory 
   that is synchronized with the "makahiki" directory (folder) on your host OS. 
   
     * Any file added to ``/vagrant`` on the virtual machine will be added to ``makahiki`` on the host machine. 
     * Any file added to ``makahiki`` on the host machine will be added to ``/vagrant`` on the virtual machine.

To start one of the two web servers that Makahiki provides, switch to the 
/vagrant/makahiki directory::

  vagrant@precise32:~$ cd /vagrant/makahiki
  
The two servers are runserver, which is better for development, and gunicorn, 
which is better for production use.
  
To start the runserver server::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000
  
Example output of starting runserver::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000
  Validating models...

  0 errors found
  Django version 1.4, using settings 'settings'
  Development server is running at http://0.0.0.0:8000/
  Quit the server with CONTROL-C.

To start the gunicorn server::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000

Example output of starting gunicorn::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000
  Validating models...
  0 errors found
  
  Django version 1.4, using settings 'settings'
  Server is running
  Quit the server with CONTROL-C.
  2013-10-11 01:59:41 [1399] [INFO] Starting gunicorn 0.13.4
  2013-10-11 01:59:41 [1399] [INFO] Listening at: http://0.0.0.0:8000 (1399)
  2013-10-11 01:59:41 [1399] [INFO] Using worker: sync
  2013-10-11 01:59:41 [1408] [INFO] Booting worker with pid: 1408

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

Makahiki Maintenance Tasks
--------------------------

The basic installation of Makahiki is now complete.

To learn how to reset or update the Makahiki database, continue to 
:ref:`section-installation-makahiki-vagrant-running-makahiki-vagrant`.

Exit Your SSH Session
---------------------

When you are finished working with the Vagrant virtual machine,
end your SSH session by typing ``exit`` in the SSH terminal::

     vagrant@precise32:/vagrant/makahiki$ exit 

On your host OS, you will be returned to the terminal that started the SSH session.




