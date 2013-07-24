ubuntu_x86_vagrant_readme.txt
=============================

Contents:
-------------------------------------------------------------------------------
0.0. Introduction
1.0. Prerequisites
1.0.1. Download the Makahiki Source Code
1.0.2. Install VirtualBox
1.0.3. Install Vagrant
[COMING SOON]
-------------------------------------------------------------------------------

0.0. Introduction.
===============================================================================
This is a README file that describes the process for deploying Makahiki in a 
Vagrant virtual machine on a Windows host machine.

If you would prefer to install Makahiki on Windows manually, without using 
Vagrant, see the documentation at:
http://makahiki.readthedocs.org/en/latest/installation-makahiki-windows.html

The Makahiki source code is available from https://github.com/csdl/makahiki.

WARNING:
-------------------------------------------------------------------------------
This guide should not be used to deploy Makahiki on a cloud-based hosting 
system such as Heroku. For instructions to deploy Makahiki on Heroku, see
http://makahiki.readthedocs.org/en/latest/installation-makahiki-heroku.html.
-------------------------------------------------------------------------------

In the examples in this document, the > represents the Windows command prompt.
===============================================================================

1.0. Prerequisites
===============================================================================
There are three prerequisites for setting up the Vagrant/Makahiki environment 
on Windows:
1. Download the Makahiki source code from Github
2. Install VirtualBox
3. Install Vagrant

Each of these steps is described in more detail below.
===============================================================================

1.0.1. Download the Makahiki Source Code
===============================================================================
There are two ways of obtaining the Makahiki source code.

A. If you do not have Git for Windows, download the source code from 
   Github as a .zip file:
- A1. In a web browser, go to https://github.com/csdl/makahiki.
- A2. Click the button to "Download ZIP."
- A3. Extract the makahiki.zip file that is downloaded.

B. If you have Git for Windows, you can clone the repository:
- B1. Change to the directory you want to download makahiki into and clone the 
  repository:
> git clone http://github.com/csdl/makahiki.git

Git for Windows can be downloaded from http://git-scm.com/download/win.
===============================================================================

1.0.2. Install VirtualBox
===============================================================================
Download VirtualBox from https://www.virtualbox.org/wiki/Downloads.
To install VirtualBox on Windows, follow the instructions at 
https://www.virtualbox.org/manual/ch02.html#installation_windows.

Select "Yes" when you are asked to install drivers for USB support and 
VirtualBox Host-Only Networking.
===============================================================================

1.0.3. Install Vagrant
===============================================================================
Download the Vagrant installer from http://downloads.vagrantup.com/.
To install Vagrant on Windows, follow the instructions at 
http://docs.vagrantup.com/v2/installation/index.html.
===============================================================================

[SECTIONS BELOW THIS LINE ARE UNDER REVISION]

Assuming you've downloaded the makahiki source code somewhere on your host machine:

1. Create a new directory for your Vagrant virtual machine. This guide uses 
   the example directory "ubuntu_x86_makahiki." A Vagrant virtual machine 
   can be "placed" anywhere. The virtual machine files will not really be located 
   here, but you will issue Vagrant commands for the virtual machine in this 
   directory.

> mkdir ubuntu_x86_makahiki
> cd ubuntu_x86_makahiki

2. Create the Vagrantfile for the new virtual machine. (This does not actually 
   create the virtual machine, it just defines its configuration file).

> vagrant init

3. Add an Ubuntu x86-architecture VirtualBox virtual machine. Use the 
   virtual machine at http://files.vagrantup.com/precise32.box:
   
> vagrant box add precise32 http://files.vagrantup.com/precise32.box

4. Open the Vagrantfile in a text editor and change the default contents 
   to the following:
-------------------------------------------------------------------------------
Vagrant.configure("2") do |config|
  config.vm.box = "precise32"
end
-------------------------------------------------------------------------------

5. If you have already downloaded the Makahiki source code, copy it into 
   the ubuntu_x86_makahiki directory. This assumes you are still in the 
   ubuntu_x86_makahiki directory.
> cp <path_to_makahiki>/makahiki ./makahiki

6. Copy bootstrap_runner.sh, bootstrap.sh, and the logs/ directory to 
   the current ubuntu_x86_makahiki directory from the makahiki directory: 
> cp ./makahiki/install/vagrant_scripts/ubuntu_x86/bootstratp_runner.sh ./bootstrap_runner.sh
> cp ./makahiki/install/vagrant_scripts/ubuntu_x86/bootstrap.sh ./bootstrap.sh
> cp ./makahiki/install/vagrant_scripts/ubuntu_x86/logs ./logs

7. [...]