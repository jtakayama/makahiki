README.md for makahiki/install
===============================

This is a lower-level README for the Makahiki installation scripts.

The goal of this fork of Makahiki is to produce a set of 
Python scripts which further automate the process of installing 
Makahiki on Ubuntu Linux x86, Ubuntu Linux x64, and Redhat x64.

Makahiki is available at https://github.com/csdl/makahiki.

The install/ folder contains the install.py script and its dependencies:<br/>
1. install.py<br/>
   Usage: sudo python install.py [--dependencies | --pip] --os [ubuntu | redhat] --arch [x86 | x64]<br/>
   --dependencies: Runs one of the scripts in install/dependency, depending on the --os and --arch flags.<br/>
   --pip: Runs "pip install -r requirements.txt" and checks that all packages in requirements.txt were installed."<br/>
   --os: Only ubuntu (Ubuntu Linux) or redhat (Red Hat Enterprise Linux)
         will be supported. Only Ubuntu support is currently implemented.<br/>
   --arch: Ubuntu has x86 and x64 support. Only x64 support will be implemented for Redhat.<br/>
   <br/>
   The script must run with root privileges in order to install software packages.

   Future versions of the script will run the initialize\_instance.py and update\_instance.py scripts as well.
