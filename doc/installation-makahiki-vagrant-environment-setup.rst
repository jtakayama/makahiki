.. _section-installation-makahiki-vagrant-environment-setup:

Setting Up the Makahiki and Vagrant Development Environment
===========================================================

These instructions configure a VirtualBox Ubuntu 12.04 LTS 32-bit virtual 
machine with Vagrant, and download the Makahiki source code.

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

Download the Base Virtual Machine
---------------------------------

Download the base virtual machine image ``precise32`` from Vagrant's servers::

  > vagrant box add precise32 http://files.vagrantup.com/precise32.box
  
.. note:: It is only necessary to download each base virtual machine once. 
   Once downloaded, the "precise32" box can be reused by Vagrant to create 
   any virtual machines that specify "precise32" in their Vagrantfiles.
   
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

If you have Git or Git for Windows, you should be able to clone the repository from 
within the Command Prompt or Terminal.::

  > git clone http://github.com/csdl/makahiki.git

.. note:: Installing Git for Windows with default settings should let you use the 
   ``git clone`` command in the Command Prompt without opening Git for Windows. 
   
   If this does not work, you will need to use Git for Windows to execute the 
   ``git clone`` command instead.


Install Makahiki On Vagrant
---------------------------

To install Makahiki, continue to :ref:`section-installation-makahiki-vagrant-quickstart`.
  
  
  
  
  
