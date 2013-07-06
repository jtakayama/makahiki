#!/usr/bin/python

import sys
import os
import datetime
import datestring_functions
import dependency.dependency_ubuntu
import dependency.dependency_redhat
import pip.pip_install

def logfile_open(scripttype):
    """
    Returns an open logfile with a timestamp. It is left to the 
    calling function to write to the file and close it.
    
    This function will terminate the calling function if an IOError 
    occurs while opening the file.
    
    Parameters:
        1. scripttype: A string describing the installation script
           that is being run.
    """
    rundir = os.getcwd()
    logsdir = "/install/logs/"
    prefix = "install_" + scripttype + "_"
    dt = datetime.datetime
    date_suffix = "null"
    try:
        date_suffix = datestring_functions.datestring(dt)
    except ValueError as ve:
        print "ValueError:\n %s" % ve
        print "Bad datetime object, could not generate logfile name."
        print "Script will terminate."
        exit(1)
    # Assumes rundir is not terminated with a "/"
    logfile_path = rundir + logsdir + prefix + date_suffix + ".log"
    
    try:
        logfile = open(logfile_path, 'w')
        return logfile
    except IOError as ioe:
        print "IOError:\n %s" % ioe
        print "Could not open logfile at %s for writing." % logfile_path
        print "Script will terminate."
        exit(1)

def scriptrunner(scripttype, os, arch, logfile):
    """
    Chooses and runs an installation script, and which logfile 
    that script will write its output to.
    
    Though not all scripts are OS-dependent, the "os" and "arch" 
    variables are used to determine if the system is supported.
    
    Parameters:
        1. scripttype: A string describing the installation script
           that is being run.
           Supported values: "dependencies", "pip", "initialize_instance," "update_instance"
        2. os: A string describing the operating system.
           Supported values: "ubuntu" or "redhat"
        3. arch: Architecture. Supported values: "x86" or "x64".
            (Ubuntu is supported for x86 and x64; Red Hat is supported for x64.)
    """
    if os == "ubuntu" and (arch != "x86" and arch != "x64"):
        logfile.write("Unsupported architecture for %s: %s" % (os, arch))
        logfile.write("Script could not be completed.")
        print "Unsupported architecture for %s: %s" % (os, arch)
        print "Script could not be completed."
        
    elif os == "redhat" and arch != "x64":
        logfile.write("Unsupported architecture for %s: %s" % (os, arch))
        logfile.write("Script could not be completed.")
        print "Unsupported architecture for %s: %s" % (os, arch)
        print "Script could not be completed."
    
    else: 
        if scripttype == "dependencies":
            if os == "ubuntu":
                logfile = dependency.dependency_ubuntu.run(arch, logfile)
            elif os == "redhat":
                logfile = dependency.dependency_redhat.run(arch, logfile)
        elif scripttype == "pip":
                logfile = pip.pip_install.run(logfile)
        elif scripttype == "initialize_instance":
            print "Not implemented."
        elif scripttype == "update_instance":
            print "Not implemented."
        
        # After the function is done, close the logfile.
        logfile.close()

def main():
    if len(sys.argv) != 6:
        print "Usage: install.py [--dependencies | --pip | --initialize_instance | --update_instance] --os [ubuntu | redhat] --arch [x86 | x64]"
        print "--dependencies: Install Makahiki dependencies (software packages)."
        print "--pip: Install Makahiki local dependencies using pip."
        print "--initialize_instance: Initialize the Makahiki installation."
        print "--update_instance: Update the Makahiki installation."
        print "--os: Operating system. Supported values are ubuntu and redhat."
        print "--arch: Architecture. Supported values are x86 and x64 if your OS is ubuntu, or x64 if your OS is redhat."
    else:
        args = sys.argv[1:]
        scripttype = args[0].strip()[2:]
        os = args[2].strip()[2:]
        arch = args[4].strip()[2:]
        
        logfile = logfile_open(scripttype)
        scriptrunner(scripttype,os,arch,logfile)
        logfile.close()

if __name__ == '__main__':
    main()
