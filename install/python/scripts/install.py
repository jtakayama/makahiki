#!/usr/bin/python

import sys
import os
import datetime
import convenience_functions

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
    logsdir ="/logs"
    prefix = "install_" + scripttype + "_"
    dt = datetime.datetime
    date_suffix = "null"
    try:
        date_suffix = convenience_functions.datestring(dt)
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

def scripthandler(scripttype, os, arch, logfile):
    """
    Chooses and runs an installation script, and which logfile 
    that script will write its output to.
    
    Parameters:
        1. scripttype: A string describing the installation script
           that is being run.
           Supported values: "dependencies", "pip", or "initialize"
        2. os: A string describing the operating system.
           Supported values: "ubuntu" or "redhat"
        3. arch: Architecture. Supported values: "x86" or "x64".
           (Ubuntu is supported for x86 and x64; Red Hat is supported for x64.)
    """
    print "Not yet implemented."

def main():
    if len(sys.argv) != 4:
        print "Usage: install (--dependencies | --pip | --initialize) --os --arch"
        print "--dependencies: Install Makahiki dependencies (software packages)."
        print "--pip: Install Makahiki local dependencies using pip."
        print "--initialize: Initialize the Makahiki installation."
        print "--os: Operating system. Supported values are --ubuntu and --redhat."
        print "--arch: Architecture. Supported values are --x86 and --x64 if your OS is ubuntu, or --x64 if your OS is redhat."
    else:
        args = sys.argv[1:]
        if args[0].strip() == "--dependencies":
            logfile = logfile_open(args[0].strip()[2:])
            logfile.close()
 
        elif args[0].strip() == "--pip":
            logfile = logfile_open(args[0].strip()[2:])
            logfile.close()
                
        elif args[0].strip() == "--initialize":
            logfile = logfile_open(args[0].strip()[2:])
            logfile.close()

if __name__ == '__main__':
    main()
