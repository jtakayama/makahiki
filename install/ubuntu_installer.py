#!/usr/bin/python

import sys
import os
import datetime
import datestring_functions
import dependency.dependency_ubuntu
import pip.pip_install
import run_update_instance
import run_initialize_instance

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
           Supported values: "ubuntu"
        3. arch: Architecture. Ubuntu is supported for "x86" and "x64" architectures.)
        4. logfile: The log file to pass to the installation script.
    """
    if os == "ubuntu" and (arch != "x86" and arch != "x64"):
        logfile.write("Unsupported architecture for %s: %s\n" % (os, arch))
        logfile.write("Script could not be completed.\n")
        print "Unsupported architecture for %s: %s\n" % (os, arch)
        print "Script could not be completed.\n"
        
    elif os == "redhat":
        logfile.write("This is not the script for Red Hat Enterprise Linux. Use install_redhat.py instead.\n")
        logfile.write("Script could not be completed.\n")
        print "This is not the script for Red Hat Enterprise Linux. Use install_redhat.py instead.\n"
        print "Script could not be completed.\n"

    elif os != "ubuntu" and os != "redhat":
        logfile.write("Unsupported operating system: %s\n" % os)
        logfile.write("Script could not be completed\n.")
        print "Unsupported operating system: %s\n" % os
        print "Script could not be completed.\n"
    
    else: 
        if scripttype == "dependencies":
            if os == "ubuntu":
                logfile = dependency.dependency_ubuntu.run(arch, logfile)
            elif os == "redhat":
                logfile.write("This is not the script for Red Hat Enterprise Linux. Use install_redhat.py instead.\n")
                logfile.write("Script could not be completed.")
                print "This is not the script for Red Hat Enterprise Linux. Use install_redhat.py instead.\n"
                print "Script could not be completed.\n"
        elif scripttype == "pip":
            logfile = pip.pip_install.run(logfile)
        elif scripttype == "initialize_instance":
            logfile = run_initialize_instance.run(logfile)
        elif scripttype == "update_instance":
            logfile = run_update_instance.run(logfile)
        else:
            logfile.write("Error: install.py invoked with invalid command: %s\n" % scripttype)
            print "Error: install.py invoked with invalid command: %s\n" % scripttype
        
    # After the function is done, return the logfile.
    return logfile

def main():
    if len(sys.argv) != 6:
        print "Usage: install.py < --dependencies | --pip | --initialize_instance | --update_instance > --os < ubuntu > --arch < x86 | x64 >"
        print "--dependencies: Install Makahiki dependencies (software packages)."
        print "--pip: Install Makahiki local dependencies using pip."
        print "--initialize_instance: Initialize the Makahiki installation."
        print "--update_instance: Update the Makahiki installation."
        print "--os: Operating system. This script only supports ubuntu (Ubuntu Linux)."
        print "--arch: Architecture. Supported values for ubuntu are x86 and x64 if your OS is ubuntu."
    else:
        args = sys.argv[1:]
        scripttype = args[0].strip()[2:]
        os = args[2].strip()
        arch = args[4].strip()
        
        logfile = logfile_open(scripttype)
        scriptrunner(scripttype,os,arch,logfile)
        logfile.close()

if __name__ == '__main__':
    main()
