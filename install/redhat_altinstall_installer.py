#!/usr/local/bin/python2.7

import sys
import os
import datetime
import datestring_functions
import dependency.dependency_redhat_altinstall
import pip.pip_install
import run_update_instance
import run_initialize_instance

# NOTE:
# This is the script to use if the default version of Python on
# your system is not a Python 2.7 version that is at least 
# Python 2.7.3. It assumes Python 2.7.3 was compiled and 
# installed using make altinstall.

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
           Supported values: "redhat"
        3. arch: Architecture. Supported values: "x86" or "x64".
           Red Hat is supported for x64.
        4. logfile: The log file to pass to the installation script.
    """
    if os == "ubuntu":
        logfile.write("This is not the script for Ubuntu Linux. Use ubuntu_installer.py instead.\n")
        logfile.write("Script could not be completed.\n")
        print "This is not the script for Ubuntu Linux. Use ubuntu_installer.py instead.\n"
        print "Script could not be completed.\n"
    elif os == "redhat" and arch != "x64":
        logfile.write("Unsupported architecture for %s: %s" % (os, arch))
        logfile.write("Script could not be completed.")
        print "Unsupported architecture for %s: %s" % (os, arch)
        print "Script could not be completed."
    elif os != "ubuntu" and os != "redhat":
        logfile.write("Unsupported operating system: %s" % os)
        logfile.write("Script could not be completed.")
        print "Unsupported operating system: %s" % os
        print "Script could not be completed."
    else: 
        if scripttype == "dependencies":
            if os == "redhat":
                logfile = dependency.dependency_redhat_altinstall.run(arch, logfile)
            elif os == "ubuntu":
                logfile.write("This is not the script for Ubuntu Linux. Use ubuntu_installer.py instead.\n")
                logfile.write("Script could not be completed.\n")
                print "This is not the script for Ubuntu Linux. Use ubuntu_installer.py instead.\n"
                print "Script could not be completed.\n"
        elif scripttype == "pip":
            logfile = pip.pip_install.run(logfile)
        elif scripttype == "initialize_instance":
            logfile = run_initialize_instance.run(logfile)
        elif scripttype == "update_instance":
            logfile = run_update_instance.run(logfile)
        else:
            logfile.write("Error: redhat_altinstall_installer.py invoked with invalid command: %s" % scripttype)
            print "Error: redhat_altinstall_installer.py invoked with invalid command: %s" % scripttype
        
    # After the function is done, return the logfile.
    return logfile

def main():
    if len(sys.argv) != 6:
        print "Usage: redhat_altinstall_installer.py < --dependencies | --pip | --initialize_instance | --update_instance > --os < redhat > --arch < x64 >"
        print "--dependencies: Install Makahiki dependencies (software packages)."
        print "--pip: Install Makahiki local dependencies using pip."
        print "--initialize_instance: Initialize the Makahiki installation."
        print "--update_instance: Update the Makahiki installation."
        print "--os: Operating system. This script supports redhat (Red Hat Enterprise Linux)."
        print "--arch: Architecture. This script only supports x64 for redhat."
    else:
        args = sys.argv[1:]
        scripttype = args[0].strip()[2:]
        os = args[2].strip()
        arch = args[4].strip()
        
        logfile = logfile_open(scripttype)
        logfile = scriptrunner(scripttype,os,arch,logfile)
        logfile.close()

if __name__ == '__main__':
    main()
